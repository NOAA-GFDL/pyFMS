import numpy as np
from numpy.typing import NDArray
from typing import Any

from ..utils.ctypes import (
    get_constant_int,
    check_str,
    set_arr,
    set_c_bool,
    set_c_int,
    set_c_str,
    set_list,
)
from . import _functions

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
_cFMS_diag_register_field_array_cfloat = None
_cFMS_diag_register_field_array_cdouble = None
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
_cFMS_diag_register_diag_scalar = {}
_cFMS_diag_register_diag_array = {}
_cFMS_diag_send_data = {}


def end():

    """
    This function must be called in order to flush out
    the diagnostic buffers and properly close
    the diagnostic files
    """

    _cFMS_diag_end

    
def init(
    diag_model_subset: int = None,
    time_init: list = None,
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
    set_list(time_init, np.int32, arglist)
    err_msg = set_c_str(" ", arglist)

    _cFMS_diag_init(*arglist)

    return err_msg.value.decode("utf-8")


def send_complete(diag_field_id: int) -> str:

    """
    Completes send_data
    This function must be called after the final send data
    call for the given time
    """

    arglist = []
    set_c_int(diag_field_id, arglist)
    err_msg = set_c_str(" ", arglist)
    
    _cFMS_diag_send_complete(*arglist)

    return err_msg.value.decode("utf-8")


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

    arglist = []
    set_c_int(year, arglist)
    set_c_int(month, arglist)
    set_c_int(day, arglist)
    set_c_int(hour, arglist)
    set_c_int(minute, arglist)
    set_c_int(second, arglist)
    set_c_int(tick, arglist)
    err_msg = set_c_str(" ", arglist)
    
    _cFMS_diag_set_field_init_time(*arglist)

    return err_msg.value.decode("utf-8")


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

    arglist = []
    set_c_int(diag_field_id, arglist)
    set_c_int(dseconds, arglist)
    set_c_int(ddays, arglist)
    set_c_int(dticks, arglist)
    err_msg = set_c_str(" ", arglist)
    
    _cFMS_diag_set_field_timestep(*arglist)

    return err_msg.value.decode("utf-8")


def advance_field_time(diag_field_id: int):

    """
    Updates the current field time by advancing
    the current field time with the field timestep
    set with diag_manager.set_field_timestep
    """

    arglist = []
    set_c_int(diag_field_id, arglist)
    
    _cFMS_diag_advance_field_time(*arglist)


def set_time_end(
    year: int = None,
    month: int = None,
    day: int = None,
    hour: int = None,
    minute: int = None,
    second: int = None,
    tick: int = None,
):

    """
    Sets the time type representing the field end time
    in cFMS.  This time must be set before calling
    diag_manager.end()
    """

    arglist = []
    set_c_int(year, arglist)
    set_c_int(month, arglist)
    set_c_int(day, arglist)
    set_c_int(hour, arglist)
    set_c_int(minute, arglist)
    set_c_int(second, arglist)
    set_c_int(tick, arglist)
    err_msg = set_c_str(" ", arglist)
    
    _cFMS_set_time_end( *arglist)


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

    #get function
    
    check_str(long_name, 64, "diag_manager.axis_init")
    check_str(set_name, 64, "diag_manager.axis_init")

    arglist = []
    set_c_str(name, arglist)
    set_c_int(axis_data.size, arglist)
    set_c_str(units, arglist)
    set_c_str(cart_name, arglist)
    set_c_int(domain_id, arglist)
    set_c_str(long_name, arglist)
    set_c_str(set_name, arglist)
    set_c_int(direction, arglist)
    set_c_int(edges, arglist)
    set_c_str(aux, arglist)
    set_c_str(req, arglist)
    set_c_int(tile_count, arglist)
    set_c_int(domain_position, arglist)
    set_c_bool(not_xy, arglist)
    not_xy_c, not_xy_t = setscalar_Cbool(not_xy)

    return cfms_diag_axis_init(*arglist).value


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
) -> int:

    """
    Registers multi-dimensional fields
    The field initial time must be set with
    diag_manager.set_field_init_time before calling
    this method
    """

    #get function
    
    whoami = "diag_manager.register_field_array"
    check_str(module_name, 64, whoami)
    check_str(field_name, 64, whoami)
    check_str(long_name, 64, whoami)
    check_str(units, 64, whoami)
    check_str(standard_name, 64, whoami)
    check_str(interp_method, 64, whoami)
    check_str(realm, 64, whoami)

    if axes is not None:
        while len(axes) < 5: axes.append(0)

    arglist = []
    set_c_char(module_name, arglist)
    set_c_char(field_name, arglist)
    set_list(axes, np.int32, arglist)
    set_c_char(long_name, arglist)
    set_c_char(units, arglist)
    set_c_bool(mask_variant, arglist)
    set_c_char(standard_name, arglist)
    set_c_bool(verbose, arglist)
    set_c_bool(do_not_log, arglist)
    err_msg = set_c_char(" ", arglist)
    set_c_char(interp_method, arglist)
    set_c_int(tile_count, arglist)
    set_c_int(area, arglist)
    set_c_int(volume, arglist)
    set_c_char(realm, arglist)
    set_c_bool(multiple_send_data, arglist)
    multiple_send_data_c, multiple_send_data_t = setscalar_Cbool(multiple_send_data)

    return cfms_register_diag_field_array(*arglist).value


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
) -> int:

    """
    Registers scalar fields
    The field initial time must be set with
    diag_manager.set_field_init_time before calling
    this method
    """

    #check function
    
    whoami = "diag_manager.register_field_scalar"
    check_str(module_name, 64, whoami)
    check_str(fieldname, 64, whoami)
    check_str(long_name, 64, whoami)
    check_str(units, 64, whoami)
    check_str(standard_name, 64, whoami)
    check_str(realm, 64, whoami)

    arglist = []
    set_c_str(module_name, arglist)
    set_c_str(field_name, arglist)
    set_c_str(long_name, arglist)
    set_c_str(units, arglist)
    set_c_str(standard_name, arglist)
    set_c_bool(do_not_long, arglist)
    err_msg = set_c_str(" ", arglist)
    set_c_int(area, arglist)
    set_c_int(volume, arglist)
    set_c_int(realm, arglist)
    set_c_int(multiple_send_data, arglist)
    
    return cfms_register_diag_field_scalar(*arglist).value


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

    #get function
    
    arglist = []
    set_c_int(diag_field_id, arglist)
    set_list(field_shape, np.int32, arglist)
    set_arr(field, arglist)
    err_msg = set_c_str(" ", arglist)
    
    return cfms_diag_send_data(*arglist).value


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
    global _cFMS_diag_set_field_init_time 
    global _cFMS_diag_set_field_timestep 
    global _cFMS_diag_advance_field_time 
    global _cFMS_diag_set_time_end 
    global _cFMS_diag_axis_init_cfloat 
    global _cFMS_diag_axis_init_cdouble 
    global _cFMS_diag_register_diag_scalar_cint 
    global _cFMS_diag_register_diag_scalar_cfloat 
    global _cFMS_diag_register_diag_scalar_cdouble 
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
    global _cFMS_diag_register_diag_scalars
    global _cFMS_diag_register_diag_arrays
    global _cFMS_diag_send_datas

    _functions.define(_lib)

    _cFMS_diag_end = _lib.cFMS_diag_end
    _cFMS_diag_init = _lib.cFMS_diag_init
    _cFMS_diag_send_complete = _lib.cFMS_diag_send_complete
    _cFMS_diag_set_field_init_time = _lib.cFMS_diag_set_field_init_time
    _cFMS_diag_set_field_timestep = _lib.cFMS_diag_set_field_timestep
    _cFMS_diag_advance_field_time = _lib.cFMS_diag_advance_field_time
    _cFMS_diag_set_time_end = _lib.cFMS_diag_set_time_end
    _cFMS_diag_axis_init_cfloat = _lib.cFMS_diag_axis_init_cfloat
    _cFMS_diag_axis_init_cdouble = _lib.cFMS_diag_axis_init_cdouble
    _cFMS_register_diag_field_scalar_cint = _lib.cFMS_register_diag_field_scalar_cint
    _cFMS_register_diag_field_scalar_cfloat = _lib.cFMS_register_diag_field_scalar_cfloat
    _cFMS_register_diag_field_scalar_cdouble = _lib.cFMS_register_diag_field_scalar_cdouble
    _cFMS_register_diag_field_array_cfloat = _lib.cFMS_register_diag_field_array_cfloat
    _cFMS_register_diag_field_array_cdouble = _lib.cFMS_register_diag_field_array_cdouble
    _cFMS_diag_send_data_2d_cint = _lib.cFMS_diag_send_data_2d_cint
    _cFMS_diag_send_data_3d_cint = _lib.cFMS_diag_send_data_3d_cint
    _cFMS_diag_send_data_4d_cint = _lib.cFMS_diag_send_data_4d_cint
    _cFMS_diag_send_data_2d_cfloat = _lib.cFMS_diag_send_data_2d_cfloat
    _cFMS_diag_send_data_3d_cfloat = _lib.cFMS_diag_send_data_3d_cfloat
    _cFMS_diag_send_data_4d_cfloat = _lib.cFMS_diag_send_data_4d_cfloat
    _cFMS_diag_send_data_2d_cdouble = _lib.cFMS_diag_send_data_2d_cdouble
    _cFMS_diag_send_data_3d_cdouble = _lib.cFMS_diag_send_data_3d_cdouble
    _cFMS_diag_send_data_4d_cdouble = _lib.cFMS_diag_send_data_4d_cdouble

    _cFMS_diag_axis_inits = {"float32": _cFMS_diag_axis_init_cfloat,
                             "float64": _cFMS_diag_axis_init_cdouble
    }

    _cFMS_register_field_arrays = {"float32": _cFMS_register_diag_field_array_cfloat,
                                   "float64": _cFMS_register_diag_field_array_cdouble
    }

    _cFMS_register_field_scalars = {"int32" :_cFMS_register_diag_field_scalar_cint,
                                    "float32": _cFMS_register_diag_field_scalar_cfloat,
                                    "float64": _cFMS_register_diag_field_scalar_cdouble
    }

    _cFMS_send_datas = {2: {"int32": _cFMS_diag_send_data_2d_cint,
                            "float32": _cFMS_diag_send_data_2d_cfloat,
                            "float64": _cFMS_diag_send_data_2d_cdouble},
                        3: {"int32": _cFMS_diag_send_data_3d_cint,
                            "float32": _cFMS_diag_send_data_3d_cfloat,
                            "float64": _cFMS_diag_send_data_3d_cdouble},
                        4: {"int32": _cFMS_diag_send_data_4d_cint,
                            "float32": _cFMS_diag_send_data_4d_cfloat,
                            "float64": _cFMS_diag_send_data_4d_cdouble}
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


