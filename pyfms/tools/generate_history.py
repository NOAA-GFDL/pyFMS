#!/usr/bin/env python3
"""
Generate structurally faithful FMS raw history files using pyfms diag_manager.

Reads a diag_table.yaml to determine output files and variables, then runs
the FMS diag manager to produce real NetCDF output with reproducible random data.

The internal model timestep is fixed at 1 hour (3600 s). Output scheduling is
driven by the 'freq' field in the diag_table.yaml, as in a real FMS run.

Usage examples:
    # Regular rectangular grid
    generate-history diag_table.yaml --nx 96 --ny 96 [--nz 33] \\
        --calendar noleap --nsteps 720

    # Cubed-sphere atmosphere (requires mpirun -n 6)
    mpirun -n 6 generate-history diag_table.yaml \\
        --grid-type cubed-sphere --ntile 96 --nz 65 \\
        --calendar noleap --nsteps 720

    # Tripolar ocean
    generate-history diag_table.yaml \\
        --grid-type tripolar --nx 1440 --ny 1080 --nz 75 \\
        --calendar noleap --nsteps 720 \\
        --q-vars uo,vo

--nsteps is the number of 1-hour steps to simulate (e.g. 720 = 30 days).
If --nz is absent or 0, all variables are 2-D (y, x).
If --nz > 0, all variables are 3-D (z, y, x).
"""

from __future__ import annotations

import argparse
import os
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

import numpy as np
import yaml

import pyfms

from pyfms.tools.grid_spec import (
    stamp_cubed_sphere_history,
    stamp_tripolar_history,
    write_cubed_sphere_gridspec,
    write_tripolar_gridspec,
)


INTERNAL_TIMESTEP_SECONDS = 3600

CALENDAR_MAP = {
    "NOLEAP": lambda: pyfms.fms.NOLEAP,
    "JULIAN": lambda: pyfms.fms.JULIAN,
    "GREGORIAN": lambda: pyfms.fms.GREGORIAN,
    "THIRTY_DAY": lambda: pyfms.fms.THIRTY_DAY_MONTHS,
}

KIND_MAP = {
    "r4": "float32",
    "r8": "float64",
}


def parse_base_date(base_date_str: str | int) -> datetime:
    """Parse an FMS base_date string into a datetime object.

    Args:
        base_date_str: Six space-separated integers representing
            year, month, day, hour, minute, second (as produced by
            yaml.safe_load of an FMS diag_table.yaml base_date field).

    Returns:
        Corresponding datetime object.

    Raises:
        ValueError: If the string does not contain exactly six fields.
    """
    parts = str(base_date_str).strip().split()
    if len(parts) != 6:
        raise ValueError(
            f"base_date must have 6 space-separated fields, got: {base_date_str!r}"
        )
    y, mo, d, h, mi, s = (int(p) for p in parts)
    return datetime(y, mo, d, h, mi, s)


def collect_vars(diag_table: dict) -> list[tuple[str, str, str]]:
    """Collect unique (module, var_name, dtype) tuples from a diag_table dict.

    Deduplicates across all diag_files entries. Variables appearing in
    multiple files are registered once and sent to all matching outputs
    by the diag manager.

    Args:
        diag_table: Parsed diag_table.yaml content as returned by
            yaml.safe_load.

    Returns:
        List of (module_name, var_name, numpy_dtype_str) tuples, where
        numpy_dtype_str is one of 'float32' or 'float64'.
    """
    seen: dict[tuple[str, str], str] = {}
    for f in diag_table.get("diag_files", []):
        for v in f.get("varlist", []):
            key = (v["module"], v["var_name"])
            if key not in seen:
                kind = v.get("kind", "r4")
                seen[key] = KIND_MAP.get(kind, "float32")
    return [(module, var_name, dtype) for (module, var_name), dtype in seen.items()]


def collect_stems(diag_table: dict) -> list[str]:
    """Return the file_name stem from every diag_files entry.

    Args:
        diag_table: Parsed diag_table.yaml content as returned by
            yaml.safe_load.

    Returns:
        List of file_name strings (one per diag_files entry).
    """
    return [f["file_name"] for f in diag_table.get("diag_files", [])]


