import os

import numpy as np

import pyfms


def test_send_data():

    nx = 8
    ny = 8
    nz = 2

    var2 = np.empty(shape=(nx, ny), dtype=np.float32)
    for i in range(nx):
        for j in range(ny):
            var2[i][j] = i * 10.0 + j * 1.0

    var3 = np.empty(shape=(nx, ny, nz), dtype=np.float32)
    for i in range(nx):
        for j in range(ny):
            for k in range(nz):
                var3[i][j][k] = i * 100 + j * 10 + k * 1

    pyfms.fms.init(calendar_type=pyfms.fms.NOLEAP)

    global_indices = [0, (nx - 1), 0, (ny - 1)]
    layout = [1, 1]
    io_layout = [1, 1]

    domain = pyfms.mpp_domains.define_domains(
        global_indices=global_indices,
        layout=layout,
    )
    pyfms.mpp_domains.define_io_domain(
        domain_id=domain.domain_id,
        io_layout=io_layout,
    )

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

    """
    register diag field var3
    """

    pyfms.diag_manager.set_field_init_time(
        year=2,
        month=1,
        day=1,
        hour=1,
        minute=1,
        second=1,
    )

    id_var3 = pyfms.diag_manager.register_field_array(
        module_name="atm_mod",
        field_name="var_3d",
        dtype="float32",
        axes=[id_x, id_y, id_z],
        long_name="Var in a lon/lat domain",
        units="muntin",
        missing_value=-99.99,
        range_data=[-1000.0, 1000.0],
    )

    pyfms.diag_manager.set_field_timestep(
        diag_field_id=id_var3, dseconds=60 * 60, ddays=0, dticks=0
    )

    """
    register diag_field var 2
    """

    pyfms.diag_manager.set_field_init_time(
        year=2,
        month=1,
        day=1,
        hour=1,
        minute=1,
        second=1,
    )

    id_var2 = pyfms.diag_manager.register_field_array(
        module_name="atm_mod",
        field_name="var_2d",
        dtype="float32",
        axes=[id_x, id_y],
        long_name="Var in a lon/lat domain",
        units="muntin",
        missing_value=-99.99,
        range_data=np.array([-1000.0, 1000.0], dtype=np.float32),
    )

    pyfms.diag_manager.set_field_timestep(
        diag_field_id=id_var2,
        dseconds=60 * 60,
        ddays=0,
        dticks=0,
    )

    """
    diag set time end
    """

    pyfms.diag_manager.set_time_end(
        year=2,
        month=1,
        day=2,
        hour=1,
        minute=1,
        second=1,
        tick=0,
    )

    """
    send data
    """

    ntime = 24
    for itime in range(ntime):

        var3 = -var3

        pyfms.diag_manager.advance_field_time(diag_field_id=id_var3)
        success = pyfms.diag_manager.send_data(
            diag_field_id=id_var3,
            field=var3,
        )
        assert success
        pyfms.diag_manager.send_complete(diag_field_id=id_var3)

        var2 = -var2

        pyfms.diag_manager.advance_field_time(diag_field_id=id_var2)
        success = pyfms.diag_manager.send_data(
            diag_field_id=id_var2,
            field=var2,
        )
        assert success
        pyfms.diag_manager.send_complete(diag_field_id=id_var2)

    pyfms.diag_manager.end()
    pyfms.fms.end()

    assert os.path.isfile("test_send_data.nc")
    os.remove("test_send_data.nc")


if __name__ == "__main__":
    test_send_data()
