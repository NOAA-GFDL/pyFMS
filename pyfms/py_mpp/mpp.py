from ctypes import CDLL, POINTER, c_int
from typing import Any

import numpy as np

from ..utils.data_handling import (
    set_Cchar,
    setarray_Cint32,
    setscalar_Cbool,
    setscalar_Cint32,
)


_libpath: str = None
_lib: type[CDLL] = None


def setlib(libpath: str, lib: type[CDLL]):

    """
    Sets _libpath and _lib module variables associated
    with the loaded cFMS library.  This function is
    to be used internally by the cfms module
    """

    global _libpath, _lib

    _libpath = libpath
    _lib = lib


def set_pelist_npes(npes_in: int = None):

    """
    Sets the length of the pelist that is to be sent to
    or retrieved from cFMS/FMS.  This function is to be
    used internally.
    """

    _cfms_set_npes = _lib.cFMS_set_pelist_npes

    npes_in_c, npes_in_t = setscalar_Cint32(npes_in)

    _cfms_set_npes.argtypes = [npes_in_t]
    _cfms_set_npes.restype = None

    if npes_in is not None:
        _cfms_set_npes(npes_in_c)


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

    _cfms_declare_pelist = _lib.cFMS_declare_pelist

    commID = 0

    pelist_p = np.array(pelist, dtype=np.int32)
    pelist_t = np.ctypeslib.ndpointer(dtype=np.int32, shape=(pelist_p.shape))
    name_c, name_t = set_Cchar(name)
    commID_c, commID_t = setscalar_Cint32(commID)

    _cfms_declare_pelist.argtypes = [pelist_t, name_t, commID_t]
    _cfms_declare_pelist.restype = None

    set_pelist_npes(npes_in=len(pelist))
    _cfms_declare_pelist(pelist_p, name_c, commID_c)

    return commID_c.value


def error(errortype: int, errormsg: str = None):

    """
    Calls mpp_error.  An errortype of FATAL will
    call for MPI synchronization and termination
    in FMS
    """

    # truncating string
    if errormsg is not None:
        errormsg = errormsg[:128]

    _cfms_error = _lib.cFMS_error

    errortype_c, errortype_t = setscalar_Cint32(errortype)
    errormsg_c, errormsg_t = set_Cchar(errormsg)

    _cfms_error.argtypes = [errortype_t, errormsg_t]
    _cfms_error.restype = None

    _cfms_error(errortype_c, errormsg_c)


def get_current_pelist(
    npes: int,
    get_name: str = None,
    get_commID: bool = False,
) -> Any:

    """
    Returns the current pelist.
    npes specifies the length of the pelist and must be
    specified to correctly retrieve the current pelist
    """

    commID = 0 if get_commID else None
    name = None
    # if get_name: name="NAME"

    pelist = np.empty(shape=npes, dtype=np.int32)

    _cfms_get_current_pelist = _lib.cFMS_get_current_pelist

    pelist_p, pelist_t = setarray_Cint32(pelist)
    name_c, name_t = set_Cchar(name)
    commID_c, commID_t = setscalar_Cint32(commID)

    _cfms_get_current_pelist.argtypes = [pelist_t, name_t, commID_t]
    _cfms_get_current_pelist.restype = None

    set_pelist_npes(npes_in=npes)
    _cfms_get_current_pelist(pelist_p, name_c, commID_c)

    # TODO: allow for return of name after cFMS fix

    # if name is not None:
    #     name = name_c.value.decode("utf-8")

    # return commID, name

    if get_commID:
        return pelist.tolist(), commID_c.value
    else:
        return pelist.tolist()


def npes() -> int:

    """
    Returns: number of pes in use
    """

    _cfms_npes = _lib.cFMS_npes
    _cfms_npes.restype = c_int
    return _cfms_npes()


def pe() -> int:

    """
    Returns: pe number of calling pe
    """

    _cfms_pe = _lib.cFMS_pe
    _cfms_pe.restype = c_int
    return _cfms_pe()


def set_current_pelist(pelist: list[int] = None, no_sync: bool = None):

    """
    Sets the current pelist
    """

    _cfms_set_current_pelist = _lib.cFMS_set_current_pelist

    if pelist is not None:
        npes = len(pelist)
        pelist_p = np.array(pelist, dtype=np.int32)
        pelist_t = np.ctypeslib.ndpointer(dtype=np.int32, shape=pelist_p.shape)
    else:
        npes = None
        pelist_p = None
        pelist_t = POINTER(c_int)
    no_sync_c, no_sync_t = setscalar_Cbool(no_sync)

    _cfms_set_current_pelist.argtypes = [pelist_t, no_sync_t]
    _cfms_set_current_pelist.restype = None

    set_pelist_npes(npes_in=npes)
    _cfms_set_current_pelist(pelist_p, no_sync_c)
