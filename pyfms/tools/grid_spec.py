"""
Generate minimally functional FMS grid spec files for regridding.

Produces NetCDF files compatible with fregrid (FMS native regridder).
SCRIP files are also written for ESMF/esmpy compatibility.

Two grid types are supported:
  cubed-sphere: C{ntile}_mosaic.nc + C{ntile}_grid.tile{N}.nc + C{ntile}_scrip.nc
  tripolar:     ocean_mosaic.nc + ocean_hgrid.nc + ocean_scrip.nc
"""

from __future__ import annotations

from pathlib import Path

import netCDF4 as nc
import numpy as np
from numpy.typing import NDArray


EARTH_RADIUS = 6.371e6


# ---------------------------------------------------------------------------
# Cubed-sphere geometry
# ---------------------------------------------------------------------------


def _face_vectors(tile: int) -> tuple[NDArray, NDArray, NDArray]:
    """Return the face-normal (N), right-tangent (R), and up-tangent (U) unit
    vectors for one of the 6 FMS gnomonic equal-angle cube faces.

    The tile ordering and orientation follow the GFDL/FMS convention produced
    by ``make_hgrid --grid_type gnomonic_ed``:
      tile 1 — equatorial, lon_center=350°; x=east,  y=north
      tile 2 — equatorial, lon_center=80°;  x=east,  y=north
      tile 3 — north polar cap;             x=toward 170°, y=toward 260°
      tile 4 — equatorial, lon_center=170°; x=south (−z),  y=toward 260°
      tile 5 — equatorial, lon_center=260°; x=south (−z),  y=toward 350°
      tile 6 — south polar cap;             x=toward 80°, y=toward 350°

    Tiles 4 and 5 have the x-axis pointing southward (−z) so that their
    edges align correctly with tiles 1, 2, 3, and 6 at the cube contacts.

    The contact connectivity in the C{N}_mosaic.nc files produced by this
    module is only valid for this specific orientation.

    Args:
        tile: Integer in [1, 6].

    Returns:
        Tuple of three (3,) float64 unit vectors (N, R, U).
    """
    if tile == 1:
        lon = np.radians(350.0)
        N = np.array([np.cos(lon), np.sin(lon), 0.0])
        R = np.array([-np.sin(lon), np.cos(lon), 0.0])  # east at lon=350°
        U = np.array([0.0, 0.0, 1.0])
    elif tile == 2:
        lon = np.radians(80.0)
        N = np.array([np.cos(lon), np.sin(lon), 0.0])
        R = np.array([-np.sin(lon), np.cos(lon), 0.0])  # east at lon=80°
        U = np.array([0.0, 0.0, 1.0])
    elif tile == 3:
        N = np.array([0.0, 0.0, 1.0])
        R = np.array([np.cos(np.radians(170.0)), np.sin(np.radians(170.0)), 0.0])
        U = np.array([np.cos(np.radians(260.0)), np.sin(np.radians(260.0)), 0.0])
    elif tile == 4:
        lon = np.radians(170.0)
        N = np.array([np.cos(lon), np.sin(lon), 0.0])
        R = np.array([0.0, 0.0, -1.0])  # south (−z)
        U = np.array([-np.sin(lon), np.cos(lon), 0.0])  # east at lon=170° → toward 260°
    elif tile == 5:
        lon = np.radians(260.0)
        N = np.array([np.cos(lon), np.sin(lon), 0.0])
        R = np.array([0.0, 0.0, -1.0])  # south (−z)
        U = np.array([-np.sin(lon), np.cos(lon), 0.0])  # east at lon=260° → toward 350°
    elif tile == 6:
        N = np.array([0.0, 0.0, -1.0])
        R = np.array([np.cos(np.radians(80.0)), np.sin(np.radians(80.0)), 0.0])
        U = np.array([np.cos(np.radians(350.0)), np.sin(np.radians(350.0)), 0.0])
    else:
        raise ValueError(f"tile must be 1–6, got {tile}")
    return N, R, U


