from typing import Any

from pyfms.py_fms import _functions
from pyfms.utils.ctypes_utils import check_str, get_constant_int, set_c_int, set_c_str


_libpath = None
_lib = None

NOTE = None
WARNING = None
FATAL = None
THIRTY_DAY_MONTHS = None
GREGORIAN = None
JULIAN = None
NOLEAP = None

_cFMS_init = None
_cFMS_end = None
_c_fms_is_initialized = None


def check_initialized():
    return __is_initialized


def init(
    alt_input_nml_path: str = None,
    localcomm: int = None,
    ndomain: int = None,
    nnest_domain: int = None,
    calendar_type: int = None,
):

    """
    Calls cfms_init which calls fms_init, calls time_manager_init,
    sets the calendar type in time_manager, and sets the total
    number of domain2D types and nest domain types that will be used

    if ndomain and/or nnest_domain is/are not specified, cFMS will only with
    1 domain2D and/or 1 nest domain
    """

    check_str(alt_input_nml_path, 64, "fms.init")

    arglist = []
    set_c_int(localcomm, arglist)
    set_c_str(alt_input_nml_path, arglist)
    set_c_int(ndomain, arglist)
    set_c_int(nnest_domain, arglist)
    set_c_int(calendar_type, arglist)

    _cFMS_init(*arglist)


def end():

    """
    Calls mpp_error
    Termination routine for the fms module. It also calls destructor routines
    for the mpp, mpp_domains, and mpp_io modules.
    """

    global __is_initialized

    _cFMS_end()


def module_is_initialized():

    """
    returns module_is_initialized variable from c_fms_mod
    """

    return _c_fms_is_initialized()


def _init_constants():

    """
    Initializes parameters for mpp.error (mpp_error)
    and parameters to set the calendar type (these values
    correspond to calendar types in time_manager)

    If a calendar type is not specified, cFMS and FMS
    will default to a NOLEAP calendar
    """

    global NOTE, WARNING, FATAL
    global THIRTY_DAY_MONTHS, GREGORIAN, JULIAN, NOLEAP

    NOTE = get_constant_int(_lib, "NOTE")
    WARNING = get_constant_int(_lib, "WARNING")
    FATAL = get_constant_int(_lib, "FATAL")
    THIRTY_DAY_MONTHS = get_constant_int(_lib, "THIRTY_DAY_MONTHS")
    GREGORIAN = get_constant_int(_lib, "GREGORIAN")
    JULIAN = get_constant_int(_lib, "JULIAN")
    NOLEAP = get_constant_int(_lib, "NOLEAP")


def _init_functions():

    global _cFMS_init
    global _cFMS_end
    global _c_fms_is_initialized

    _functions.define(_lib)

    _cFMS_init = _lib.cFMS_init
    _cFMS_end = _lib.cFMS_end
    _c_fms_is_initialized = _lib.c_fms_is_initialized


def _init(libpath: str, lib: Any):

    """
    Sets _libpath and _lib module variables associated
    with the loaded cFMS library.  This function is
    to be used internally by the cfms module
    """

    global _libpath, _lib

    _lib_path = libpath
    _lib = lib

    _init_constants()
    _init_functions()
