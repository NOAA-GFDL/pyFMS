# generate-history

Generates structurally faithful FMS raw history NetCDF files using the pyfms
diag manager. Useful for creating test fixtures for climate data processing
pipelines without needing a full model run.

`generate-history` is installed as a command when pyfms is pip-installed.

---

## Usage

Write a `diag_table.yaml` in the standard FMS format, then run one of:

```tcsh
# Regular rectangular grid
generate-history diag_table.yaml \
    --nx 96 --ny 96 [--nz 65] \
    --calendar noleap \
    --nsteps 720 \
    --output-dir ./output

# Cubed-sphere atmosphere (C96, 6 tiles)
mpirun -n 6 generate-history diag_table.yaml \
    --grid-type cubed-sphere --ntile 96 [--nz 65] \
    --calendar noleap \
    --nsteps 720 \
    --output-dir ./output

# Tripolar ocean
generate-history diag_table.yaml \
    --grid-type tripolar --nx 1440 --ny 1080 [--nz 75] \
    --calendar noleap \
    --nsteps 720 \
    --q-vars uo,vo \
    --output-dir ./output
```

### All options

| Option | Required | Description |
|---|---|---|
| `diag_table.yaml` | yes | Path to your diag_table.yaml |
| `--grid-type` | no | `regular` (default), `cubed-sphere`, or `tripolar` |
| `--nx`, `--ny` | for regular/tripolar | Horizontal grid dimensions |
| `--ntile` | for cubed-sphere | Tile size (e.g. 96 for C96, 48 for C48) |
| `--nz N` | no | Vertical levels; omit or 0 for all-2D output |
| `--calendar` | no | `noleap` (default), `julian`, `gregorian`, `thirty_day` |
| `--nsteps` | yes | Number of 1-hour steps to simulate |
| `--output-dir` | no | Where to write output (default: `./output`) |
| `--seed` | no | Random seed for reproducible data (default: 0) |
| `--q-vars` | no | Comma-separated var_names on the q-grid (tripolar only) |

The internal model timestep is fixed at 1 hour. Output frequency is driven by
the `freq` field in the diag_table.yaml. Data values are random but reproducible.

---

## Grid types

### `regular` (default)
Standard rectangular grid. Produces a single output file per diag_files entry.

### `cubed-sphere`
Six-tile gnomonic equal-angle cubed-sphere (GFDL FMS convention). Requires
`mpirun -n 6`. Produces:
- `{file_name}.tile1.nc` … `{file_name}.tile6.nc` — history files
- `C{ntile}_mosaic.nc` — FMS mosaic descriptor (for fregrid)
- `C{ntile}_grid.tile{1..6}.nc` — per-tile supergrid files (lat/lon/area/dx/dy)
- `C{ntile}_scrip.nc` — combined SCRIP file (for ESMF/esmpy)

### `tripolar`
Single-tile tripolar ocean grid with h-point (tracer) and q-point (velocity)
axes. Produces:
- `{file_name}.nc` — history file with `xh`, `yh`, `xq`, `yq` dimensions
- `ocean_mosaic.nc` — FMS mosaic descriptor (for fregrid)
- `ocean_hgrid.nc` — supergrid file (lat/lon/area/dx/dy)
- `ocean_scrip.nc` — SCRIP file (for ESMF/esmpy)

Variables named in `--q-vars` are placed on the q-grid; all others default
to the h-grid.

---

## diag_table.yaml format

```yaml
title: my_test
base_date: 2000 1 1 0 0 0

diag_files:
- file_name: atmos_month
  freq: 1 months
  time_units: hours
  unlimdim: time
  varlist:
  - module: atm_mod
    var_name: tas
    reduction: average
    kind: r4
    output_name: tas
  - module: atm_mod
    var_name: ua
    reduction: average
    kind: r4
    output_name: ua
```

`base_date` sets the simulation start time (year month day hour minute second).
`--nsteps 720` with a 1-hour internal step covers 30 days from that start time.

---

## Checking output

```python
import xarray as xr

# Regular or tripolar
ds = xr.open_dataset("output/atmos_month.nc")
print(ds)

# Cubed-sphere (one tile)
ds = xr.open_dataset("output/atmos_month.tile1.nc")
print(ds)

# Grid spec
ds = xr.open_dataset("output/C96_mosaic.nc")
```

---

## Troubleshooting

**No output files produced**  
→ The simulation must run long enough to cross at least one output boundary.
Check that `--nsteps` × 1 hour exceeds the `freq` of every file in the diag_table.

**`import pyfms` fails**  
→ The pyfms venv is not active, or the required environment modules (gcc, mpich,
netcdf-c, netcdf-fortran) were not loaded. Load modules and activate the venv
before running.

**cubed-sphere: `RuntimeError: requires exactly 6 MPI ranks`**  
→ Run with `mpirun -n 6 generate-history ...`

**cubed-sphere: no `.tileN.nc` files appear**  
→ The cubic mosaic domain integration with diag_manager may need verification.
Check that `define_cubic_mosaic` is set as the current domain before calling
`diag_manager.init`.
