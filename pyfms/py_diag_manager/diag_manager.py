from datetime import datetime, timedelta
from typing import Any

import numpy as np
from numpy.typing import NDArray

from pyfms.py_diag_manager import _functions
from pyfms.utils.ctypes_utils import (
    check_str,
    get_constant_int,
    set_array,
    set_c_bool,
    set_c_double,
    set_c_float,
    set_c_int,
    set_c_str,
    set_list,
)


DIAG_ALL = None
DIAG_OCEAN = None
DIAG_OTHER = None

_libpath = None
_lib = None

_cFMS_diag_end = None
_cFMS_diag_init = None
_cFMS_diag_send_complete = None
_cFMS_diag_set_field_init_time = None
_cFMS_diag_set_field_timestep = None
_cFMS_diag_advance_field_time = None
_cFMS_diag_set_time_end = None
_cFMS_diag_axis_init_cfloat = None
_cFMS_diag_axis_init_cdouble = None
_cFMS_diag_register_diag_scalar_cint = None
_cFMS_diag_register_diag_scalar_cfloat = None
_cFMS_diag_register_diag_scalar_cdouble = None
_cFMS_diag_register_diag_field_array_cfloat = None
_cFMS_diag_register_diag_field_array_cdouble = None
_cFMS_diag_send_data_2d_cint = None
_cFMS_diag_send_data_3d_cint = None
_cFMS_diag_send_data_4d_cint = None
_cFMS_diag_send_data_2d_cfloat = None
_cFMS_diag_send_data_3d_cfloat = None
_cFMS_diag_send_data_4d_cfloat = None
_cFMS_diag_send_data_2d_cdouble = None
_cFMS_diag_send_data_3d_cdouble = None
_cFMS_diag_send_data_4d_cdouble = None

_cFMS_diag_axis_inits = {}
_cFMS_register_diag_field_arrays = {}
_cFMS_register_diag_field_scalars = {}
_cFMS_diag_send_datas = {}

# TODO: ideally, end_time would be optional here since it can be set prior to the end of a run via set_time_end.
# FMS usage typically sets the end time with diag_manager_end instead, so leaving this as is for now
def end(end_time: datetime):
    """
    Called at end of a run to write and close any diagnostic files.
    """
    arglist = []

    int_time = []
    int_time.append(end_time.year)
    int_time.append(end_time.month)
    int_time.append(end_time.day)
    int_time.append(end_time.hour)
    int_time.append(end_time.minute)
    int_time.append(end_time.second)
    int_time.append(0)  # ticks
    set_list(int_time, np.int32, arglist)
    _cFMS_diag_end(*arglist)


