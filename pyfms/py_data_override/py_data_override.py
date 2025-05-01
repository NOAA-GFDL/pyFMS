import ctypes
from typing import Any

import numpy as np
import numpy.typing as npt


class data_override:

    """
    Parameters for initializing data_override in FMS
    These parameters can be specified through data_override.init()
    mode=CFLOAT_MODE initializes data_override in 32-bit mode for real variables
    mode=CDOUBLE_MODE initializes data_override in 64-bit mode for real variables
    if mode is not specified, both 32-bit and 64-bit modes are initialized
    """

    CFLOAT_MODE: int = None
    CDOUBLE_MODE: int = None

    __libpath: str = None
    __lib: type[ctypes.CDLL] = None

    @classmethod
    def setlib(cls, libpath: str, lib: type[ctypes.CDLL]):
        cls.__libpath = libpath
        cls.__lib = lib

    @classmethod
    def lib(cls) -> type[ctypes.CDLL]:
        return cls.__lib

    @classmethod
    def libpath(cls) -> str:
        return cls.__libpath

    """
    pyfms.data_override.init()
    Calls data_override_init in FMS.  Domain_id's are required to pass in the
    domains data_override_init.  Domain_id's is generated through mpp_domains.define
    """

    @classmethod
    def init(
        cls,
        atm_domain_id: int = None,
        ocn_domain_id: int = None,
        ice_domain_id: int = None,
        land_domain_id: int = None,
        land_domainUG_id: int = None,
        mode: int = None,
    ):

        CFLOAT_MODE = int(ctypes.c_int.in_dll(cls.lib(), "CFLOAT_MODE").value)
        CDOUBLE_MODE = int(ctypes.c_int.in_dll(cls.lib(), "CDOUBLE_MODE").value)

        _data_override_init = cls.lib().cFMS_data_override_init

        atm_domain_id_t = ctypes.c_int
        ocn_domain_id_t = ctypes.c_int
        ice_domain_id_t = ctypes.c_int
        land_domain_id_t = ctypes.c_int
        land_domainUG_id_t = ctypes.c_int
        mode_t = ctypes.c_int

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
            land_domainUG_id_t(land_domainUG_id)
            if land_domainUG_id is not None
            else None
        )
        mode_c = mode_t(mode) if mode is not None else None

        _data_override_init.restype = None
        _data_override_init.argtypes = [
            ctypes.POINTER(atm_domain_id_t),
            ctypes.POINTER(ocn_domain_id_t),
            ctypes.POINTER(ice_domain_id_t),
            ctypes.POINTER(land_domain_id_t),
            ctypes.POINTER(land_domainUG_id_t),
            ctypes.POINTER(mode_t),
        ]

        _data_override_init(
            atm_domain_id_c,
            ocn_domain_id_c,
            ice_domain_id_c,
            land_domain_id_c,
            land_domainUG_id_c,
            mode_c,
        )

    """
    pyfms.data_override.set_time()
    Sets the time type in cFMS.  The set time will be used to specify
    targeted time for temporal interpolation in FMS data_override
    """

    @classmethod
    def set_time(
        cls,
        year: int = None,
        month: int = None,
        day: int = None,
        hour: int = None,
        minute: int = None,
        second: int = None,
        tick: int = None,
    ):

        _data_override_set_time = cls.lib().cFMS_data_override_set_time

        year_t = ctypes.c_int
        month_t = ctypes.c_int
        day_t = ctypes.c_int
        hour_t = ctypes.c_int
        minute_t = ctypes.c_int
        second_t = ctypes.c_int
        tick_t = ctypes.c_int
        err_msg_t = ctypes.c_char_p

        year_c = year_t(year) if year is not None else None
        month_c = month_t(month) if month is not None else None
        day_c = day_t(day) if day is not None else None
        hour_c = hour_t(hour) if hour is not None else None
        minute_c = minute_t(minute) if minute is not None else None
        second_c = second_t(second) if second is not None else None
        tick_c = tick_t(tick) if tick is not None else None
        err_msg_c = err_msg_t("NONE".encode("utf-8"))

        _data_override_set_time.restype = None
        _data_override_set_time.argtypes = [
            ctypes.POINTER(year_t),
            ctypes.POINTER(month_t),
            ctypes.POINTER(day_t),
            ctypes.POINTER(hour_t),
            ctypes.POINTER(minute_t),
            ctypes.POINTER(second_t),
            ctypes.POINTER(tick_t),
            ctypes.POINTER(err_msg_t),
        ]

        _data_override_set_time(
            year_c, month_c, day_c, hour_c, minute_c, second_c, tick_c, err_msg_c
        )

    """
    pyfms.data_override.override_scalar
    Calls data_override in FMS for scalar variables
    """

    @classmethod
    def override_scalar(
        cls,
        gridname: str,
        fieldname: str,
        data_type: Any,
        data_index: int = None,
    ) -> np.float32 | np.float64:

        _data_override_scalar = cls.lib().cFMS_data_override_0d_cdouble
        gridname_t = ctypes.c_char_p
        fieldname_t = ctypes.c_char_p
        data_t = ctypes.c_float if data_type is np.float32 else ctypes.c_double
        override_t = ctypes.c_bool
        data_index_t = ctypes.c_int

        gridname_c = gridname_t(gridname.encode("utf-8"))
        fieldname_c = fieldname_t(fieldname.encode("utf-8"))
        data_c = data_t(-99.99)
        override_c = ctypes.c_bool(False)
        data_index_c = data_index_t(data_index) if data_index is not None else None

        _data_override_scalar.restype = None
        _data_override_scalar.argtypes = [
            gridname_t,
            fieldname_t,
            ctypes.POINTER(data_t),
            ctypes.POINTER(override_t),
            ctypes.POINTER(data_index_t),
        ]

        _data_override_scalar(gridname_c, fieldname_c, data_c, override_c, data_index_c)

        # TODO:  add check for override
        return data_c.value

    """
    pyfms.data_override.override
    Calls data override in FMS
    """

    @classmethod
    def override(
        cls,
        gridname: str,
        fieldname: str,
        data_shape: list[int],
        data_type: Any,
        is_in: int = None,
        ie_in: int = None,
        js_in: int = None,
        je_in: int = None,
    ) -> npt.NDArray:

        nshape = len(data_shape)

        if data_type is np.float32:
            if nshape == 2:
                _data_override = cls.lib().cFMS_data_override_2d_cfloat
            if nshape == 3:
                _data_override = cls.lib().cFMS_data_override_3d_cfloat
        elif data_type is np.float64:
            if nshape == 2:
                _data_override = cls.lib().cFMS_data_override_2d_cdouble
            if nshape == 3:
                _data_override = cls.lib().cFMS_data_override_3d_cdouble
        else:
            # add cFMS_end
            raise RuntimeError("Data_override, datatype not supported")

        ndata = np.prod(data_shape)

        gridname_t = ctypes.c_char_p
        fieldname_t = ctypes.c_char_p
        data_shape_t = np.ctypeslib.ndpointer(dtype=np.int32, ndim=(1), shape=(nshape))
        data_t = np.ctypeslib.ndpointer(
            dtype=data_type, ndim=(nshape), shape=data_shape
        )
        override_t = ctypes.c_bool
        is_in_t = ctypes.c_int
        ie_in_t = ctypes.c_int
        js_in_t = ctypes.c_int
        je_in_t = ctypes.c_int

        gridname_c = gridname_t(gridname.encode("utf-8"))
        fieldname_c = fieldname_t(fieldname.encode("utf-8"))
        data_shape_c = np.array(data_shape, dtype=np.int32)
        data = np.ascontiguousarray(np.zeros(data_shape, dtype=data_type, order="C"))
        override = override_t(False)
        is_in_c = is_in_t(is_in) if is_in is not None else None
        js_in_c = js_in_t(js_in) if js_in is not None else None
        ie_in_c = ie_in_t(ie_in) if ie_in is not None else None
        je_in_c = je_in_t(je_in) if je_in is not None else None

        _data_override.restype = None
        _data_override.argtypes = [
            gridname_t,
            fieldname_t,
            data_shape_t,
            data_t,
            ctypes.POINTER(override_t),
            ctypes.POINTER(is_in_t),
            ctypes.POINTER(ie_in_t),
            ctypes.POINTER(js_in_t),
            ctypes.POINTER(je_in_t),
        ]
        _data_override(
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
