import os

import numpy as np
import xarray as xr
import yaml


def test_write_input_files():
    data_table = yaml.load(
        """
        data_table:
        - grid_name: OCN
          fieldname_in_model: runoff_scalar
          override_file:
          - fieldname_in_file: runoff
            file_name: ./INPUT/scalar.nc
            interp_method: bilinear
          factor: 1.0
        - grid_name: OCN
          fieldname_in_model: runoff_2d
          override_file:
          - fieldname_in_file: runoff
            file_name: ./INPUT/array_2d.nc
            interp_method: bilinear
          factor: 1.0
        - grid_name: OCN
          fieldname_in_model: runoff_3d
          override_file:
          - fieldname_in_file: runoff
            file_name: ./INPUT/array_3d.nc
            interp_method: bilinear
          factor: 1.0
        """,
        Loader=yaml.Loader,
    )

    data_table_yaml_file = open("data_table.yaml", "w")
    yaml.dump(data_table, data_table_yaml_file, sort_keys=False)
    data_table_yaml_file.close()

    input_nml = """
&data_override_nml
use_data_table_yaml = .True.
/
    """
    input_nml_file = open("input.nml", "w")
    input_nml_file.write(input_nml)
    input_nml_file.close()


def test_write_grid_files():

    try:
        os.mkdir("./INPUT")
    except FileExistsError:
        pass

    ocn_mosaic = xr.DataArray(data="ocean_mosaic.nc".encode())
    xr.Dataset(data_vars=dict(ocn_mosaic_file=ocn_mosaic)).to_netcdf(
        "./INPUT/grid_spec.nc"
    )

    ocean_hgrid = xr.DataArray(data="ocean_hgrid.nc".encode()).expand_dims(
        dim=["ntiles"]
    )
    xr.Dataset(data_vars=dict(gridfiles=ocean_hgrid)).to_netcdf(
        "./INPUT/ocean_mosaic.nc"
    )

    nxp, nyp = 721, 361
    x = np.array([0.5 * i for i in range(nxp)] * nyp, dtype=np.float32).reshape(
        (nyp, nxp)
    )
    y = np.array(
        [[-90.0 - 0.5 * i] * nxp for i in range(nyp)], dtype=np.float32
    ).reshape((nyp, nxp))
    area = np.ones((nyp - 1, nxp - 1), dtype=np.float32)

    xr.Dataset(
        data_vars=dict(
            x=xr.DataArray(x, dims=["nyp", "nxp"]),
            y=xr.DataArray(y, dims=["nyp", "nxp"]),
            area=xr.DataArray(area, dims=["ny", "nx"]),
        )
    ).to_netcdf(
        "./INPUT/ocean_hgrid.nc",
    )


def test_write_scalar_file():

    runoff = xr.DataArray(np.arange(1, 11, 1, dtype=np.float64), dims=["time"])
    time = xr.DataArray(
        data=np.arange(1.0, 11.0, 1.0, dtype=np.float64),
        dims=["time"],
        attrs={"units": "days since 0001-01-01 00:00:00", "calendar": "noleap"},
    )

    xr.Dataset(data_vars=dict(time=time, runoff=runoff)).to_netcdf(
        "./INPUT/scalar.nc", unlimited_dims="time"
    )


def test_write_2d_file():

    nx, ny, ntime = 361, 179, 11
    x = xr.DataArray(np.arange(0, 361, 1, dtype=np.float64), dims=["x"])
    y = xr.DataArray(np.arange(-89, 90, 1, dtype=np.float64), dims=["y"])

    time = xr.DataArray(
        data=np.arange(1, ntime, 1.0, dtype=np.float64),
        dims=["time"],
        attrs={"units": "days since 0001-01-01 00:00:00", "calendar": "noleap"},
    )

    runoff_data = np.array(
        [[100 * (itime + 1)] * nx * ny for itime in range(ntime - 1)], dtype=np.float64
    ).reshape((ntime - 1, ny, nx))
    runoff = xr.DataArray(runoff_data, dims=["time", "y", "x"])

    xr.Dataset(data_vars=dict(x=x, y=y, time=time, runoff=runoff)).to_netcdf(
        "./INPUT/array_2d.nc", unlimited_dims="time"
    )


def test_write_3d_file():

    nx, ny, nz, ntime = 361, 179, 5, 11
    x = xr.DataArray(np.arange(0, 361, 1, dtype=np.float64), dims=["x"])
    y = xr.DataArray(np.arange(-89, 90, 1, dtype=np.float64), dims=["y"])
    z = xr.DataArray(np.arange(1, nz + 1, 1, dtype=np.float64), dims=["z"])

    time = xr.DataArray(
        data=np.arange(1, ntime, 1.0, dtype=np.float64),
        dims=["time"],
        attrs={"units": "days since 0001-01-01 00:00:00", "calendar": "noleap"},
    )

    runoff_list = [
        [[100 * (itime + 1) + z + 1] * nx * ny for z in range(nz)]
        for itime in range(ntime - 1)
    ]
    runoff_data = np.array(runoff_list, dtype=np.float64).reshape(
        (ntime - 1, nz, ny, nx)
    )
    runoff = xr.DataArray(runoff_data, dims=["time", "z", "y", "x"])

    xr.Dataset(data_vars=dict(x=x, y=y, z=z, time=time, runoff=runoff)).to_netcdf(
        "./INPUT/array_3d.nc", unlimited_dims="time"
    )
