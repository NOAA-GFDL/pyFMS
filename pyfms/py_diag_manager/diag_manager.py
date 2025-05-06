from ctypes import CDLL, c_bool, c_int

import numpy as np
from numpy.typing import NDArray

from pyfms.utils.data_handling import (
    set_Cchar,
    setarray_Cdouble,
    setarray_Cfloat,
    setarray_Cint32,
    setscalar_Cbool,
    setscalar_Cdouble,
    setscalar_Cfloat,
    setscalar_Cint32,
)


_libpath: str = None
_lib: type[CDLL] = None

DIAG_ALL: int = None
DIAG_OCEAN: int = None
DIAG_OTHER: int = None


def setlib(libpath: str, lib: type[CDLL]):

    """
    Sets _libpath and _lib module variables associated
    with the loaded cFMS library.  This function is
    to be used internally by the cfms module
    """

    global _libpath, _lib

    _libpath = libpath
    _lib = lib


def constants_init():

    """
    Retrieves and assigns diag_manager related parameters
    from FMS
    """

    global DIAG_OTHER, DIAG_OCEAN, DIAG_ALL

    def get_constant(variable):
        return int(c_int.in_dll(_lib, variable).value)

    DIAG_OTHER = get_constant("DIAG_OTHER")
    DIAG_OCEAN = get_constant("DIAG_OCEAN")
    DIAG_ALL = get_constant("DIAG_ALL")


def end():

    """
    This function must be called in order to flush out
    the diagnostic buffers and properly close
    the diagnostic files
    """

    _cfms_diag_end = _lib.cFMS_diag_end
    _cfms_diag_end.restype = None
    _cfms_diag_end()


def init(
    diag_model_subset: int = None,
    time_init: NDArray = None,
) -> str:

    """
    Initializes diag_manager

    pyfms is initialized to use the latest cFMS and FMS.  Thus, diag_manager
    will only work with diag_table.yaml.  Users should ensure that
    (1) diag_table.yaml exists, and
    (2) use_modern_diag = .True. for &diag_manager_nml in input.nml

    The above criteria may not be applicable if users have specified to
    load an alternative cFMS and FMS library during cfms.init() 

    See https://github.com/NOAA-GFDL/FMScoupler/blob/main/full/full_coupler_mod.F90
    for diag_model_subset specification
    """

    _cfms_diag_init = _lib.cFMS_diag_init

    diag_model_subset_c, diag_model_subset_t = setscalar_Cint32(diag_model_subset)
    time_init_p, time_init_t = setarray_Cint32(time_init)
    err_msg_c, err_msg_t = set_Cchar(" ")

    _cfms_diag_init.argtypes = [
        diag_model_subset_t,
        time_init_t,
        err_msg_t,
    ]
    _cfms_diag_init.restype = None

    _cfms_diag_init(diag_model_subset_c, time_init_p, err_msg_c)

    return err_msg_c.value.decode("utf-8")


def send_complete(diag_field_id: int) -> str:

    _cfms_diag_send_complete = _lib.cFMS_diag_send_complete

    diag_field_id_c, diag_field_id_t = setscalar_Cint32(diag_field_id)
    err_msg_c, err_msg_t = set_Cchar(" ")

    _cfms_diag_send_complete.argtypes = [diag_field_id_t, err_msg_t]
    _cfms_diag_send_complete.restype = None

    _cfms_diag_send_complete(diag_field_id_c, err_msg_c)

    return err_msg_c.value.decode("utf-8")


def set_field_init_time(
    year: int,
    month: int,
    day: int,
    hour: int,
    minute: int,
    second: int = None,
    tick: int = None,
) -> str:

    """
    Sets the time type in cFMS that represents the
    field initial time.  This time is used when registering
    a diag field
    """

    _cfms_diag_set_field_init_time = _lib.cFMS_diag_set_field_init_time

    year_c, year_t = setscalar_Cint32(year)
    month_c, month_t = setscalar_Cint32(month)
    day_c, day_t = setscalar_Cint32(day)
    hour_c, hour_t = setscalar_Cint32(hour)
    minute_c, minute_t = setscalar_Cint32(minute)
    second_c, second_t = setscalar_Cint32(second)
    tick_c, tick_t = setscalar_Cint32(tick)
    err_msg_c, err_msg_t = set_Cchar(" ")

    _cfms_diag_set_field_init_time.argtypes = [
        year_t,
        month_t,
        day_t,
        hour_t,
        minute_t,
        second_t,
        tick_t,
        err_msg_t,
    ]
    _cfms_diag_set_field_init_time.restype = None

    _cfms_diag_set_field_init_time(
        year_c, month_c, day_c, hour_c, minute_c, second_c, tick_c, err_msg_c
    )

    return err_msg_c.value.decode("utf-8")


