from typing import Any

import numpy as np
import numpy.typing as npt

from pyfms.py_data_override import _functions
from pyfms.utils.ctypes_utils import (
    get_constant_int,
    set_array,
    set_c_bool,
    set_c_int,
    set_c_str,
    set_list,
)


# library
_libpath = None
_lib = None

# module parameters
CFLOAT_MODE = None
CDOUBLE_MODE = None

# module functions
_cFMS_data_override_init = None
_cFMS_data_override_set_time = None
_cFMS_data_override_0d_cfloat = None
_cFMS_data_override_0d_cdouble = None
_cFMS_data_override_2d_cfloat = None
_cFMS_data_override_2d_cdouble = None
_cFMS_data_override_3d_cfloat = None
_cFMS_data_override_3d_cdouble = None

_cFMS_data_override_scalars = {}
_cFMS_data_overrides = {}


def init(
    atm_domain_id: int = None,
    ocn_domain_id: int = None,
    ice_domain_id: int = None,
    land_domain_id: int = None,
    land_domainUG_id: int = None,
    mode: int = None,
):

    """
    Users can specify the domains associated with each component with
    domain_ids generated from mpp_domains.define.  This id's correspond
    to the FmsMppDomain2D domains saved in cFMS.  If domain_id's are not
    provided, the domain will be initialized as NULL_DOMAINs
    Currently, only domains of type FmsMppDomain2D are supported.

    pyfms is initialized to use the latest cFMS and FMS by default.
    Thus, data_override will only work with data_table.yaml.
    Users should ensure that
    (1) data_table.yaml exists, and
    (2) use_data_table_yaml = .True. is set for &data_override_nml in input.nml

    The above criteria may not be applicable if users have specified to
    load an alternative cFMS and FMS library during cfms.init()
    """

    arglist = []
    set_c_int(atm_domain_id, arglist)
    set_c_int(ocn_domain_id, arglist)
    set_c_int(ice_domain_id, arglist)
    set_c_int(land_domain_id, arglist)
    set_c_int(land_domainUG_id, arglist)
    set_c_int(mode, arglist)

    _cFMS_data_override_init(*arglist)


def set_time(
    year: int = None,
    month: int = None,
    day: int = None,
    hour: int = None,
    minute: int = None,
    second: int = None,
    tick: int = None,
):

    """
    Sets the time type in cFMS.  The set time will be used to specify
    targeted time for temporal interpolation in FMS data_override
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

    _cFMS_data_override_set_time(*arglist)


def override_scalar(
    gridname: str,
    fieldname: str,
    dtype: str,
    data_index: int = None,
) -> np.float32 | np.float64:

    """
    pyfms.data_override.override_scalar
    Interpolates scalar variables
    The interpolation time should be set with
    data_override.set_time() before calling this function
    """

    try:
        _cFMS_data_override = _cFMS_data_override_scalars[dtype]
    except KeyError:
        raise RuntimeError(f"data_override.override_scalar {dtype} not supported")

    arglist = []
    set_c_str(gridname, arglist)
    set_c_str(fieldname, arglist)
    data = set_array(np.array([1.0], dtype=dtype), arglist)
    override = set_c_bool(False, arglist)
    set_c_int(data_index, arglist)

    _cFMS_data_override(*arglist)

    return data[0], override.value


def override(
        gridname: str,
        fieldname: str,
        data: npt.NDArray,
        is_in: int = None,
        ie_in: int = None,
        js_in: int = None,
        je_in: int = None,
        convert_cf_order: bool = True
) -> bool:

    """
    pyfms.data_override.override
    Interpolates data of c_float and c_double kind
    The interpolation time should be set with
    data_override.set_time() before calling this function
    """

    try:
        _cFMS_data_override = _cFMS_data_overrides[data.ndim][data.dtype.name]
    except KeyError:
        raise RuntimeError(
            (
                "data_override.override:"
                f"data of dimensions {data.ndim}"
                f"and/or of type {data.dtype}"
            )
        )

    arglist = []
    set_c_str(gridname, arglist)
    set_c_str(fieldname, arglist)
    set_list(data.shape, np.int32, arglist)
    set_array(data, arglist)
    override = set_c_bool(False, arglist)
    set_c_int(is_in, arglist)
    set_c_int(ie_in, arglist)
    set_c_int(js_in, arglist)
    set_c_int(je_in, arglist)
    set_c_bool(convert_cf_order, arglist)

    _cFMS_data_override(*arglist)

    return override.value


def _init_constants():

    """
    Initializes parameters used in data_override_init
    mode=CFLOAT_MODE initializes data_override in 32-bit mode for real variables
    mode=CDOUBLE_MODE initializes data_override in 64-bit mode for real variables
    if mode is not specified, both 32-bit and 64-bit modes are initialized
    """

    global CFLOAT_MODE, CDOUBLE_MODE

    CFLOAT_MODE = get_constant_int(_lib, "CFLOAT_MODE")
    CDOUBLE_MODE = get_constant_int(_lib, "CDOUBLE_MODE")


def _init_functions():

    global _cFMS_data_override_init
    global _cFMS_data_override_set_time
    global _cFMS_data_override_0d_cfloat
    global _cFMS_data_override_0d_cdouble
    global _cFMS_data_override_2d_cfloat
    global _cFMS_data_override_2d_cdouble
    global _cFMS_data_override_3d_cfloat
    global _cFMS_data_override_3d_cdouble
    global _cFMS_data_override_scalars
    global _cFMS_data_overrides

    _functions.define(_lib)

    _cFMS_data_override_init = _lib.cFMS_data_override_init
    _cFMS_data_override_set_time = _lib.cFMS_data_override_set_time
    _cFMS_data_override_0d_cfloat = _lib.cFMS_data_override_0d_cfloat
    _cFMS_data_override_0d_cdouble = _lib.cFMS_data_override_0d_cdouble
    _cFMS_data_override_2d_cfloat = _lib.cFMS_data_override_2d_cfloat
    _cFMS_data_override_3d_cfloat = _lib.cFMS_data_override_3d_cfloat
    _cFMS_data_override_2d_cdouble = _lib.cFMS_data_override_2d_cdouble
    _cFMS_data_override_3d_cdouble = _lib.cFMS_data_override_3d_cdouble

    _cFMS_data_override_scalars = {
        "float32": _cFMS_data_override_0d_cfloat,
        "float64": _cFMS_data_override_0d_cdouble,
    }

    _cFMS_data_overrides = {
        2: {
            "float32": _cFMS_data_override_2d_cfloat,
            "float64": _cFMS_data_override_2d_cdouble,
        },
        3: {
            "float32": _cFMS_data_override_3d_cfloat,
            "float64": _cFMS_data_override_3d_cdouble,
        },
    }


def _init(libpath: str, lib: Any):

    """
    Sets the library path and library object
    Initializes constants
    Initializes the argtypes and restype of functions
    """

    global _libpath, _lib

    _libpath = libpath
    _lib = lib

    _init_constants()
    _init_functions()
