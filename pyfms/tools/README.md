# generate-history

Generates structurally faithful FMS raw history NetCDF files using the pyfms
diag manager. Useful for creating test fixtures for climate data processing
pipelines without needing a full model run.

`generate-history` is installed as a command when pyfms is pip-installed.

---

## Usage

Write a `diag_table.yaml` in the standard FMS format, then run:

```tcsh
generate-history diag_table.yaml \
    --nx 96 --ny 96 \
    --calendar noleap \
    --nsteps 720 \
    --output-dir ./output
```

| Option | Required | Description |
|---|---|---|
| `diag_table.yaml` | yes | Path to your diag_table.yaml |
| `--nx`, `--ny` | yes | Horizontal grid dimensions |
| `--nz N` | no | Vertical levels; omit or 0 for all-2d output |
| `--calendar` | no | `noleap` (default), `julian`, `gregorian`, `thirty_day` (case-insensitive) |
| `--nsteps` | yes | Number of 1-hour steps to simulate (e.g. 720 = 30 days, 8760 = 1 year) |
| `--output-dir` | no | Where to write output (default: `./output`) |
| `--seed` | no | Random seed for reproducible output (default: 0) |

The internal model timestep is fixed at 1 hour. Output frequency is driven by
the `freq` field in the diag_table.yaml. Data values are random but reproducible
across runs with the same `--seed`.

If `--nz` is absent or 0, all variables are written as 2d (y, x).
If `--nz N`, all variables are written as 3d (z, y, x).

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
`--nsteps 720` with a 1-hour internal step covers 30 days from that start time,
enough to trigger one monthly output record.

---

## Checking output

```python
import xarray as xr
ds = xr.open_dataset("output/atmos_month.nc")
print(ds)
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