def _setup_regular_domain(nx: int, ny: int) -> tuple[int, dict[str, int]]:
    """Set up a rectangular 2-D MPI domain.

    Args:
        nx: Global grid size in x.
        ny: Global grid size in y.

    Returns:
        Tuple of (domain_id, compute) where compute maps 'isc', 'iec',
        'jsc', 'jec' to their 1-indexed values for the local PE.
    """
    npes = pyfms.mpp.npes()
    domain = pyfms.mpp_domains.define_domains(
        global_indices=[0, nx - 1, 0, ny - 1],
        layout=[1, npes],
    )
    pyfms.mpp_domains.define_io_domain(domain_id=domain.domain_id, io_layout=[1, 1])
    return domain.domain_id, {
        "isc": domain.isc, "iec": domain.iec,
        "jsc": domain.jsc, "jec": domain.jec,
    }


def _setup_cubed_sphere_domain(ntile: int) -> tuple[int, dict[str, int]]:
    """Set up a cubic mosaic domain.

    Requires exactly 6 MPI ranks (one per tile).

    Args:
        ntile: Tile grid size (e.g. 96 for C96).

    Returns:
        Tuple of (domain_id, compute) where compute maps 'isc', 'iec',
        'jsc', 'jec' to their 1-indexed values for the local PE.

    Raises:
        RuntimeError: If the number of MPI ranks is not 6.
    """
    npes = pyfms.mpp.npes()
    if npes != 6:
        raise RuntimeError(
            f"cubed-sphere grid type requires exactly 6 MPI ranks, got {npes}. "
            "Run with: mpirun -n 6 generate-history ..."
        )
    domain_id = pyfms.mpp_domains.define_cubic_mosaic(
        ni=[ntile] * 6,
        nj=[ntile] * 6,
        global_indices=[1, ntile, 1, ntile],
        layout=[1, 1],
        ntiles=6,
    )
    pyfms.mpp_domains.define_io_domain(domain_id=domain_id, io_layout=[1, 1])
    compute = pyfms.mpp_domains.get_compute_domain(domain_id=domain_id)
    return domain_id, {
        "isc": compute["isc"], "iec": compute["iec"],
        "jsc": compute["jsc"], "jec": compute["jec"],
    }


def _register_regular_axes(
    nx: int, ny: int, nz: int, domain_id: int, set_name: str = "atm"
) -> dict[str, int]:
    """Register x, y and optionally z diag axes for a regular grid.

    Args:
        nx: Grid size in x.
        ny: Grid size in y.
        nz: Number of vertical levels; 0 means no z axis.
        domain_id: MPI domain id from define_domains / define_cubic_mosaic.
        set_name: Axis set name passed to axis_init (e.g. 'atm').

    Returns:
        Dict with keys 'x', 'y', and 'z' (None when nz == 0) mapping to
        the integer axis ids returned by axis_init.
    """
    id_x = pyfms.diag_manager.axis_init(
        name="x",
        axis_data=np.arange(nx, dtype=np.float64),
        units="point_E",
        cart_name="x",
        domain_id=domain_id,
        long_name="point_E",
        set_name=set_name,
    )
    id_y = pyfms.diag_manager.axis_init(
        name="y",
        axis_data=np.arange(ny, dtype=np.float64),
        units="point_N",
        cart_name="y",
        domain_id=domain_id,
        long_name="point_N",
        set_name=set_name,
    )
    id_z = None
    if nz > 0:
        id_z = pyfms.diag_manager.axis_init(
            name="z",
            axis_data=np.arange(nz, dtype=np.float64),
            units="point_Z",
            cart_name="z",
            long_name="point_Z",
            set_name=set_name,
            not_xy=True,
        )
    return {"x": id_x, "y": id_y, "z": id_z}