def init(
    diag_model_subset: int = None,
    time_init: datetime = None,
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

    arglist = []
    set_c_int(diag_model_subset, arglist)
    if time_init is not None:
        int_time = []
        int_time.append(time_init.year)
        int_time.append(time_init.month)
        int_time.append(time_init.day)
        int_time.append(time_init.hour)
        int_time.append(time_init.minute)
        int_time.append(time_init.second)
        int_time.append(0)  # ticks
    else:
        int_time = None
    set_list(int_time, np.int32, arglist)
    err_msg = set_c_str(" ", arglist)

    _cFMS_diag_init(*arglist)

    return err_msg.value.decode("utf-8")


def send_complete(timestep: timedelta, ticks: int = 0) -> str:

    """
    Finishes diag manager operations for this timestep; performing any reductions and writing to the file(s).
    This function must be called after all data for a given timestep has been sent via send_data.
    """
    arglist = []

    dtime = datetime.min + timestep
    int_time = []
    # this may need adjustments due to slight differences in datetime/timedelta and fms Time_type
    int_time.append(dtime.year)
    int_time.append(dtime.month)
    int_time.append(dtime.day)
    int_time.append(dtime.hour)
    int_time.append(dtime.minute)
    int_time.append(dtime.second)
    int_time.append(ticks)

    print(f"send complete timestep:{timestep}\ndtime:{dtime}")

    set_list(int_time, np.int32, arglist)
    err_msg = set_c_str(" ", arglist)

    _cFMS_diag_send_complete(*arglist)

    return err_msg.value.decode("utf-8")


def set_time_end(
    time_end: datetime,
):

    """
    Sets the end time for the diag manager.
    """
    arglist = []
    set_c_int(time_end.year, arglist)
    set_c_int(time_end.month, arglist)
    set_c_int(time_end.day, arglist)
    set_c_int(time_end.hour, arglist)
    set_c_int(time_end.minute, arglist)
    set_c_int(time_end.second, arglist)
    set_c_int(0, arglist)  # assumes no ticks
    err_msg = set_c_str(" ", arglist)
    _cFMS_diag_set_time_end(*arglist)


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

    try:
        cfms_diag_axis_init = _cFMS_diag_axis_inits[axis_data.dtype.name]
    except KeyError:
        raise RuntimeError(
            f"diag_manager.diag_axis_init {axis_data.dtype} not supported"
        )

    check_str(long_name, 64, "diag_manager.axis_init")
    check_str(set_name, 64, "diag_manager.axis_init")

    arglist = []
    set_c_str(name, arglist)
    set_c_int(axis_data.size, arglist)
    set_array(axis_data, arglist)
    set_c_str(units, arglist)
    set_c_str(cart_name, arglist)
    set_c_int(domain_id, arglist)
    set_c_str(long_name, arglist)
    set_c_int(direction, arglist)
    set_c_str(set_name, arglist)
    set_c_int(edges, arglist)
    set_c_str(aux, arglist)
    set_c_str(req, arglist)
    set_c_int(tile_count, arglist)
    set_c_int(domain_position, arglist)
    set_c_bool(not_xy, arglist)

    return cfms_diag_axis_init(*arglist)


def register_field_array(
    module_name: str,
    field_name: str,
    dtype,
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
    init_time: datetime = None,
    ticks_per_second: int = 0,
) -> int:

    """
    Registers multi-dimensional fields
    The field initial time must be set with
    diag_manager.set_field_init_time before calling
    this method
    """

    try:
        cFMS_register_diag_field_array = _cFMS_register_diag_field_arrays[dtype]
    except KeyError:
        raise RuntimeError(f"diag_manager.register_field_array {dtype} not supported")

    whoami = "diag_manager.register_field_array"
    check_str(module_name, 64, whoami)
    check_str(field_name, 64, whoami)
    check_str(long_name, 64, whoami)
    check_str(units, 64, whoami)
    check_str(standard_name, 64, whoami)
    check_str(interp_method, 64, whoami)
    check_str(realm, 64, whoami)

    if axes is not None:
        while len(axes) < 5:
            axes.append(0)

    int_time = []
    if init_time is not None:
        int_time.append(init_time.year)
        int_time.append(init_time.month)
        int_time.append(init_time.day)
        int_time.append(init_time.hour)
        int_time.append(init_time.minute)
        int_time.append(init_time.second)
        int_time.append(ticks_per_second)

    arglist = []
    set_c_str(module_name, arglist)
    set_c_str(field_name, arglist)
    set_list(axes, np.int32, arglist)
    set_c_str(long_name, arglist)
    set_c_str(units, arglist)
    set_list(int_time, np.int32, arglist)
    if dtype == "float32":
        set_c_float(missing_value, arglist)
    else:
        set_c_double(missing_value, arglist)
    set_list(range_data, dtype, arglist)
    set_c_bool(mask_variant, arglist)
    set_c_str(standard_name, arglist)
    set_c_bool(verbose, arglist)
    set_c_bool(do_not_log, arglist)
    err_msg = set_c_str(" ", arglist)
    set_c_str(interp_method, arglist)
    set_c_int(tile_count, arglist)
    set_c_int(area, arglist)
    set_c_int(volume, arglist)
    set_c_str(realm, arglist)
    set_c_bool(multiple_send_data, arglist)

    return cFMS_register_diag_field_array(*arglist)


def register_field_scalar(
    module_name: str,
    field_name: str,
    dtype: str,
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
    init_time: datetime = None,
    ticks_per_second: int = 0,
) -> int:

    """
    Registers scalar fields
    """

    try:
        cFMS_register_diag_field_scalar = _cFMS_register_diag_field_scalars[dtype]
    except KeyError:
        raise RuntimeError(f"diag_manager.register_field_scalar {dtype} not supported")

    whoami = "diag_manager.register_field_scalar"
    check_str(module_name, 64, whoami)
    check_str(field_name, 64, whoami)
    check_str(long_name, 64, whoami)
    check_str(units, 64, whoami)
    check_str(standard_name, 64, whoami)
    check_str(realm, 64, whoami)

    int_time = []
    if init_time is not None:
        int_time.append(init_time.year)
        int_time.append(init_time.month)
        int_time.append(init_time.day)
        int_time.append(init_time.hour)
        int_time.append(init_time.minute)
        int_time.append(init_time.second)
        int_time.append(ticks_per_second)

    arglist = []
    set_c_str(module_name, arglist)
    set_c_str(field_name, arglist)
    set_c_str(long_name, arglist)
    set_c_str(units, arglist)
    set_list(int_time, np.int32, arglist)
    set_c_str(standard_name, arglist)
    if dtype == "float32":
        set_c_float(missing_value, arglist)
    else:
        set_c_double(missing_value, arglist)
    set_list(range_data, dtype, arglist)
    set_c_bool(do_not_log, arglist)
    err_msg = set_c_str(" ", arglist)
    set_c_int(area, arglist)
    set_c_int(volume, arglist)
    set_c_int(realm, arglist)
    set_c_int(multiple_send_data, arglist)

    return cFMS_register_diag_field_scalar(*arglist)


def send_data(
    diag_field_id: int,
    field: NDArray,
    convert_cf_order: bool = True,
    time: datetime = None,
    ticks: int = 0,
) -> bool:

    """
    Send field data to diag_manager that will be outputted to a diagnostic file
    The users should set the field time by advancing current time with
    the timestep that has been set with diag_manager.set_field_timestep

    Currently, field data only on the compute domain is supported.
    """

    try:
        cfms_diag_send_data = _cFMS_diag_send_datas[field.ndim][field.dtype.name]
    except KeyError:
        raise RuntimeError(
            (
                "diag_manager.send_data for"
                f"ndim={field.ndim} and type {field.dtype} not supported"
            )
        )
    int_time = []
    if time is not None:
        int_time.append(time.year)
        int_time.append(time.month)
        int_time.append(time.day)
        int_time.append(time.hour)
        int_time.append(time.minute)
        int_time.append(time.second)
        int_time.append(ticks)

    arglist = []
    set_c_int(diag_field_id, arglist)
    set_list([*field.shape], np.int32, arglist)
    set_array(field, arglist)
    err_msg = set_c_str(" ", arglist)
    set_c_bool(convert_cf_order, arglist)
    set_list(int_time, np.int32, arglist)

    return cfms_diag_send_data(*arglist)


def _init_constants():

    """
    Retrieves and assigns diag_manager related parameters
    from FMS
    """

    global DIAG_OTHER, DIAG_OCEAN, DIAG_ALL

    DIAG_OTHER = get_constant_int(_lib, "DIAG_OTHER")
    DIAG_OCEAN = get_constant_int(_lib, "DIAG_OCEAN")
    DIAG_ALL = get_constant_int(_lib, "DIAG_ALL")


def _init_functions():

    global _cFMS_diag_end
    global _cFMS_diag_init
    global _cFMS_diag_send_complete
    global _cFMS_diag_set_time_end
    global _cFMS_diag_axis_init_cfloat
    global _cFMS_diag_axis_init_cdouble
    global _cFMS_diag_register_diag_field_scalar_cint
    global _cFMS_diag_register_diag_field_scalar_cfloat
    global _cFMS_diag_register_diag_field_scalar_cdouble
    global _cFMS_diag_register_field_array_cfloat
    global _cFMS_diag_register_field_array_cdouble
    global _cFMS_diag_send_data_2d_cint
    global _cFMS_diag_send_data_3d_cint
    global _cFMS_diag_send_data_4d_cint
    global _cFMS_diag_send_data_2d_cfloat
    global _cFMS_diag_send_data_3d_cfloat
    global _cFMS_diag_send_data_4d_cfloat
    global _cFMS_diag_send_data_2d_cdouble
    global _cFMS_diag_send_data_3d_cdouble
    global _cFMS_diag_send_data_4d_cdouble
    global _cFMS_diag_axis_inits
    global _cFMS_register_diag_field_arrays
    global _cFMS_register_diag_field_scalars
    global _cFMS_diag_send_datas

    _functions.define(_lib)

    _cFMS_diag_end = _lib.cFMS_diag_end
    _cFMS_diag_init = _lib.cFMS_diag_init
    _cFMS_diag_send_complete = _lib.cFMS_diag_send_complete
    _cFMS_diag_set_time_end = _lib.cFMS_diag_set_time_end
    _cFMS_diag_axis_init_cfloat = _lib.cFMS_diag_axis_init_cfloat
    _cFMS_diag_axis_init_cdouble = _lib.cFMS_diag_axis_init_cdouble
    _cFMS_register_diag_field_scalar_cint = _lib.cFMS_register_diag_field_scalar_cint
    _cFMS_register_diag_field_scalar_cfloat = (
        _lib.cFMS_register_diag_field_scalar_cfloat
    )
    _cFMS_register_diag_field_scalar_cdouble = (
        _lib.cFMS_register_diag_field_scalar_cdouble
    )
    _cFMS_register_diag_field_array_cfloat = _lib.cFMS_register_diag_field_array_cfloat
    _cFMS_register_diag_field_array_cdouble = (
        _lib.cFMS_register_diag_field_array_cdouble
    )
    _cFMS_diag_send_data_2d_cint = _lib.cFMS_diag_send_data_2d_cint
    _cFMS_diag_send_data_3d_cint = _lib.cFMS_diag_send_data_3d_cint
    _cFMS_diag_send_data_4d_cint = _lib.cFMS_diag_send_data_4d_cint
    _cFMS_diag_send_data_2d_cfloat = _lib.cFMS_diag_send_data_2d_cfloat
    _cFMS_diag_send_data_3d_cfloat = _lib.cFMS_diag_send_data_3d_cfloat
    _cFMS_diag_send_data_4d_cfloat = _lib.cFMS_diag_send_data_4d_cfloat
    _cFMS_diag_send_data_2d_cdouble = _lib.cFMS_diag_send_data_2d_cdouble
    _cFMS_diag_send_data_3d_cdouble = _lib.cFMS_diag_send_data_3d_cdouble
    _cFMS_diag_send_data_4d_cdouble = _lib.cFMS_diag_send_data_4d_cdouble

    _cFMS_diag_axis_inits = {
        "float32": _cFMS_diag_axis_init_cfloat,
        "float64": _cFMS_diag_axis_init_cdouble,
    }

    _cFMS_register_diag_field_arrays = {
        "float32": _cFMS_register_diag_field_array_cfloat,
        "float64": _cFMS_register_diag_field_array_cdouble,
    }

    _cFMS_register_diag_field_scalars = {
        "int32": _cFMS_register_diag_field_scalar_cint,
        "float32": _cFMS_register_diag_field_scalar_cfloat,
        "float64": _cFMS_register_diag_field_scalar_cdouble,
    }

    _cFMS_diag_send_datas = {
        2: {
            "int32": _cFMS_diag_send_data_2d_cint,
            "float32": _cFMS_diag_send_data_2d_cfloat,
            "float64": _cFMS_diag_send_data_2d_cdouble,
        },
        3: {
            "int32": _cFMS_diag_send_data_3d_cint,
            "float32": _cFMS_diag_send_data_3d_cfloat,
            "float64": _cFMS_diag_send_data_3d_cdouble,
        },
        4: {
            "int32": _cFMS_diag_send_data_4d_cint,
            "float32": _cFMS_diag_send_data_4d_cfloat,
            "float64": _cFMS_diag_send_data_4d_cdouble,
        },
    }


def _init(libpath: str, lib: Any):

    """
    Sets _libpath and _lib module variables associated
    with the loaded cFMS library.  This function is
    to be used internally by the cfms module
    """

    global _libpath, _lib

    _libpath = libpath
    _lib = lib

    _init_constants()
    _init_functions()