def set_field_timestep(
    diag_field_id: int,
    dseconds: int,
    ddays: int = None,
    dticks: int = None,
) -> str:

    """
    Sets the timestep between each send_data
    The timestep is saved as a time type in cFMS and is
    used to advance field time
    """

    _cfms_diag_set_field_timestep = _lib.cFMS_diag_set_field_timestep

    diag_field_id_c, diag_field_id_t = setscalar_Cint32(diag_field_id)
    dseconds_c, dseconds_t = setscalar_Cint32(dseconds)
    ddays_c, ddays_t = setscalar_Cint32(ddays)
    dticks_c, dticks_t = setscalar_Cint32(dticks)
    err_msg_c, err_msg_t = set_Cchar(" ")

    _cfms_diag_set_field_timestep.argtypes = [
        diag_field_id_t,
        dseconds_t,
        ddays_t,
        dticks_t,
        err_msg_t,
    ]
    _cfms_diag_set_field_timestep.restype = None

    _cfms_diag_set_field_timestep(
        diag_field_id_c, dseconds_c, ddays_c, dticks_c, err_msg_c
    )

    return err_msg_c.value.decode("utf-8")


def advance_field_time(diag_field_id: int):

    """
    Updates the current field time by advancing
    the current field time with the field timestep
    set with diag_manager.set_field_timestep
    """

    _cfms_diag_advance_field_time = _lib.cFMS_diag_advance_field_time

    diag_field_id_c, diag_field_id_t = setscalar_Cint32(diag_field_id)

    _cfms_diag_advance_field_time.argtypes = [diag_field_id_t]
    _cfms_diag_advance_field_time.restype = None

    _cfms_diag_advance_field_time(diag_field_id_c)


def set_time_end(
    year: int = None,
    month: int = None,
    day: int = None,
    hour: int = None,
    minute: int = None,
    second: int = None,
    tick: int = None,
    err_msg: str = None,
):

    """
    Sets the time type representing the field end time
    in cFMS.  This time must be set before calling
    diag_manager.end()
    """

    if err_msg is not None:
        err_msg = err_msg[:128]

    _cfms_set_time_end = _lib.cFMS_diag_set_time_end

    year_c, year_t = setscalar_Cint32(year)
    month_c, month_t = setscalar_Cint32(month)
    day_c, day_t = setscalar_Cint32(day)
    hour_c, hour_t = setscalar_Cint32(hour)
    minute_c, minute_t = setscalar_Cint32(minute)
    second_c, second_t = setscalar_Cint32(second)
    tick_c, tick_t = setscalar_Cint32(tick)
    err_msg_c, err_msg_t = set_Cchar(err_msg)

    _cfms_set_time_end.argtypes = [
        year_t,
        month_t,
        day_t,
        hour_t,
        minute_t,
        second_t,
        tick_t,
        err_msg_t,
    ]
    _cfms_set_time_end.restype = None

    _cfms_set_time_end(
        year_c,
        month_c,
        day_c,
        hour_c,
        minute_c,
        second_c,
        tick_c,
        err_msg_c,
    )