def _gnomonic_tile_latlon(ntile: int, tile: int) -> tuple[NDArray, NDArray]:
    """Compute gnomonic equal-angle supergrid lat/lon for one cube face.

    The supergrid has (2*ntile+1, 2*ntile+1) points — cell centers and corners
    interleaved. The equal-angle parameterisation maps the angular interval
    [-π/4, π/4] uniformly in both directions.

    Args:
        ntile: Model grid size per tile (e.g. 96 for C96).
        tile: Integer in [1, 6].

    Returns:
        Tuple (lat, lon) each of shape (2*ntile+1, 2*ntile+1) in degrees.
        lon is in [0°, 360°).
    """
    sn = 2 * ntile
    ang = np.linspace(-np.pi / 4, np.pi / 4, sn + 1)
    N, R, U = _face_vectors(tile)
    A, B = np.meshgrid(ang, ang)  # (sn+1, sn+1); A varies along i, B along j
    ta = np.tan(A)[..., np.newaxis]
    tb = np.tan(B)[..., np.newaxis]
    P = N + ta * R + tb * U  # (sn+1, sn+1, 3)
    r = np.linalg.norm(P, axis=-1, keepdims=True)
    P = P / r
    lat = np.degrees(np.arcsin(np.clip(P[..., 2], -1.0, 1.0)))
    lon = np.degrees(np.arctan2(P[..., 1], P[..., 0])) % 360.0
    return lat, lon


# ---------------------------------------------------------------------------
# Shared geometry helpers
# ---------------------------------------------------------------------------


def _haversine(lat1: NDArray, lon1: NDArray, lat2: NDArray, lon2: NDArray) -> NDArray:
    """Great circle distance in metres between arrays of (lat, lon) pairs.

    Args:
        lat1, lon1: Starting coordinates in degrees.
        lat2, lon2: Ending coordinates in degrees.

    Returns:
        Array of distances in metres, same shape as inputs.
    """
    d_lat = np.radians(lat2 - lat1)
    d_lon = np.radians(lon2 - lon1)
    lat1_r = np.radians(lat1)
    lat2_r = np.radians(lat2)
    a = (
        np.sin(d_lat / 2) ** 2
        + np.cos(lat1_r) * np.cos(lat2_r) * np.sin(d_lon / 2) ** 2
    )
    return 2.0 * EARTH_RADIUS * np.arcsin(np.sqrt(np.clip(a, 0.0, 1.0)))


def _to_cartesian(lat_deg: NDArray, lon_deg: NDArray) -> NDArray:
    """Convert (lat, lon) degrees to 3-D Cartesian unit vectors.

    Args:
        lat_deg: Latitude array in degrees.
        lon_deg: Longitude array in degrees.

    Returns:
        Array of shape (*lat_deg.shape, 3).
    """
    lat = np.radians(lat_deg)
    lon = np.radians(lon_deg)
    return np.stack(
        [np.cos(lat) * np.cos(lon), np.cos(lat) * np.sin(lon), np.sin(lat)], axis=-1
    )


def _triangle_solid_angle(a: NDArray, b: NDArray, c: NDArray) -> NDArray:
    """Solid angle (steradians) of a spherical triangle with vertices a, b, c.

    Uses the formula: Omega = 2 * arctan( |a·(b×c)| / (1 + a·b + b·c + a·c) ).

    Args:
        a, b, c: Arrays of shape (..., 3) — Cartesian unit vectors.

    Returns:
        Array of solid angles in steradians, shape (...,).
    """
    bxc = np.cross(b, c)
    num = np.abs(np.einsum("...i,...i->...", a, bxc))
    den = 1.0 + (
        np.einsum("...i,...i->...", a, b)
        + np.einsum("...i,...i->...", b, c)
        + np.einsum("...i,...i->...", a, c)
    )
    return 2.0 * np.arctan2(num, den)


def _cell_areas(lat: NDArray, lon: NDArray) -> NDArray:
    """Cell areas in m² for a supergrid lat/lon array.

    Splits each quadrilateral cell into two triangles and sums
    spherical excess areas (Girard's theorem).

    Args:
        lat, lon: Arrays of shape (M+1, N+1) — supergrid corners.

    Returns:
        Array of shape (M, N) — one area per cell in m².
    """
    v = _to_cartesian(lat, lon)
    v1 = v[:-1, :-1]  # bottom-left
    v2 = v[:-1, 1:]  # bottom-right
    v3 = v[1:, 1:]  # top-right
    v4 = v[1:, :-1]  # top-left
    a1 = _triangle_solid_angle(v1, v2, v3)
    a2 = _triangle_solid_angle(v1, v3, v4)
    return (a1 + a2) * EARTH_RADIUS ** 2


