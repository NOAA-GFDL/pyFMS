from ctypes import CDLL, c_int

from ..utils.data_handling import set_Cchar, setscalar_Cint32


_libpath: str = None
_lib: type[CDLL] = None

NOTE: int = None
WARNING: int = None
FATAL: int = None
THIRTY_DAY_MONTHS: int = None
GREGORIAN: int = None
JULIAN: int = None
NOLEAP: int = None


def setlib(libpath: str, lib: type[CDLL]):

    """
    Sets _libpath and _lib module variables associated
    with the loaded cFMS library.  This function is
    to be used internally by the cfms module
    """

    global _libpath, _lib

    _lib_path = libpath
    _lib = lib


def constants_init():

    """
    Initializes parameters for mpp.error (mpp_error)
    and parameters to set the calendar type (these values
    correspond to calendar types in time_manager)

    If a calendar type is not specified, cFMS and FMS
    will default to a NOLEAP calendar
    """

    def get_constant(variable):
        return int(c_int.in_dll(_lib, variable).value)

    global NOTE, WARNING, FATAL
    global THIRTY_DAY_MONTHS, GREGORIAN, JULIAN, NOLEAP

    NOTE = get_constant("NOTE")
    WARNING = get_constant("WARNING")
    FATAL = get_constant("FATAL")
    THIRTY_DAY_MONTHS = get_constant("THIRTY_DAY_MONTHS")
    GREGORIAN = get_constant("GREGORIAN")
    JULIAN = get_constant("JULIAN")
    NOLEAP = get_constant("NOLEAP")


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

    cfms_init = _lib.cFMS_init

    localcomm_c, localcomm_t = setscalar_Cint32(localcomm)
    alt_input_nml_path_c, alt_input_nml_path_t = set_Cchar(alt_input_nml_path)
    ndomain_c, ndomain_t = setscalar_Cint32(ndomain)
    nnest_domain_c, nnest_domain_t = setscalar_Cint32(nnest_domain)
    calendar_type_c, calendar_type_t = setscalar_Cint32(calendar_type)

    cfms_init.argtypes = [
        localcomm_t,
        alt_input_nml_path_t,
        ndomain_t,
        nnest_domain_t,
        calendar_type_t,
    ]
    cfms_init.restype = None

    cfms_init(
        localcomm_c,
        alt_input_nml_path_c,
        ndomain_c,
        nnest_domain_c,
        calendar_type_c,
    )


def end():

    """
    Calls mpp_error
    Termination routine for the fms module. It also calls destructor routines
    for the mpp, mpp_domains, and mpp_io modules.
    """

    cfms_end = _lib.cFMS_end
    cfms_end.restype = None
    cfms_end()
