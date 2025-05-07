from ctypes import CDLL, POINTER, c_bool, c_char_p, c_double, c_float, c_int
from typing import Any

import numpy as np
import numpy.typing as npt


_libpath: str = None
_lib: type[CDLL] = None

CFLOAT_MODE: int = None
CDOUBLE_MODE: int = None


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
    Initializes parameters used in data_override_init
    mode=CFLOAT_MODE initializes data_override in 32-bit mode for real variables
    mode=CDOUBLE_MODE initializes data_override in 64-bit mode for real variables
    if mode is not specified, both 32-bit and 64-bit modes are initialized
    """

    global CFLOAT_MODE, CDOUBLE_MODE
    CFLOAT_MODE = int(c_int.in_dll(_lib, "CFLOAT_MODE").value)
    CDOUBLE_MODE = int(c_int.in_dll(_lib, "CDOUBLE_MODE").value)


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

    data_override_init = _lib.cFMS_data_override_init

    atm_domain_id_t = c_int
    ocn_domain_id_t = c_int
    ice_domain_id_t = c_int
    land_domain_id_t = c_int
    land_domainUG_id_t = c_int
    mode_t = c_int

    atm_domain_id_c = (
        atm_domain_id_t(atm_domain_id) if atm_domain_id is not None else None
    )
    ocn_domain_id_c = (
        ocn_domain_id_t(ocn_domain_id) if ocn_domain_id is not None else None
    )
    ice_domain_id_c = (
        ice_domain_id_t(ice_domain_id) if ice_domain_id is not None else None
    )
    land_domain_id_c = (
        land_domain_id_t(land_domain_id) if land_domain_id is not None else None
    )
    land_domainUG_id_c = (
        land_domainUG_id_t(land_domainUG_id) if land_domainUG_id is not None else None
    )
    mode_c = mode_t(mode) if mode is not None else None

    data_override_init.restype = None
    data_override_init.argtypes = [
        POINTER(atm_domain_id_t),
        POINTER(ocn_domain_id_t),
        POINTER(ice_domain_id_t),
        POINTER(land_domain_id_t),
        POINTER(land_domainUG_id_t),
        POINTER(mode_t),
    ]

    data_override_init(
        atm_domain_id_c,
        ocn_domain_id_c,
        ice_domain_id_c,
        land_domain_id_c,
        land_domainUG_id_c,
        mode_c,
    )


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

    data_override_set_time = _lib.cFMS_data_override_set_time

    year_t = c_int
    month_t = c_int
    day_t = c_int
    hour_t = c_int
    minute_t = c_int
    second_t = c_int
    tick_t = c_int
    err_msg_t = c_char_p

    year_c = year_t(year) if year is not None else None
    month_c = month_t(month) if month is not None else None
    day_c = day_t(day) if day is not None else None
    hour_c = hour_t(hour) if hour is not None else None
    minute_c = minute_t(minute) if minute is not None else None
    second_c = second_t(second) if second is not None else None
    tick_c = tick_t(tick) if tick is not None else None
    err_msg_c = err_msg_t("NONE".encode("utf-8"))

    data_override_set_time.restype = None
    data_override_set_time.argtypes = [
        POINTER(year_t),
        POINTER(month_t),
        POINTER(day_t),
        POINTER(hour_t),
        POINTER(minute_t),
        POINTER(second_t),
        POINTER(tick_t),
        POINTER(err_msg_t),
    ]

    data_override_set_time(
        year_c, month_c, day_c, hour_c, minute_c, second_c, tick_c, err_msg_c
    )


def override_scalar(
    gridname: str,
    fieldname: str,
    data_type: Any,
    data_index: int = None,
) -> np.float32 | np.float64:

    """
    pyfms.data_override.override_scalar
    Interpolates scalar variables
    The interpolation time should be set with
    data_override.set_time() before calling this function
    """

    data_override_scalar = _lib.cFMS_data_override_0d_cdouble
    gridname_t = c_char_p
    fieldname_t = c_char_p
    data_t = c_float if data_type is np.float32 else c_double
    override_t = c_bool
    data_index_t = c_int

    gridname_c = gridname_t(gridname.encode("utf-8"))
    fieldname_c = fieldname_t(fieldname.encode("utf-8"))
    data_c = data_t(-99.99)
    override_c = c_bool(False)
    data_index_c = data_index_t(data_index) if data_index is not None else None

    data_override_scalar.restype = None
    data_override_scalar.argtypes = [
        gridname_t,
        fieldname_t,
        POINTER(data_t),
        POINTER(override_t),
        POINTER(data_index_t),
    ]

    data_override_scalar(gridname_c, fieldname_c, data_c, override_c, data_index_c)

    # TODO:  add check for override
    return data_c.value


def override(
    gridname: str,
    fieldname: str,
    data_shape: list[int],
    data_type: Any,
    is_in: int = None,
    ie_in: int = None,
    js_in: int = None,
    je_in: int = None,
) -> npt.NDArray:

    """
    pyfms.data_override.override
    Interpolates data of c_float and c_double kind
    The interpolation time should be set with
    data_override.set_time() before calling this function
    """

    nshape = len(data_shape)

    if data_type is np.float32:
        if nshape == 2:
            data_override = _lib.cFMS_data_override_2d_cfloat
        if nshape == 3:
            data_override = _lib.cFMS_data_override_3d_cfloat
    elif data_type is np.float64:
        if nshape == 2:
            data_override = _lib.cFMS_data_override_2d_cdouble
        if nshape == 3:
            data_override = _lib.cFMS_data_override_3d_cdouble
    else:
        # add cFMS_end
        raise RuntimeError("Data_override, datatype not supported")

    ndata = np.prod(data_shape)

    gridname_t = c_char_p
    fieldname_t = c_char_p
    data_shape_t = np.ctypeslib.ndpointer(dtype=np.int32, ndim=(1), shape=(nshape))
    data_t = np.ctypeslib.ndpointer(dtype=data_type, ndim=(nshape), shape=data_shape)
    override_t = c_bool
    is_in_t = c_int
    ie_in_t = c_int
    js_in_t = c_int
    je_in_t = c_int

    gridname_c = gridname_t(gridname.encode("utf-8"))
    fieldname_c = fieldname_t(fieldname.encode("utf-8"))
    data_shape_c = np.array(data_shape, dtype=np.int32)
    data = np.ascontiguousarray(np.zeros(data_shape, dtype=data_type, order="C"))
    override = override_t(False)
    is_in_c = is_in_t(is_in) if is_in is not None else None
    js_in_c = js_in_t(js_in) if js_in is not None else None
    ie_in_c = ie_in_t(ie_in) if ie_in is not None else None
    je_in_c = je_in_t(je_in) if je_in is not None else None

    data_override.restype = None
    data_override.argtypes = [
        gridname_t,
        fieldname_t,
        data_shape_t,
        data_t,
        POINTER(override_t),
        POINTER(is_in_t),
        POINTER(ie_in_t),
        POINTER(js_in_t),
        POINTER(je_in_t),
    ]
    data_override(
        gridname_c,
        fieldname_c,
        data_shape_c,
        data,
        override,
        is_in_c,
        js_in_c,
        ie_in_c,
        je_in_c,
    )

    return data