def _dx_dy(lat: NDArray, lon: NDArray) -> tuple[NDArray, NDArray]:
    """Edge lengths in metres on a supergrid.

    Args:
        lat, lon: Supergrid arrays of shape (nyp, nxp).

    Returns:
        Tuple (dx, dy):
          dx — shape (nyp, nx)  — zonal edge lengths (i-direction)
          dy — shape (ny, nxp) — meridional edge lengths (j-direction)
    """
    dx = _haversine(lat[:, :-1], lon[:, :-1], lat[:, 1:], lon[:, 1:])
    dy = _haversine(lat[:-1, :], lon[:-1, :], lat[1:, :], lon[1:, :])
    return dx, dy


def _angle_dx(lat: NDArray, lon: NDArray) -> NDArray:
    """Approximate grid rotation angle (degrees east) at every supergrid point.

    Defined as the angle between the local x-axis of the grid and geographic
    east.  Computed from the bearing between adjacent x-direction points.

    Args:
        lat, lon: Supergrid arrays of shape (nyp, nxp).

    Returns:
        Array of shape (nyp, nxp) in degrees.
    """
    # Forward bearing at each interior/edge point (central/forward difference)
    lat_r = np.radians(lat)
    lon_r = np.radians(lon)
    # Use central difference except at right boundary
    dlat = np.diff(lat_r, axis=1)  # (nyp, nxp-1)
    dlon = np.diff(lon_r, axis=1)
    lat_mid = (lat_r[:, :-1] + lat_r[:, 1:]) / 2
    bearing = np.degrees(
        np.arctan2(
            np.sin(dlon) * np.cos(lat_r[:, 1:]),
            np.cos(lat_mid) * np.sin(lat_r[:, 1:])
            - np.sin(lat_mid) * np.cos(lat_r[:, 1:]) * np.cos(dlon),
        )
    )  # (nyp, nxp-1)
    # Pad right edge by repeating the last column
    angle = np.concatenate([bearing, bearing[:, -1:]], axis=1)
    return angle


# ---------------------------------------------------------------------------
# Mosaic file writers
# ---------------------------------------------------------------------------


def _write_char_var(ncvar: nc.Variable, value: str) -> None:
    """Write a string into a (string,) char variable, null-padded."""
    n = ncvar.shape[0]
    b = value.encode("ascii")
    arr = np.zeros(n, dtype="S1")
    arr[: len(b)] = np.frombuffer(b, dtype="S1")
    ncvar[:] = arr


def _write_char_array(ncvar: nc.Variable, values: list[str]) -> None:
    """Write strings into a (n, string) char variable, null-padded."""
    n = ncvar.shape[1]
    for i, v in enumerate(values):
        b = v.encode("ascii")
        arr = np.zeros(n, dtype="S1")
        arr[: len(b)] = np.frombuffer(b, dtype="S1")
        ncvar[i, :] = arr


