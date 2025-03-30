import numpy as np

from pyfms import DiagManager, pyFMS, pyFMS_mpp_domains


def test_send_data():

    NX = 8
    NY = 8
    NZ = 2

    domain_id = 0
    calendar_type = 4

    var2_shape = np.array([NX, NY], dtype=np.int32)
    var2 = np.empty(shape=NX * NY, dtype=np.float32)

    var3_shape = np.array([NX, NY, NZ], dtype=np.int32)
    var3 = np.empty(shape=NX * NY * NZ, dtype=np.float32)

    ijk = 0
    for i in range(NX):
        for j in range(NY):
            for k in range(NZ):
                var3[ijk] = i * 100 + j * 10 + k * 1
                ijk += 1

    ij = 0
    for i in range(NX):
        for j in range(NY):
            var2[ij] = i * 10.0 + j * 1.0
            ij += 1

    cfms_path = "./cFMS/libcFMS/.libs/libcFMS.so"

    pyfms = pyFMS(cFMS_path=cfms_path, calendar_type=calendar_type)
    mpp_domains = pyFMS_mpp_domains(cFMS=pyfms.cFMS)

    global_indices = [0, (NX - 1), 0, (NY - 1)]
    layout = [1, 1]
    io_layout = [1, 1]

    mpp_domains.define_domains(
        domain_id=domain_id,
        global_indices=global_indices,
        layout=layout,
    )
    mpp_domains.define_io_domain(
        domain_id=domain_id,
        io_layout=io_layout,
    )

    """
    diag manager init
    """

    diag_manager = DiagManager(clibFMS=pyfms.cFMS)
    diag_manager.init(diag_model_subset=diag_manager.DIAG_ALL)

    mpp_domains.set_current_domain(domain_id=domain_id)

    """
    diag axis init x
    """
    x = np.arange(NX, dtype=np.float64)

    for i in range(NX):
        x[i] = i

    id_x = diag_manager.axis_init(
        name="x",
        axis_data=x,
        units="point_E",
        cart_name="x",
        long_name="point_E",
        set_name="atm",
    )

    """
    diag axis init y
    """
    y = np.arange(NY, dtype=np.float64)

    for j in range(NY):
        y[j] = j

    id_y = diag_manager.axis_init(
        name="y",
        axis_data=y,
        units="point_N",
        cart_name="y",
        long_name="point_N",
        set_name="atm",
    )

    """
    diag axis init z
    """

    z = np.arange(NZ, dtype=np.float64)

    for k in range(NZ):
        z[k] = k

    id_z = diag_manager.axis_init(
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

    axes_3d = np.array([id_x, id_y, id_z, 0, 0], dtype=np.int32)
    range_3d = np.array([-1000.0, 1000.0], dtype=np.float32)

    diag_manager.set_field_init_time(
        year=2,
        month=1,
        day=1,
        hour=1,
        minute=1,
        second=1,
    )

    id_var3 = diag_manager.register_field_array(
        module_name="atm_mod",
        field_name="var_3d",
        axes=axes_3d,
        long_name="Var in a lon/lat domain",
        units="muntin",
        missing_value=-99.99,
        range=range_3d,
    )

    diag_manager.set_field_timestep(
        diag_field_id=id_var3, dseconds=60 * 60, ddays=0, dticks=0
    )

    """
    register diag_field var 2
    """

    axes_2d = np.array([id_x, id_y, 0, 0, 0], dtype=np.int32)
    range_2d = np.array([-1000.0, 1000.0], dtype=np.float32)

    diag_manager.set_field_init_time(
        year=2,
        month=1,
        day=1,
        hour=1,
        minute=1,
        second=1,
    )

    id_var2 = diag_manager.register_field_array(
        module_name="atm_mod",
        field_name="var_2d",
        axes=axes_2d,
        long_name="Var in a lon/lat domain",
        units="muntin",
        missing_value=-99.99,
        range=range_2d,
    )

    diag_manager.set_field_timestep(
        diag_field_id=id_var2,
        dseconds=60 * 60,
        ddays=0,
        dticks=0,
    )

    """
    diag set time end
    """

    diag_manager.set_time_end(
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

    diag_manager.send_data(
        diag_field_id=id_var3,
        field_shape=var3_shape,
        field=var3,
    )

    ntime = 24
    for itime in range(ntime):
        ijk = 0
        for i in range(NX):
            for j in range(NY):
                for k in range(NZ):
                    var3[ijk] = -1.0 * var3[ijk]
                    ijk += 1
        diag_manager.advance_field_time(diag_field_id=id_var3)
        diag_manager.send_data(
            diag_field_id=id_var3,
            field_shape=var3_shape,
            field=var3,
        )
        diag_manager.send_complete(diag_field_id=id_var3)

        var2 = -var2

        diag_manager.advance_field_time(diag_field_id=id_var2)
        diag_manager.send_data(
            diag_field_id=id_var2,
            field_shape=var2_shape,
            field=var2,
        )
        diag_manager.send_complete(diag_field_id=id_var2)

    diag_manager.end()

    pyfms.pyfms_end()


if __name__ == "__main__":
    test_send_data()