def axis_init(
    name: str,
    axis_data: NDArray,
    units: str,
    cart_name: str,
    domain_id: int = None,
    long_name: str = None,
    set_name: str = None,
    direction: int = None,
    edges: int = None,
    aux: str = None,
    req: str = None,
    tile_count: int = None,
    domain_position: int = None,
    not_xy: bool = None,
) -> int:

    """
    Initializes the diag_axis
    not_xy = True must be specified when initializing an axis
    that is not a horizontal x-y axis
    """

    long_name = long_name[:64]
    set_name = set_name[:64]

    name_c, name_t = set_Cchar(name)
    naxis_data_c, naxis_data_t = setscalar_Cint32(axis_data.size)
    units_c, units_t = set_Cchar(units)
    cart_name_c, cart_name_t = set_Cchar(cart_name)
    domain_id_c, domain_id_t = setscalar_Cint32(domain_id)
    long_name_c, long_name_t = set_Cchar(long_name)
    set_name_c, set_name_t = set_Cchar(set_name)
    direction_c, direction_t = setscalar_Cint32(direction)
    edges_c, edges_t = setscalar_Cint32(edges)
    aux_c, aux_t = set_Cchar(aux)
    req_c, req_t = set_Cchar(req)
    tile_count_c, tile_count_t = setscalar_Cint32(tile_count)
    domain_position_c, domain_position_t = setscalar_Cint32(domain_position)
    not_xy_c, not_xy_t = setscalar_Cbool(not_xy)

    if axis_data.dtype == np.float64:
        _cfms_diag_axis_init_ = _lib.cFMS_diag_axis_init_cdouble
        axis_data_p, axis_data_t = setarray_Cdouble(axis_data)
    elif axis_data.dtype == np.float32:
        _cfms_diag_axis_init_ = _lib.cFMS_diag_axis_init_cfloat
        axis_data_p, axis_data_t = setarray_Cfloat(axis_data)
    else:
        raise RuntimeError("diag_axis_init datatype not supported")

    _cfms_diag_axis_init_.argtypes = [
        name_t,
        naxis_data_t,
        axis_data_t,
        units_t,
        cart_name_t,
        domain_id_t,
        long_name_t,
        direction_t,
        set_name_t,
        edges_t,
        aux_t,
        req_t,
        tile_count_t,
        domain_position_t,
        not_xy_t,
    ]
    _cfms_diag_axis_init_.restype = c_int

    return _cfms_diag_axis_init_(
        name_c,
        naxis_data_c,
        axis_data_p,
        units_c,
        cart_name_c,
        domain_id_c,
        long_name_c,
        direction_c,
        set_name_c,
        edges_c,
        aux_c,
        req_c,
        tile_count_c,
        domain_position_c,
        not_xy_c,
    )


def register_field_array(
    module_name: str,
    field_name: str,
    datatype,
    axes: list[int] = None,
    long_name: str = None,
    units: str = None,
    missing_value: int = None,
    range_data: NDArray = None,
    mask_variant: bool = None,
    standard_name: str = None,
    verbose: bool = None,
    do_not_log: bool = None,
    interp_method: str = None,
    tile_count: int = None,
    area: int = None,
    volume: int = None,
    realm: str = None,
    multiple_send_data: bool = None,
) -> int:

    """
    Registers multi-dimensional fields
    The field initial time must be set with
    diag_manager.set_field_init_time before calling
    this method
    """

    module_name = module_name[:64]
    field_name = field_name[:64]
    if long_name is not None:
        long_name = long_name[:64]
    if units is not None:
        units = units[:64]
    if standard_name is not None:
        standard_name = standard_name[:64]
    if interp_method is not None:
        interp_method = interp_method[:64]
    if realm is not None:
        realm = realm[:64]

    if axes is not None:
        if len(axes) < 5:
            for i in range(5 - len(axes)):
                axes.append(0)
            axes_arr = np.array(axes, dtype=np.int32)
        else:
            axes_arr = None

    module_name_c, module_name_t = set_Cchar(module_name)
    field_name_c, field_name_t = set_Cchar(field_name)
    axes_p, axes_t = setarray_Cint32(axes_arr)
    long_name_c, long_name_t = set_Cchar(long_name)
    units_c, units_t = set_Cchar(units)
    mask_variant_c, mask_variant_t = setscalar_Cbool(mask_variant)
    standard_name_c, standard_name_t = set_Cchar(standard_name)
    verbose_c, verbose_t = setscalar_Cbool(verbose)
    do_not_log_c, do_not_log_t = setscalar_Cbool(do_not_log)
    err_msg_c, err_msg_t = set_Cchar(" ")
    interp_method_c, interp_method_t = set_Cchar(interp_method)
    tile_count_c, tile_count_t = setscalar_Cint32(tile_count)
    area_c, area_t = setscalar_Cint32(area)
    volume_c, volume_t = setscalar_Cint32(volume)
    realm_c, realm_t = set_Cchar(realm)
    multiple_send_data_c, multiple_send_data_t = setscalar_Cbool(multiple_send_data)

    if datatype == np.int32:
        _cfms_register_diag_field_array_ = _lib.cFMS_register_diag_field_array_cint
        range_data_p, range_data_t = setarray_Cint32(range_data)
        missing_value_c, missing_value_t = setscalar_Cint32(missing_value)
    elif datatype == np.float64:
        _cfms_register_diag_field_array_ = _lib.cFMS_register_diag_field_array_cdouble
        range_data_p, range_data_t = setarray_Cdouble(range_data)
        missing_value_c, missing_value_t = setscalar_Cdouble(missing_value)
    elif datatype == np.float32:
        _cfms_register_diag_field_array_ = _lib.cFMS_register_diag_field_array_cfloat
        range_data_p, range_data_t = setarray_Cfloat(range_data)
        missing_value_c, missing_value_t = setscalar_Cfloat(missing_value)
    else:
        raise RuntimeError(
            "register diag field array range_data datatype not supported"
        )

    _cfms_register_diag_field_array_.argtypes = [
        module_name_t,
        field_name_t,
        axes_t,
        long_name_t,
        units_t,
        missing_value_t,
        range_data_t,
        mask_variant_t,
        standard_name_t,
        verbose_t,
        do_not_log_t,
        err_msg_t,
        interp_method_t,
        tile_count_t,
        area_t,
        volume_t,
        realm_t,
        multiple_send_data_t,
    ]
    _cfms_register_diag_field_array_.restype = c_int

    return _cfms_register_diag_field_array_(
        module_name_c,
        field_name_c,
        axes_p,
        long_name_c,
        units_c,
        missing_value_c,
        range_data_p,
        mask_variant_c,
        standard_name_c,
        verbose_c,
        do_not_log_c,
        err_msg_c,
        interp_method_c,
        tile_count_c,
        area_c,
        volume_c,
        realm_c,
        multiple_send_data_c,
    )