def _write_grid_tile_nc(
    path: Path, lat: NDArray, lon: NDArray, *, projection: str = "cube_gnomonic"
) -> None:
    """Write a single grid tile NetCDF file (FMS hgrid format).

    Args:
        path: Output file path.
        lat, lon: Supergrid arrays of shape (nyp, nxp) in degrees.
        projection: Value for the ``tile:projection`` attribute.
    """
    nyp, nxp = lat.shape
    ny, nx = nyp - 1, nxp - 1

    dx, dy = _dx_dy(lat, lon)
    area = _cell_areas(lat, lon)
    angle = _angle_dx(lat, lon)

    ds = nc.Dataset(path, "w", format="NETCDF3_64BIT_OFFSET")
    try:
        ds.createDimension("string", 255)
        ds.createDimension("nx", nx)
        ds.createDimension("ny", ny)
        ds.createDimension("nxp", nxp)
        ds.createDimension("nyp", nyp)

        vt = ds.createVariable("tile", "c", ("string",))
        vt.standard_name = "grid_tile_spec"
        vt.geometry = "spherical"
        vt.north_pole = "0.0 90.0"
        vt.projection = projection
        vt.discretization = "logically_rectangular"
        vt.conformal = "FALSE"
        _write_char_var(vt, "tile1")

        vx = ds.createVariable("x", "f8", ("nyp", "nxp"))
        vx.standard_name = "geographic_longitude"
        vx.units = "degree_east"
        vx[:] = lon

        vy = ds.createVariable("y", "f8", ("nyp", "nxp"))
        vy.standard_name = "geographic_latitude"
        vy.units = "degree_north"
        vy[:] = lat

        vdx = ds.createVariable("dx", "f8", ("nyp", "nx"))
        vdx.standard_name = "grid_edge_x_distance"
        vdx.units = "meters"
        vdx[:] = dx

        vdy = ds.createVariable("dy", "f8", ("ny", "nxp"))
        vdy.standard_name = "grid_edge_y_distance"
        vdy.units = "meters"
        vdy[:] = dy

        va = ds.createVariable("area", "f8", ("ny", "nx"))
        va.standard_name = "grid_cell_area"
        va.units = "m2"
        va[:] = area

        vang = ds.createVariable("angle_dx", "f8", ("nyp", "nxp"))
        vang.standard_name = "grid_vertex_x_angle_WRT_geographic_east"
        vang.units = "degrees_east"
        vang[:] = angle

        ds.grid_version = "0.2"
    finally:
        ds.close()


def _write_mosaic_nc(
    path: Path,
    mosaic_name: str,
    gridlocation: str,
    gridfiles: list[str],
    gridtiles: list[str],
    contacts: list[str],
    contact_index: list[str],
) -> None:
    """Write a FMS mosaic descriptor NetCDF file.

    Args:
        path: Output file path.
        mosaic_name: Value of the ``mosaic`` variable.
        gridlocation: Directory containing grid tile files.
        gridfiles: List of tile filename strings.
        gridtiles: List of tile name strings (e.g. ["tile1", ...]).
        contacts: List of contact specifier strings.
        contact_index: List of contact index strings (same length as contacts).
    """
    ntiles = len(gridfiles)
    ncontact = len(contacts)

    ds = nc.Dataset(path, "w", format="NETCDF3_64BIT_OFFSET")
    try:
        ds.createDimension("ntiles", ntiles)
        ds.createDimension("ncontact", ncontact)
        ds.createDimension("string", 255)

        vm = ds.createVariable("mosaic", "c", ("string",))
        vm.standard_name = "grid_mosaic_spec"
        vm.children = "gridtiles"
        vm.contact_regions = "contacts"
        vm.grid_descriptor = ""
        _write_char_var(vm, mosaic_name)

        vgl = ds.createVariable("gridlocation", "c", ("string",))
        vgl.standard_name = "grid_file_location"
        _write_char_var(vgl, gridlocation)

        vgf = ds.createVariable("gridfiles", "c", ("ntiles", "string"))
        _write_char_array(vgf, gridfiles)

        vgt = ds.createVariable("gridtiles", "c", ("ntiles", "string"))
        _write_char_array(vgt, gridtiles)

        vc = ds.createVariable("contacts", "c", ("ncontact", "string"))
        vc.standard_name = "grid_contact_spec"
        vc.contact_type = "boundary"
        vc.alignment = "true"
        vc.contact_index = "contact_index"
        vc.orientation = "orient"
        _write_char_array(vc, contacts)

        vci = ds.createVariable("contact_index", "c", ("ncontact", "string"))
        vci.standard_name = "starting_ending_point_index_of_contact"
        _write_char_array(vci, contact_index)

        ds.grid_version = "0.2"
    finally:
        ds.close()


