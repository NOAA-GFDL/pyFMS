#!/usr/bin/env python3
"""
Generate structurally faithful FMS raw history files using pyfms diag_manager.

Reads a diag_table.yaml to determine output files and variables, then runs
the FMS diag manager to produce real NetCDF output with reproducible random data.

The internal model timestep is fixed at 1 hour (3600s). Output scheduling is
driven by the 'freq' field in the diag_table.yaml, as in a real FMS run.

Usage:
    python generate_history.py diag_table.yaml \\
        --nx 96 --ny 96 [--nz 33] \\
        --calendar NOLEAP \\
        --nsteps 720 \\
        [--output-dir ./output] [--seed 0]

--nsteps is the number of 1-hour steps to simulate (e.g. 720 = 30 days).
If --nz is absent or 0, all variables are 2d (x, y).
If --nz > 0, all variables are 3d (x, y, z).
"""

import argparse
import os
import shutil
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import yaml

import pyfms


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
        raise ValueError(f"base_date must have 6 space-separated fields, got: {base_date_str!r}")
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
    seen = {}
    for f in diag_table.get("diag_files", []):
        for v in f.get("varlist", []):
            key = (v["module"], v["var_name"])
            if key not in seen:
                kind = v.get("kind", "r4")
                seen[key] = KIND_MAP.get(kind, "float32")
    return [(module, var_name, dtype) for (module, var_name), dtype in seen.items()]


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("diag_table", help="Path to diag_table.yaml")
    parser.add_argument("--nx", type=int, required=True, help="Grid points in x")
    parser.add_argument("--ny", type=int, required=True, help="Grid points in y")
    parser.add_argument("--nz", type=int, default=0, help="Vertical levels (0 = all vars are 2d)")
    parser.add_argument("--calendar", default="NOLEAP", type=str.upper, choices=list(CALENDAR_MAP))
    parser.add_argument("--nsteps", type=int, required=True, help="Number of 1-hour steps to simulate")
    parser.add_argument("--output-dir", default="./output", help="Directory for output files (created if absent)")
    parser.add_argument("--seed", type=int, default=0, help="Random seed for reproducible output (default: 0)")
    args = parser.parse_args()

    nx, ny, nz = args.nx, args.ny, args.nz
    three_d = nz > 0
    timestep = timedelta(seconds=INTERNAL_TIMESTEP_SECONDS)
    rng = np.random.default_rng(args.seed)

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

    npes = pyfms.mpp.npes()
    domain = pyfms.mpp_domains.define_domains(
        global_indices=[0, nx - 1, 0, ny - 1],
        layout=[1, npes],
    )
    pyfms.mpp_domains.define_io_domain(
        domain_id=domain.domain_id,
        io_layout=[1, 1],
    )

    pyfms.diag_manager.init(diag_model_subset=pyfms.diag_manager.DIAG_ALL)
    pyfms.mpp_domains.set_current_domain(domain_id=domain.domain_id)

    id_x = pyfms.diag_manager.axis_init(
        name="x",
        axis_data=np.arange(nx, dtype=np.float64),
        units="point_E",
        cart_name="x",
        domain_id=domain.domain_id,
        long_name="point_E",
        set_name="atm",
    )
    id_y = pyfms.diag_manager.axis_init(
        name="y",
        axis_data=np.arange(ny, dtype=np.float64),
        units="point_N",
        cart_name="y",
        domain_id=domain.domain_id,
        long_name="point_N",
        set_name="atm",
    )
    axes = [id_x, id_y]

    if three_d:
        id_z = pyfms.diag_manager.axis_init(
            name="z",
            axis_data=np.arange(nz, dtype=np.float64),
            units="point_Z",
            cart_name="z",
            long_name="point_Z",
            set_name="atm",
            not_xy=True,
        )
        axes = [id_x, id_y, id_z]

    vars_list = collect_vars(diag_table)
    if not vars_list:
        raise ValueError("No variables found in diag_table.yaml")

    field_ids = []
    for module_name, var_name, dtype in vars_list:
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

    pyfms.diag_manager.set_time_end(end_time)

    local_shape = (
        (domain.iec - domain.isc + 1, domain.jec - domain.jsc + 1, nz)
        if three_d
        else (domain.iec - domain.isc + 1, domain.jec - domain.jsc + 1)
    )

    curr_time = start_time
    for _ in range(args.nsteps):
        curr_time = curr_time + timestep
        for fid, dtype in field_ids:
            field = rng.random(local_shape, dtype=np.float64).astype(dtype)
            pyfms.diag_manager.send_data(
                diag_field_id=fid,
                field=field,
                time=curr_time,
            )
        pyfms.diag_manager.send_complete(timestep)

    pyfms.diag_manager.end(end_time)
    pyfms.fms.end()

    if pyfms.mpp.pe() == pyfms.mpp.root_pe():
        print(f"Output written to: {outdir}")


if __name__ == "__main__":
    main()