def register_field_scalar(
    module_name: str,
    field_name: str,
    datatype,
    long_name: str = None,
    units: str = None,
    standard_name: str = None,
    missing_value: int = None,
    range_data: NDArray = None,
    do_not_log: bool = None,
    area: int = None,
    volume: int = None,
    realm: str = None,
    multiple_send_data: bool = None,
) -> int:

    """
    Registers scalar fields
    The field initial time must be set with
    diag_manager.set_field_init_time before calling
    this method
    """

    module_name = module_name[:64]
    field_name = field_name[:64]
    if long_name is not None:
        long_name = long_name[:64]
    if units is not None:
        units = units[:64]
    if standard_name is not None:
        standard_name = standard_name[:64]
    if realm is not None:
        realm = realm[:64]

    module_name_c, module_name_t = set_Cchar(module_name)
    field_name_c, field_name_t = set_Cchar(field_name)
    long_name_c, long_name_t = set_Cchar(long_name)
    units_c, units_t = set_Cchar(units)
    standard_name_c, standard_name_t = set_Cchar(standard_name)
    do_not_log_c, do_not_log_t = setscalar_Cbool(do_not_log)
    err_msg_c, err_msg_t = set_Cchar(" ")
    area_c, area_t = setscalar_Cint32(area)
    volume_c, volume_t = setscalar_Cint32(volume)
    realm_c, realm_t = set_Cchar(realm)
    multiple_send_data_c, multiple_send_data_t = setscalar_Cbool(multiple_send_data)

    if datatype == np.int32:
        _cfms_register_diag_field_scalar_ = _lib.cFMS_register_diag_field_array_cint
        range_data_p, range_data_t = setarray_Cint32(range_data)
        missing_value_c, missing_value_t = setscalar_Cint32(missing_value)
    elif datatype == np.float64:
        _cfms_register_diag_field_scalar_ = _lib.cFMS_register_diag_field_array_cdouble
        range_data_p, range_data_t = setarray_Cdouble(range_data)
        missing_value_c, missing_value_t = setscalar_Cdouble(missing_value)
    elif datatype == np.float32:
        _cfms_register_diag_field_scalar_ = _lib.cFMS_register_diag_field_array_cfloat
        range_data_p, range_data_t = setarray_Cfloat(range_data)
        missing_value_c, missing_value_t = setscalar_Cfloat(missing_value)
    else:
        raise RuntimeError(
            "register diag field array range_data datatype not supported"
        )

    _cfms_register_diag_field_scalar_.argtypes = [
        module_name_t,
        field_name_t,
        long_name_t,
        units_t,
        standard_name_t,
        missing_value_t,
        range_data_t,
        do_not_log_t,
        err_msg_t,
        area_t,
        volume_t,
        realm_t,
        multiple_send_data_t,
    ]
    _cfms_register_diag_field_scalar_.restype = c_int

    return _cfms_register_diag_field_scalar_(
        module_name_c,
        field_name_c,
        long_name_c,
        units_c,
        standard_name_c,
        missing_value_c,
        range_data_p,
        do_not_log_c,
        err_msg_c,
        area_c,
        volume_c,
        realm_c,
        multiple_send_data_c,
    )