def _write_scrip_nc(path: Path, lat: NDArray, lon: NDArray) -> None:
    """Write a SCRIP-format grid file derived from a supergrid.

    Cell centers come from every other supergrid point (even indices),
    and cell corners from the 4 surrounding odd-indexed points.

    Args:
        path: Output file path.
        lat, lon: Supergrid arrays of shape (nyp, nxp) in degrees,
            where nyp = 2*ny+1, nxp = 2*nx+1.
    """
    nyp, nxp = lat.shape
    ny, nx = (nyp - 1) // 2, (nxp - 1) // 2
    grid_size = ny * nx

    # Centers: supergrid even-indexed points (2i, 2j) for i in 0..ny-1, j in 0..nx-1
    lat_ctr = lat[1::2, 1::2].ravel()  # (grid_size,)
    lon_ctr = lon[1::2, 1::2].ravel()

    # Corners: 4 corners of each cell from supergrid
    # For cell (iy, ix): corners at supergrid (2*iy, 2*ix), (2*iy, 2*ix+2),
    #                    (2*iy+2, 2*ix+2), (2*iy+2, 2*ix)
    iy = np.arange(ny)
    ix = np.arange(nx)
    IY, IX = np.meshgrid(iy, ix, indexing="ij")  # (ny, nx)
    si = 2 * IY  # supergrid j index of bottom-left corner
    sj = 2 * IX  # supergrid i index of bottom-left corner

    lat_corners = np.stack(
        [
            lat[si, sj].ravel(),
            lat[si, sj + 2].ravel(),
            lat[si + 2, sj + 2].ravel(),
            lat[si + 2, sj].ravel(),
        ],
        axis=-1,
    )  # (grid_size, 4)

    lon_corners = np.stack(
        [
            lon[si, sj].ravel(),
            lon[si, sj + 2].ravel(),
            lon[si + 2, sj + 2].ravel(),
            lon[si + 2, sj].ravel(),
        ],
        axis=-1,
    )

    ds = nc.Dataset(path, "w", format="NETCDF3_64BIT_OFFSET")
    try:
        ds.createDimension("grid_size", grid_size)
        ds.createDimension("grid_corners", 4)
        ds.createDimension("grid_rank", 2)

        vdims = ds.createVariable("grid_dims", "i4", ("grid_rank",))
        vdims[:] = [ny, nx]

        vcl = ds.createVariable("grid_center_lat", "f8", ("grid_size",))
        vcl.units = "degrees"
        vcl[:] = lat_ctr

        vclo = ds.createVariable("grid_center_lon", "f8", ("grid_size",))
        vclo.units = "degrees"
        vclo[:] = lon_ctr

        vkl = ds.createVariable("grid_corner_lat", "f8", ("grid_size", "grid_corners"))
        vkl.units = "degrees"
        vkl[:] = lat_corners

        vklo = ds.createVariable("grid_corner_lon", "f8", ("grid_size", "grid_corners"))
        vklo.units = "degrees"
        vklo[:] = lon_corners

        vmask = ds.createVariable("grid_imask", "i4", ("grid_size",))
        vmask.units = "unitless"
        vmask[:] = np.ones(grid_size, dtype=np.int32)

        ds.title = "SCRIP grid file"
        ds.conventions = "SCRIP"
    finally:
        ds.close()


# ---------------------------------------------------------------------------
# Public interface: cubed-sphere
# ---------------------------------------------------------------------------