def _register_cubed_sphere_axes(
    ntile: int, nz: int, domain_id: int
) -> dict[str, int]:
    """Register x, y and optionally z diag axes for a cubed-sphere grid.

    Passes tile_count=6 so FMS writes separate tile output files.

    Args:
        ntile: Tile grid size.
        nz: Number of vertical levels; 0 means no z axis.
        domain_id: Cubic mosaic domain id from define_cubic_mosaic.

    Returns:
        Dict with keys 'x', 'y', and 'z' (None when nz == 0).
    """
    id_x = pyfms.diag_manager.axis_init(
        name="x",
        axis_data=np.arange(ntile, dtype=np.float64),
        units="point_E",
        cart_name="x",
        domain_id=domain_id,
        long_name="point_E",
        set_name="atm",
        tile_count=6,
    )
    id_y = pyfms.diag_manager.axis_init(
        name="y",
        axis_data=np.arange(ntile, dtype=np.float64),
        units="point_N",
        cart_name="y",
        domain_id=domain_id,
        long_name="point_N",
        set_name="atm",
        tile_count=6,
    )
    id_z = None
    if nz > 0:
        id_z = pyfms.diag_manager.axis_init(
            name="z",
            axis_data=np.arange(nz, dtype=np.float64),
            units="point_Z",
            cart_name="z",
            long_name="point_Z",
            set_name="atm",
            not_xy=True,
        )
    return {"x": id_x, "y": id_y, "z": id_z}


def _register_tripolar_axes(
    nx: int, ny: int, nz: int, domain_id: int
) -> dict[str, int | None]:
    """Register xh/yh (h-grid) and xq/yq (q-grid) axes for a tripolar ocean grid.

    The h-grid (tracer/T-grid) axes are centered at integer positions.
    The q-grid (velocity/U-grid) axes are offset by +0.5 (staggered).

    Args:
        nx: Grid size in x.
        ny: Grid size in y.
        nz: Number of vertical levels; 0 means no z axis.
        domain_id: MPI domain id from define_domains.

    Returns:
        Dict with keys 'xh', 'yh', 'xq', 'yq', and 'z' (None when nz == 0).
    """
    id_xh = pyfms.diag_manager.axis_init(
        name="xh",
        axis_data=np.arange(1.0, nx + 1.0, dtype=np.float64),
        units="degree_east",
        cart_name="x",
        domain_id=domain_id,
        long_name="h-point longitude index",
        set_name="ocean",
    )
    id_yh = pyfms.diag_manager.axis_init(
        name="yh",
        axis_data=np.arange(1.0, ny + 1.0, dtype=np.float64),
        units="degree_north",
        cart_name="y",
        domain_id=domain_id,
        long_name="h-point latitude index",
        set_name="ocean",
    )
    id_xq = pyfms.diag_manager.axis_init(
        name="xq",
        axis_data=np.arange(0.5, nx + 0.5, dtype=np.float64),
        units="degree_east",
        cart_name="x",
        domain_id=domain_id,
        long_name="q-point longitude index",
        set_name="ocean",
    )
    id_yq = pyfms.diag_manager.axis_init(
        name="yq",
        axis_data=np.arange(0.5, ny + 0.5, dtype=np.float64),
        units="degree_north",
        cart_name="y",
        domain_id=domain_id,
        long_name="q-point latitude index",
        set_name="ocean",
    )
    id_z = None
    if nz > 0:
        id_z = pyfms.diag_manager.axis_init(
            name="z_l",
            axis_data=np.arange(nz, dtype=np.float64),
            units="m",
            cart_name="z",
            long_name="Layer pseudo-depth",
            set_name="ocean",
            not_xy=True,
        )
    return {"xh": id_xh, "yh": id_yh, "xq": id_xq, "yq": id_yq, "z": id_z}


