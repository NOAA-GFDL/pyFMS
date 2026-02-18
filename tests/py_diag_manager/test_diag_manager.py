import os
from datetime import datetime, timedelta

import numpy as np
import xarray as xr

import pyfms


def test_send_data():

    nx = 32
    ny = 32
    nz = 2

    pyfms.fms.init(calendar_type=pyfms.fms.NOLEAP)

    pe = pyfms.mpp.pe()
    npes = pyfms.mpp.npes()

    global_indices = [0, nx-1, 0, ny-1]
    layout = [1, npes]
    io_layout = [1, 1]

    domain = pyfms.mpp_domains.define_domains(
        global_indices=global_indices,
        layout=layout,
    )
    pyfms.mpp_domains.define_io_domain(
        domain_id=domain.domain_id,
        io_layout=io_layout,
    )

    var2_global = np.empty(shape=(nx,ny), dtype=np.float32)
    var3_global = np.empty(shape=(nx,ny,nz), dtype=np.float32)
    for i in range(nx):
        for j in range(ny):
            var2_global[i][j] = i * 10.0 + j * 1.0
    for i in range(nx):
        for j in range(ny):
            for k in range(nz):
                var3_global[i][j][k] = i * 100 + j * 10 + k * 1

    # fortran includes the last element in array slices (ie array[isc:iec] includes array[iec])
    # python does not, so need to increment.
    var2 = var2_global[domain.isc:domain.iec+1,domain.jsc:domain.jec+1]
    var3 = var3_global[domain.isc:domain.iec+1,domain.jsc:domain.jec+1,:]

    """
    diag manager init
    """
    pyfms.diag_manager.init(diag_model_subset=pyfms.diag_manager.DIAG_ALL)
    pyfms.mpp_domains.set_current_domain(domain_id=domain.domain_id)

    """
    diag axis init x
    """
    x = np.arange(nx, dtype=np.float64)

    id_x = pyfms.diag_manager.axis_init(
        name="x",
        axis_data=x,
        units="point_E",
        cart_name="x",
        domain_id=domain.domain_id,
        long_name="point_E",
        set_name="atm",
    )

    """
    diag axis init y
    """
    y = np.arange(ny, dtype=np.float64)

    id_y = pyfms.diag_manager.axis_init(
        name="y",
        axis_data=y,
        units="point_N",
        cart_name="y",
        domain_id=domain.domain_id,
        long_name="point_N",
        set_name="atm",
    )

    """
    diag axis init z
    """

    z = np.arange(nz, dtype=np.float64)

    id_z = pyfms.diag_manager.axis_init(
        name="z",
        axis_data=z,
        units="point_Z",
        cart_name="z",
        long_name="point_Z",
        set_name="atm",
        not_xy=True,
    )
    print("axes are registered")

    """
    set up our start/end times and timestep
    """
    start_time = datetime(2, 1, 1, 1, 1, 1)
    timestep = timedelta(seconds=3600)
    ntime = 8
    end_time = start_time + (timestep * ntime)

    """
    register diag field var3
    """

    id_var3 = pyfms.diag_manager.register_field_array(
        module_name="atm_mod",
        field_name="var_3d",
        dtype="float32",
        axes=[id_x, id_y, id_z],
        long_name="Var in a lon/lat domain",
        units="muntin",
        missing_value=-99.99,
        range_data=[-1000.0, 1000.0],
        init_time=start_time,
    )

    """
    register diag_field var 2
    """
    id_var2 = pyfms.diag_manager.register_field_array(
        module_name="atm_mod",
        field_name="var_2d",
        dtype="float32",
        axes=[id_x, id_y],
        long_name="Var in a lon/lat domain",
        units="muntin",
        missing_value=-99.99,
        range_data=np.array([-1000.0, 1000.0], dtype=np.float32),
        init_time=start_time,
    )
    print("fields are registered")

    """
    diag set time end
    """
    pyfms.diag_manager.set_time_end(end_time)

    """
    send data
    """
    curr_time = start_time
    do_send_data = True 
    for itime in range(ntime):
        curr_time = curr_time + timestep
        print(f"(not) sending data for time: {curr_time}")
        if do_send_data:

            success = pyfms.diag_manager.send_data(
                diag_field_id=id_var3,
                field=var3,
                time=curr_time,
            )
            assert success
            # skip this one for now
            success = pyfms.diag_manager.send_data(
                diag_field_id=id_var2,
                field=var2,
                time=curr_time,
            )
            assert success
        pyfms.diag_manager.send_complete(timestep)

    pyfms.diag_manager.end(end_time)
    pyfms.fms.end()

    """
    check our output is correct
    """
    if pyfms.mpp.pe() == pyfms.mpp.root_pe():
        assert os.path.isfile("test_send_data.nc")
        ds = xr.open_mfdataset("test_send_data.nc", decode_times=True)
        assert "var2_avg" in ds
        assert "var3_avg" in ds
        assert ds["var2_avg"].dims == ("time", "y", "x")
        assert ds["var3_avg"].dims == ("time", "z", "y", "x" )
        assert ds["time"].dims == ("time",)
        assert ds["time"].shape == (ntime,)
        for i in range(ntime):
            np.testing.assert_array_equal(ds["var2_avg"].values[i,:,:], np.transpose(var2_global))
            np.testing.assert_array_equal(ds["var3_avg"].values[i,:,:,:], np.transpose(var3_global))


if __name__ == "__main__":
    test_send_data()