def write_cubed_sphere_gridspec(outdir: Path | str, ntile: int) -> None:
    """Write a complete cubed-sphere FMS grid spec to *outdir*.

    Produces:
      C{ntile}_grid.tile{1..6}.nc — per-tile supergrid files
      C{ntile}_mosaic.nc          — FMS mosaic descriptor (for fregrid)
      C{ntile}_scrip.nc           — SCRIP file (for ESMF/esmpy, bonus)

    The geometry uses the gnomonic equal-angle projection with the GFDL/FMS
    tile orientation convention, so the contact strings in the mosaic file
    are valid for regridding with fregrid.

    Args:
        outdir: Directory where files will be written (must exist).
        ntile: Model grid size per tile side (e.g. 96 for C96).
    """
    outdir = Path(outdir)
    n = ntile
    sn = 2 * n  # supergrid size per tile side
    mosaic_name = f"C{n}_mosaic"

    all_lat, all_lon = [], []

    for tile in range(1, 7):
        lat, lon = _gnomonic_tile_latlon(n, tile)
        all_lat.append(lat)
        all_lon.append(lon)
        fname = f"C{n}_grid.tile{tile}.nc"
        _write_grid_tile_nc(outdir / fname, lat, lon, projection="cube_gnomonic")

    # Mosaic file — contact index strings use the supergrid size sn
    contacts = [
        f"{mosaic_name}:tile1::{mosaic_name}:tile2",
        f"{mosaic_name}:tile1::{mosaic_name}:tile3",
        f"{mosaic_name}:tile1::{mosaic_name}:tile5",
        f"{mosaic_name}:tile1::{mosaic_name}:tile6",
        f"{mosaic_name}:tile2::{mosaic_name}:tile3",
        f"{mosaic_name}:tile2::{mosaic_name}:tile4",
        f"{mosaic_name}:tile2::{mosaic_name}:tile6",
        f"{mosaic_name}:tile3::{mosaic_name}:tile4",
        f"{mosaic_name}:tile3::{mosaic_name}:tile5",
        f"{mosaic_name}:tile4::{mosaic_name}:tile5",
        f"{mosaic_name}:tile4::{mosaic_name}:tile6",
        f"{mosaic_name}:tile5::{mosaic_name}:tile6",
    ]
    contact_index = [
        f"{sn}:{sn},1:{sn}::1:1,1:{sn}",
        f"1:{sn},{sn}:{sn}::1:1,{sn}:1",
        f"1:1,1:{sn}::{sn}:1,{sn}:{sn}",
        f"1:{sn},1:1::1:{sn},{sn}:{sn}",
        f"1:{sn},{sn}:{sn}::1:{sn},1:1",
        f"{sn}:{sn},1:{sn}::{sn}:1,1:1",
        f"1:{sn},1:1::{sn}:{sn},{sn}:1",
        f"{sn}:{sn},1:{sn}::1:1,1:{sn}",
        f"1:{sn},{sn}:{sn}::1:1,{sn}:1",
        f"1:{sn},{sn}:{sn}::1:{sn},1:1",
        f"{sn}:{sn},1:{sn}::{sn}:1,1:1",
        f"{sn}:{sn},1:{sn}::1:1,1:{sn}",
    ]
    _write_mosaic_nc(
        outdir / f"{mosaic_name}.nc",
        mosaic_name=mosaic_name,
        gridlocation="./",
        gridfiles=[f"C{n}_grid.tile{t}.nc" for t in range(1, 7)],
        gridtiles=[f"tile{t}" for t in range(1, 7)],
        contacts=contacts,
        contact_index=contact_index,
    )

    # SCRIP: combine all 6 tiles into one flat SCRIP file
    scrip_path = outdir / f"C{n}_scrip.nc"
    _write_cubed_sphere_scrip(scrip_path, all_lat, all_lon, ntile)


def _write_cubed_sphere_scrip(
    path: Path, all_lat: list[NDArray], all_lon: list[NDArray], ntile: int
) -> None:
    """Write a combined SCRIP file for all 6 cube tiles.

    Args:
        path: Output file path.
        all_lat, all_lon: Lists of 6 supergrid arrays, one per tile.
        ntile: Model grid size per tile side.
    """
    sn = 2 * ntile
    cells_per_tile = ntile * ntile
    grid_size = 6 * cells_per_tile

    lat_ctr = np.empty(grid_size)
    lon_ctr = np.empty(grid_size)
    lat_corners = np.empty((grid_size, 4))
    lon_corners = np.empty((grid_size, 4))

    for t, (lat, lon) in enumerate(zip(all_lat, all_lon)):
        start = t * cells_per_tile
        end = start + cells_per_tile

        lat_ctr[start:end] = lat[1::2, 1::2].ravel()
        lon_ctr[start:end] = lon[1::2, 1::2].ravel()

        iy = np.arange(ntile)
        ix = np.arange(ntile)
        IY, IX = np.meshgrid(iy, ix, indexing="ij")
        si = 2 * IY
        sj = 2 * IX

        lat_corners[start:end, 0] = lat[si, sj].ravel()
        lat_corners[start:end, 1] = lat[si, sj + 2].ravel()
        lat_corners[start:end, 2] = lat[si + 2, sj + 2].ravel()
        lat_corners[start:end, 3] = lat[si + 2, sj].ravel()
        lon_corners[start:end, 0] = lon[si, sj].ravel()
        lon_corners[start:end, 1] = lon[si, sj + 2].ravel()
        lon_corners[start:end, 2] = lon[si + 2, sj + 2].ravel()
        lon_corners[start:end, 3] = lon[si + 2, sj].ravel()

    ds = nc.Dataset(path, "w", format="NETCDF3_64BIT_OFFSET")
    try:
        ds.createDimension("grid_size", grid_size)
        ds.createDimension("grid_corners", 4)
        ds.createDimension("grid_rank", 2)

        vdims = ds.createVariable("grid_dims", "i4", ("grid_rank",))
        vdims[:] = [6 * ntile, ntile]

        vcl = ds.createVariable("grid_center_lat", "f8", ("grid_size",))
        vcl.units = "degrees"
        vcl[:] = lat_ctr

        vclo = ds.createVariable("grid_center_lon", "f8", ("grid_size",))
        vclo.units = "degrees"
        vclo[:] = lon_ctr

        vkl = ds.createVariable("grid_corner_lat", "f8", ("grid_size", "grid_corners"))
        vkl.units = "degrees"
        vkl[:] = lat_corners

        vklo = ds.createVariable("grid_corner_lon", "f8", ("grid_size", "grid_corners"))
        vklo.units = "degrees"
        vklo[:] = lon_corners

        vmask = ds.createVariable("grid_imask", "i4", ("grid_size",))
        vmask.units = "unitless"
        vmask[:] = np.ones(grid_size, dtype=np.int32)

        ds.title = f"Cubed-sphere C{ntile} SCRIP grid"
        ds.conventions = "SCRIP"
    finally:
        ds.close()