def _register_fields(
    vars_list: list[tuple[str, str, str]],
    h_axes: list[int],
    q_axes: list[int],
    q_var_names: set[str],
    start_time: datetime,
) -> list[tuple[int, str]]:
    """Register all diagnostic fields with the diag manager.

    Args:
        vars_list: List of (module_name, var_name, dtype) tuples.
        h_axes: Axis id list for h-point (or default) fields.
        q_axes: Axis id list for q-point fields.
        q_var_names: Set of var_names to place on the q-grid.
        start_time: Simulation start time for init_time.

    Returns:
        List of (field_id, dtype_str) tuples in the same order as vars_list.
    """
    field_ids = []
    for module_name, var_name, dtype in vars_list:
        axes = q_axes if var_name in q_var_names else h_axes
        fid = pyfms.diag_manager.register_field_array(
            module_name=module_name,
            field_name=var_name,
            dtype=dtype,
            axes=list(axes),
            long_name=var_name,
            units="none",
            missing_value=-99.99,
            range_data=np.array([-1e6, 1e6], dtype=dtype),
            init_time=start_time,
        )
        field_ids.append((fid, dtype))
    return field_ids


def _run_time_loop(
    field_ids: list[tuple[int, str]],
    local_shape: tuple[int, ...],
    nsteps: int,
    start_time: datetime,
    timestep: timedelta,
    rng: np.random.Generator,
) -> None:
    """Drive the FMS diag manager time loop.

    Generates random data for each field at each timestep, sends it to the
    diag manager, and advances the simulation clock.

    Args:
        field_ids: List of (field_id, dtype_str) pairs from _register_fields.
        local_shape: Shape of the local (per-PE) data array.
        nsteps: Total number of timesteps to simulate.
        start_time: Simulation start time (used to track current time).
        timestep: Duration of each simulation step.
        rng: NumPy random generator for reproducible synthetic data.
    """
    curr_time = start_time
    for _ in range(nsteps):
        curr_time = curr_time + timestep
        for fid, dtype in field_ids:
            field = rng.random(local_shape, dtype=np.float64).astype(dtype)
            pyfms.diag_manager.send_data(
                diag_field_id=fid,
                field=field,
                time=curr_time,
            )
        pyfms.diag_manager.send_complete(timestep)


