#!/usr/bin/env python3

import ctypes

from .py_mpp.py_mpp_domains import mpp_domains
from .utils.constants import constants
from .utils.data_handling import set_Cchar, setscalar_Cint32


class fms:

    __libpath: str = None
    __lib: type[ctypes.CDLL] = None

    NOTE: int = None
    WARNING: int = None
    FATAL: int = None
    THIRTY_DAY_MONTHS: int = None
    GREGORIAN: int = None
    JULIAN: int = None
    NOLEAP: int = None

    @classmethod
    def setlib(cls, libpath: str, lib: type[ctypes.CDLL]):
        cls.__lib_path = libpath
        cls.__lib = lib

    @classmethod
    def lib(cls) -> type[ctypes.CDLL]:
        return cls.__lib

    @classmethod
    def libpath(cls) -> str:
        return cls.__libpath

    @classmethod
    def init(
        cls,
        alt_input_nml_path: str = None,
        localcomm: int = None,
        ndomain: int = None,
        nnest_domain: int = None,
        calendar_type: int = None,
    ):
        def get_constant(variable):
            return int(ctypes.c_int.in_dll(cls.lib(), variable).value)

        cls.NOTE = get_constant("NOTE")
        cls.WARNING = get_constant("WARNING")
        cls.FATAL = get_constant("FATAL")
        cls.THIRTY_DAY_MONTHS = get_constant("THIRTY_DAY_MONTHS")
        cls.GREGORIAN = get_constant("GREGORIAN")
        cls.JULIAN = get_constant("JULIAN")
        cls.NOLEAP = get_constant("NOLEAP")

        _cfms_init = cls.lib().cFMS_init

        localcomm_c, localcomm_t = setscalar_Cint32(localcomm)
        alt_input_nml_path_c, alt_input_nml_path_t = set_Cchar(alt_input_nml_path)
        ndomain_c, ndomain_t = setscalar_Cint32(ndomain)
        nnest_domain_c, nnest_domain_t = setscalar_Cint32(nnest_domain)
        calendar_type_c, calendar_type_t = setscalar_Cint32(calendar_type)

        _cfms_init.argtypes = [
            localcomm_t,
            alt_input_nml_path_t,
            ndomain_t,
            nnest_domain_t,
            calendar_type_t,
        ]
        _cfms_init.restype = None

        _cfms_init(
            localcomm_c,
            alt_input_nml_path_c,
            ndomain_c,
            nnest_domain_c,
            calendar_type_c,
        )
        mpp_domains.init()
        constants.init()

    """
    Subroutine: pyfms_end

    Calls the termination routines for all modules in the MPP package.
    Termination routine for the fms module. It also calls destructor routines
    for the mpp, mpp_domains, and mpp_io modules. If this routine is called
    more than once it will return silently. There are no arguments.
    """

    @classmethod
    def end(cls):
        _cfms_end = cls.lib().cFMS_end
        _cfms_end.restype = None
        _cfms_end()