# ---------------------------------------------------------------------------
# Public interface: tripolar ocean
# ---------------------------------------------------------------------------


def _tripolar_supergrid(
    nx: int, ny: int, lat_south: float = -80.0, lat_bp: float = 65.0
) -> tuple[NDArray, NDArray]:
    """Generate a simplified tripolar ocean supergrid.

    The domain uses a Mercator-like regular spacing in the southern region
    (lat_south to lat_bp) and a bipolar-fold approximation north of lat_bp.
    The supergrid has (2*ny+1, 2*nx+1) points.

    Args:
        nx: Number of model grid cells in x.
        ny: Number of model grid cells in y.
        lat_south: Southernmost latitude of the domain.
        lat_bp: Latitude of the bipolar fold join.

    Returns:
        Tuple (lat, lon) each of shape (2*ny+1, 2*nx+1) in degrees.
        lon is in [-180°, 180°].
    """
    sny = 2 * ny
    snx = 2 * nx

    # x-axis: uniform longitude spanning full 360°
    lon_1d = np.linspace(-180.0, 180.0, snx + 1, endpoint=True)

    # y-axis: split between regular and bipolar regions
    # Count supergrid rows allocated to each region (proportional to lat range)
    lat_range_total = 90.0 - lat_south
    lat_range_reg = lat_bp - lat_south
    n_reg = max(2, int(round(sny * lat_range_reg / lat_range_total)))
    n_bp = sny - n_reg

    # Regular region: Mercator-like, enhanced resolution near equator
    lat_reg = np.linspace(lat_south, lat_bp, n_reg + 1)

    # Bipolar region north of lat_bp: use a simple conformal-like mapping
    # The bipolar cap linearly interpolates lat from lat_bp to 90 but the
    # longitude folds at the midpoint (i=snx/2).
    lat_bp_1d = np.linspace(lat_bp, 90.0, n_bp + 1)

    # Concatenate lat_1d (drop the duplicate lat_bp row)
    lat_1d = np.concatenate([lat_reg, lat_bp_1d[1:]])  # (sny+1,)

    # Build 2D arrays
    LON, LAT = np.meshgrid(lon_1d, lat_1d)  # (sny+1, snx+1)

    # Apply bipolar fold north of n_reg rows: fold x symmetrically
    for j in range(n_reg, sny + 1):
        frac = (j - n_reg) / max(1, n_bp)  # 0 at join, 1 at pole
        # Fold: mirror the right half of the longitude axis
        fold_lon = lon_1d.copy()
        fold_lon[snx // 2 + 1 :] = lon_1d[snx // 2 - 1 :: -1][: snx // 2]
        LON[j, :] = fold_lon + frac * (0.0 - fold_lon)  # blend toward 0 at pole
        # Latitude still increases smoothly
        LAT[j, :] = lat_1d[j]

    return LAT, LON


def write_tripolar_gridspec(
    outdir: Path | str, nx: int, ny: int, lat_south: float = -80.0, lat_bp: float = 65.0
) -> None:
    """Write a complete tripolar ocean FMS grid spec to *outdir*.

    Produces:
      ocean_hgrid.nc   — supergrid file (FMS hgrid format, for fregrid)
      ocean_mosaic.nc  — FMS mosaic descriptor
      ocean_scrip.nc   — SCRIP file (for ESMF/esmpy, bonus)

    The tripolar grid uses a Mercator-like regular section south of
    *lat_bp* and a simplified bipolar fold north of it.  The longitude
    is periodic (the eastern edge connects to the western edge).

    Args:
        outdir: Directory where files will be written (must exist).
        nx: Model grid size in x (number of longitude cells).
        ny: Model grid size in y (number of latitude rows).
        lat_south: Southern boundary latitude in degrees.
        lat_bp: Latitude of the bipolar fold join in degrees.
    """
    outdir = Path(outdir)
    lat, lon = _tripolar_supergrid(nx, ny, lat_south, lat_bp)

    _write_grid_tile_nc(outdir / "ocean_hgrid.nc", lat, lon, projection="tripolar")

    snx = 2 * nx
    sny = 2 * ny
    contacts = [
        "ocean_mosaic:tile1::ocean_mosaic:tile1",
        "ocean_mosaic:tile1::ocean_mosaic:tile1",
    ]
    contact_index = [
        f"{snx}:{snx},1:{sny}::1:1,1:{sny}",  # periodic x
        f"1:{snx // 2},{sny}:{sny}::{snx}:{snx // 2 + 1},{sny}:{sny}",  # bipolar fold
    ]
    _write_mosaic_nc(
        outdir / "ocean_mosaic.nc",
        mosaic_name="ocean_mosaic",
        gridlocation="./",
        gridfiles=["ocean_hgrid.nc"],
        gridtiles=["tile1"],
        contacts=contacts,
        contact_index=contact_index,
    )

    _write_scrip_nc(outdir / "ocean_scrip.nc", lat, lon)


# ---------------------------------------------------------------------------
# Post-processing: add global attributes to history NetCDF files
# ---------------------------------------------------------------------------


def stamp_cubed_sphere_history(
    outdir: Path | str, ntile: int, file_stems: list[str]
) -> None:
    """Add cubed-sphere grid global attributes to FMS history tile files.

    For each file stem in *file_stems*, opens
    ``{outdir}/{stem}.tile{N}.nc`` (N = 1..6) and sets:
      ``grid_type = "cubic_mosaic"``
      ``grid_tile = "N"``
      ``associated_files = "area: C{ntile}_mosaic.nc"``

    Args:
        outdir: Directory containing the history files.
        ntile: Tile size (used to build the mosaic file name).
        file_stems: List of output file name stems (without tile suffix).
    """
    outdir = Path(outdir)
    for stem in file_stems:
        for t in range(1, 7):
            path = outdir / f"{stem}.tile{t}.nc"
            if not path.exists():
                continue
            with nc.Dataset(path, "a") as ds:
                ds.grid_type = "cubic_mosaic"
                ds.grid_tile = str(t)
                ds.associated_files = f"area: C{ntile}_mosaic.nc"
                for vname, var in ds.variables.items():
                    if vname not in (
                        "time",
                        "time_bnds",
                        "average_T1",
                        "average_T2",
                        "average_DT",
                    ):
                        var.interp_method = "conserve_order1"


def stamp_tripolar_history(outdir: Path | str, file_stems: list[str]) -> None:
    """Add tripolar grid global attributes to FMS ocean history files.

    Args:
        outdir: Directory containing the history files.
        file_stems: List of output file name stems.
    """
    outdir = Path(outdir)
    for stem in file_stems:
        path = outdir / f"{stem}.nc"
        if not path.exists():
            continue
        with nc.Dataset(path, "a") as ds:
            ds.grid_type = "tripolar"
            ds.associated_files = "area: ocean_mosaic.nc"
            for vname, var in ds.variables.items():
                if vname not in (
                    "time",
                    "time_bnds",
                    "average_T1",
                    "average_T2",
                    "average_DT",
                ):
                    var.interp_method = "conserve_order1"