def main() -> None:
    """Entry point for the generate-history CLI tool."""
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("diag_table", help="Path to diag_table.yaml")
    parser.add_argument(
        "--grid-type",
        default="regular",
        choices=["regular", "cubed-sphere", "tripolar"],
        help="Grid type: regular (default), cubed-sphere, or tripolar",
    )
    parser.add_argument("--nx", type=int, help="Grid points in x (regular / tripolar)")
    parser.add_argument("--ny", type=int, help="Grid points in y (regular / tripolar)")
    parser.add_argument(
        "--ntile",
        type=int,
        help="Tile size for cubed-sphere (e.g. 96 for C96)",
    )
    parser.add_argument(
        "--nz",
        type=int,
        default=0,
        help="Vertical levels (0 = all vars 2-D)",
    )
    parser.add_argument(
        "--calendar",
        default="NOLEAP",
        type=str.upper,
        choices=list(CALENDAR_MAP),
    )
    parser.add_argument(
        "--nsteps",
        type=int,
        required=True,
        help="Number of 1-hour steps to simulate",
    )
    parser.add_argument(
        "--output-dir",
        default="./output",
        help="Directory for output files (default: ./output)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=0,
        help="Random seed for reproducible data (default: 0)",
    )
    parser.add_argument(
        "--q-vars",
        default="",
        help="Comma-separated var_names to assign to q-grid (tripolar only)",
    )
    args = parser.parse_args()

    grid_type = args.grid_type
    nz = args.nz
    three_d = nz > 0
    timestep = timedelta(seconds=INTERNAL_TIMESTEP_SECONDS)
    rng = np.random.default_rng(args.seed)
    q_var_names: set[str] = set(
        v.strip() for v in args.q_vars.split(",") if v.strip()
    )

    # Validate dimension args
    if grid_type == "cubed-sphere":
        if args.ntile is None:
            parser.error("--ntile is required for --grid-type cubed-sphere")
        ntile = args.ntile
        nx = ny = ntile
    else:
        if args.nx is None or args.ny is None:
            parser.error("--nx and --ny are required for regular/tripolar grid types")
        nx, ny = args.nx, args.ny
        ntile = None

    with open(args.diag_table) as fh:
        diag_table = yaml.safe_load(fh)

    start_time = parse_base_date(diag_table["base_date"])
    end_time = start_time + timestep * args.nsteps

    outdir = Path(args.output_dir).resolve()
    outdir.mkdir(parents=True, exist_ok=True)
    shutil.copy(args.diag_table, outdir / "diag_table.yaml")
    (outdir / "input.nml").write_text(
        "&diag_manager_nml\n    use_modern_diag = .true.\n/\n"
    )

    os.chdir(outdir)

    pyfms.fms.init(calendar_type=CALENDAR_MAP[args.calendar]())

    # -----------------------------------------------------------------------
    # Domain setup
    # -----------------------------------------------------------------------
    if grid_type == "cubed-sphere":
        domain_id, compute = _setup_cubed_sphere_domain(ntile)
    else:
        domain_id, compute = _setup_regular_domain(nx, ny)

    pyfms.diag_manager.init(diag_model_subset=pyfms.diag_manager.DIAG_ALL)
    pyfms.mpp_domains.set_current_domain(domain_id=domain_id)

    # -----------------------------------------------------------------------
    # Axis registration
    # -----------------------------------------------------------------------
    if grid_type == "cubed-sphere":
        axes_dict = _register_cubed_sphere_axes(ntile, nz, domain_id)
        xy_axes = [axes_dict["x"], axes_dict["y"]]
    elif grid_type == "tripolar":
        axes_dict = _register_tripolar_axes(nx, ny, nz, domain_id)
        xy_axes = [axes_dict["xh"], axes_dict["yh"]]      # default h-axes
        xy_q_axes = [axes_dict["xq"], axes_dict["yq"]]
    else:
        axes_dict = _register_regular_axes(nx, ny, nz, domain_id)
        xy_axes = [axes_dict["x"], axes_dict["y"]]

    if three_d and axes_dict["z"] is not None:
        h_axes = xy_axes + [axes_dict["z"]]
        q_axes = (xy_q_axes + [axes_dict["z"]]
                  if grid_type == "tripolar" else h_axes)
    else:
        h_axes = xy_axes
        q_axes = xy_q_axes if grid_type == "tripolar" else h_axes

    # -----------------------------------------------------------------------
    # Field registration
    # -----------------------------------------------------------------------
    vars_list = collect_vars(diag_table)
    if not vars_list:
        raise ValueError("No variables found in diag_table.yaml")

    field_ids = _register_fields(
        vars_list, h_axes, q_axes, q_var_names, start_time
    )

    pyfms.diag_manager.set_time_end(end_time)

    # -----------------------------------------------------------------------
    # Local array shape (per-PE compute domain)
    # -----------------------------------------------------------------------
    isize = compute["iec"] - compute["isc"] + 1
    jsize = compute["jec"] - compute["jsc"] + 1
    local_shape: tuple[int, ...] = (
        (isize, jsize, nz) if three_d else (isize, jsize)
    )

    # -----------------------------------------------------------------------
    # Time loop
    # -----------------------------------------------------------------------
    _run_time_loop(field_ids, local_shape, args.nsteps, start_time, timestep, rng)

    pyfms.diag_manager.end(end_time)
    pyfms.fms.end()

    # -----------------------------------------------------------------------
    # Post-processing: grid spec files and global attributes (root PE only)
    # -----------------------------------------------------------------------
    if pyfms.mpp.pe() == pyfms.mpp.root_pe():
        stems = collect_stems(diag_table)

        if grid_type == "cubed-sphere":
            write_cubed_sphere_gridspec(outdir, ntile)
            stamp_cubed_sphere_history(outdir, ntile, stems)

        elif grid_type == "tripolar":
            write_tripolar_gridspec(outdir, nx, ny)
            stamp_tripolar_history(outdir, stems)

        print(f"Output written to: {outdir}")


if __name__ == "__main__":
    main()
