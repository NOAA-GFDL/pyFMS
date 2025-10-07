from typing import Any

import numpy as np
import numpy.typing as npt

from pyfms.py_mpp import _mpp_functions
from pyfms.utils.ctypes_utils import (
    check_str,
    set_c_bool,
    set_c_int,
    set_c_str,
    set_list,
)


# library
_libpath = None
_lib = None

_cFMS_declare_pelist = None
_cFMS_error = None
_cFMS_gather_pelist_2d_cdouble = None
_cFMS_gather_pelist_2d_cfloat = None
_cFMS_gather_pelist_2d_cint = None
_cFMS_gather_pelist_2ds = None
_cFMS_get_current_pelist = None
_cFMS_npes = None
_cFMS_pe = None
_cFMS_set_current_pelist = None


def gather(domain: dict, pelist: list, send_array: npt.NDArray, ishift: int = None,
           jshift: int = None, convert_cf_order: bool = True):

    datatype = send_array.dtype
    is_root_pe = pe() == mpp_root()

    try:
        cFMS_gather_pelist_2d = cFMS_gather_pelist_2ds[datatype.name]
    except Exception:
        cFMS_error(FATAL, f"mpp.gather {datatype.name} not supported")
        exit()
    
    nx = domain.ieg-domain.isg+1 if is_root_pe else 1
    ny = domain.jeg-domain.jsg+1 if is_root_pe else 1
    
    arglist = []
    set_c_int(domain.isc, arglist)
    set_c_int(domain.iec, arglist)
    set_c_int(domain.jsc, arglist)
    set_c_int(domain.jec, arglist)
    set_c_int(len(pelist), arglist)
    set_array(send_array, arglist)
    if convert_cf_order:
        set_list([nx, ny], np.int32, arglist)
        receive = set_array(np.zeros((nx,ny), dtype=datatype))
    else:
        set_list([ny, nx], np.int32, arglist)
        receive = set_array(np.zeros((ny,nx), dtype=datatype))
    set_c_bool(is_root_pe, arglist)
    set_c_int(ishift, arglist)
    set_c_int(jshift, arglist)
    set_c_bool(convert_cf_order)
                        
    cFMS_gather_pelist_2d(*arglist)

    if is_root_pe:
        return receive
                            

def declare_pelist(
    pelist: list[int],
    name: str = None,
) -> int:

    """
    This method is written specifically to accommodate a MPI restriction
    that requires a parent communicator to create a child communicator.
    In other words: a pelist cannot go off and declare a communicator,
    but every PE in the parent, including those not in pelist(:), must get
    together for the MPI_COMM_CREATE call. The parent is typically MPI_COMM_WORLD,
    though it could also be a subset that includes all PEs in pelist.

    This call implies synchronization across the PEs in the current pelist,
    of which pelist is a subset.

    The size of the passed pelist must match the current number
    of npes; pelist(npes)

    Returns: commID is returned, and the object passed to the method should be
    set to the result of the call
    """

    arglist = []
    set_c_int(len(pelist), arglist)
    set_list(pelist, np.int32, arglist)
    set_c_str(name, arglist)
    commID = set_c_int(0, arglist)

    _cFMS_declare_pelist(*arglist)

    return commID


def error(errortype: int, errormsg: str = None):

    """
    Calls mpp_error.  An errortype of FATAL will
    call for MPI synchronization and termination
    in FMS
    """

    check_str(errormsg, 128, "mpp.error")

    arglist = []
    set_c_int(errortype, arglist)
    set_c_str(errormsg, arglist)

    _cFMS_error(*arglist)


def get_current_pelist(
    npes: int,
    get_name: bool = False,
    get_commID: bool = False,
) -> Any:

    """
    Returns the current pelist.
    npes specifies the length of the pelist and must be
    specified to correctly retrieve the current pelist
    """

    arglist = []
    set_c_int(npes, arglist)
    pelist = set_list([0] * npes, np.int32, arglist)
    name = set_c_str(" ", arglist) if get_name else set_c_str(None, arglist)
    commid = set_c_int(0, arglist) if get_commID else set_c_int(None, arglist)

    _cFMS_get_current_pelist(*arglist)

    returns = []
    if get_name:
        returns.append(name.value.decode("utf-8"))
    if get_commID:
        returns.append(commid)

    if len(returns) > 0:
        return (pelist.tolist(), *returns)
    return pelist.tolist()


def npes() -> int:

    """
    Returns: number of pes in use
    """

    return _cFMS_npes()


def pe() -> int:

    """
    Returns: pe number of calling pe
    """

    return _cFMS_pe()


def set_current_pelist(pelist: list[int] = None, no_sync: bool = None):

    """
    Sets the current pelist
    """

    arglist = []
    if pelist is None:
        set_c_int(None, arglist)
    else:
        set_c_int(len(pelist), arglist)
    set_list(pelist, np.int32, arglist)
    set_c_bool(no_sync, arglist)

    _cFMS_set_current_pelist(*arglist)


def _init_functions():

    global _cFMS_declare_pelist
    global _cFMS_error
    global _cFMS_gather_pelist_2d_cdouble    
    global _cFMS_gather_pelist_2d_cfloat
    global _cFMS_gather_pelist_2d_cint
    global _cFMS_gather_pelist_2ds
    global _cFMS_get_current_pelist
    global _cFMS_npes
    global _cFMS_pe
    global _cFMS_set_current_pelist

    _mpp_functions.define(_lib)

    _cFMS_declare_pelist = _lib.cFMS_declare_pelist
    _cFMS_error = _lib.cFMS_error
    _cFMS_gather_pelist_2d_cdouble = _lib.cFMS_gather_pelist_2d_cdouble
    _cFMS_gather_pelist_2d_cfloat = _lib.cFMS_gather_pelist_2d_cfloat
    _cFMS_gather_pelist_2d_cint = _lib.cFMS_gather_pelist_2d_cint
    _cFMS_get_current_pelist = _lib.cFMS_get_current_pelist
    _cFMS_npes = _lib.cFMS_npes
    _cFMS_pe = _lib.cFMS_pe
    _cFMS_set_current_pelist = _lib.cFMS_set_current_pelist

    _cFMS_gather_pelist_2ds = {"int32": _cFMS_gather_pelist_2d_cint,
                               "float32": _cFMS_gather_pelist_2d_cfloat,
                               "float64": _cFMS_gather_pelist_2d_cdouble
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

    _init_functions()