def send_data(
    diag_field_id: int,
    field_shape: list[int],
    field: NDArray,
) -> bool:

    """
    Send field data to diag_manager that will be outputted to a diagnostic file
    The users should set the field time by advancing current time with
    the timestep that has been set with diag_manager.set_field_timestep

    Currently, field data only on the compute domain is supported.
    """

    diag_field_id_c, diag_field_id_t = setscalar_Cint32(diag_field_id)
    field_shape_arr = np.array(field_shape, dtype=np.int32)
    field_shape_p, field_shape_t = setarray_Cint32(field_shape_arr)
    err_msg_c, err_msg_t = set_Cchar(" ")

    if field_shape_arr.size == 2:
        if field.dtype == np.int32:
            _cfms_diag_send_data_ = _lib.cFMS_diag_send_data_2d_cint
            field_p, field_t = setarray_Cint32(field)
        elif field.dtype == np.float64:
            _cfms_diag_send_data_ = _lib.cFMS_diag_send_data_2d_cdouble
            field_p, field_t = setarray_Cdouble(field)
        elif field.dtype == np.float32:
            _cfms_diag_send_data_ = _lib.cFMS_diag_send_data_2d_cfloat
            field_p, field_t = setarray_Cfloat(field)
        else:
            raise RuntimeError(f"diag_send_data {field.dtype} unsupported")
    elif field_shape_arr.size == 3:
        if field.dtype == np.int32:
            _cfms_diag_send_data_ = _lib.cFMS_diag_send_data_3d_cint
            field_p, field_t = setarray_Cint32(field)
        elif field.dtype == np.float64:
            _cfms_diag_send_data_ = _lib.cFMS_diag_send_data_3d_cdouble
            field_p, field_t = setarray_Cdouble(field)
        elif field.dtype == np.float32:
            _cfms_diag_send_data_ = _lib.cFMS_diag_send_data_3d_cfloat
            field_p, field_t = setarray_Cfloat(field)
        else:
            raise RuntimeError(f"diag_send_data {field.dtype} unsupported")
    elif field_shape_arr.size == 4:
        if field.dtype == np.int32:
            _cfms_diag_send_data_ = _lib.cFMS_diag_send_data_4d_cint
            field_p, field_t = setarray_Cint32(field)
        elif field.dtype == np.float64:
            _cfms_diag_send_data_ = _lib.cFMS_diag_send_data_4d_cdouble
            field_p, field_t = setarray_Cdouble(field)
        elif field.dtype == np.float32:
            _cfms_diag_send_data_ = _lib.cFMS_diag_send_data_4d_cfloat
            field_p, field_t = setarray_Cfloat(field)
        else:
            raise RuntimeError(f"diag_send_data {field.dtype} unsupported")
    elif field_shape_arr.size == 5:
        if field.dtype == np.int32:
            _cfms_diag_send_data_ = _lib.cFMS_diag_send_data_5d_cint
            field_p, field_t = setarray_Cint32(field)
        elif field.dtype == np.float64:
            _cfms_diag_send_data_ = _lib.cFMS_diag_send_data_5d_cdouble
            field_p, field_t = setarray_Cdouble(field)
        elif field.dtype == np.float32:
            _cfms_diag_send_data_ = _lib.cFMS_diag_send_data_5d_cfloat
            field_p, field_t = setarray_Cfloat(field)
        else:
            raise RuntimeError(f"diag_send_data {field.dtype} unsupported")
    else:
        raise RuntimeError(
            f"diag_send_data {field_shape_arr.size} dimensions unsupported"
        )

    _cfms_diag_send_data_.argtypes = [
        diag_field_id_t,
        field_shape_t,
        field_t,
        err_msg_t,
    ]
    _cfms_diag_send_data_.restype = c_bool

    return _cfms_diag_send_data_(
        diag_field_id_c,
        field_shape_p,
        field_p,
        err_msg_c,
    )
