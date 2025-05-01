import ctypes
from typing import Any

import numpy as np

from ..utils.data_handling import (
    set_Cchar,
    setarray_Cint32,
    setscalar_Cbool,
    setscalar_Cint32,
)


class mpp:

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
    Subroutine: declare_pelist

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

    @classmethod
    def declare_pelist(
        cls,
        pelist: list[int],
        name: str = None,
    ) -> int:

        _cfms_declare_pelist = cls.lib().cFMS_declare_pelist

        commID = 0

        pelist_p = np.array(pelist, dtype=np.int32)
        pelist_t = np.ctypeslib.ndpointer(dtype=np.int32, shape=(pelist_p.shape))
        name_c, name_t = set_Cchar(name)
        commID_c, commID_t = setscalar_Cint32(commID)

        _cfms_declare_pelist.argtypes = [pelist_t, name_t, commID_t]
        _cfms_declare_pelist.restype = None

        cls.set_pelist_npes(npes_in=len(pelist))
        _cfms_declare_pelist(pelist_p, name_c, commID_c)

        return commID_c.value

    """
    Subroutine: pyfms_error

    Error messaging method

    Returns: No return
    """

    @classmethod
    def error(cls, errortype: int, errormsg: str = None):
        # truncating string
        if errormsg is not None:
            errormsg = errormsg[:128]

        _cfms_error = cls.lib().cFMS_error

        errortype_c, errortype_t = setscalar_Cint32(errortype)
        errormsg_c, errormsg_t = set_Cchar(errormsg)

        _cfms_error.argtypes = [errortype_t, errormsg_t]
        _cfms_error.restype = None

        _cfms_error(errortype_c, errormsg_c)

    """
    Subroutine: get_current_pelist

    Passed pelist will be populated with the current pelist

    The size of the passed pelist must match the current number
    of npes; pelist(npes)

    Returns: NDArray containing pelist
    """

    @classmethod
    def get_current_pelist(
        cls,
        npes: int,
        get_name: str = None,
        get_commID: bool = False,
    ) -> Any:

        commID = 0 if get_commID else None
        name = None
        # if get_name: name="NAME"

        pelist = np.empty(shape=npes, dtype=np.int32)

        _cfms_get_current_pelist = cls.lib().cFMS_get_current_pelist

        pelist_p, pelist_t = setarray_Cint32(pelist)
        name_c, name_t = set_Cchar(name)
        commID_c, commID_t = setscalar_Cint32(commID)

        _cfms_get_current_pelist.argtypes = [pelist_t, name_t, commID_t]
        _cfms_get_current_pelist.restype = None

        cls.set_pelist_npes(npes_in=npes)
        _cfms_get_current_pelist(pelist_p, name_c, commID_c)

        # TODO: allow for return of name after cFMS fix

        # if name is not None:
        #     name = name_c.value.decode("utf-8")

        # return commID, name

        if get_commID:
            return pelist.tolist(), commID_c.value
        else:
            return pelist.tolist()

    """
    Function: npes

    Returns: number of pes in use
    """

    @classmethod
    def npes(cls) -> int:
        _cfms_npes = cls.lib().cFMS_npes

        _cfms_npes.restype = ctypes.c_int32

        return _cfms_npes()

    """
    Function: pe

    Returns: pe number of calling pe
    """

    @classmethod
    def pe(cls) -> int:
        _cfms_pe = cls.lib().cFMS_pe

        _cfms_pe.restype = ctypes.c_int32

        return _cfms_pe()

    """
    Subroutine: set_current_pelist

    Passed pelist will be used to set the current pelist

    The size of the passed pelist must match the current number
    of npes; pelist(npes)

    Returns: No return
    """

    @classmethod
    def set_current_pelist(cls, pelist: list[int] = None, no_sync: bool = None):
        _cfms_set_current_pelist = cls.lib().cFMS_set_current_pelist

        if pelist is not None:
            npes = len(pelist)
            pelist_p = np.array(pelist, dtype=np.int32)
            pelist_t = np.ctypeslib.ndpointer(dtype=np.int32, shape=pelist_p.shape)
        else:
            npes = None
            pelist_p = None
            pelist_t = ctypes.POINTER(ctypes.c_int)
        no_sync_c, no_sync_t = setscalar_Cbool(no_sync)

        _cfms_set_current_pelist.argtypes = [pelist_t, no_sync_t]
        _cfms_set_current_pelist.restype = None

        cls.set_pelist_npes(npes_in=npes)
        _cfms_set_current_pelist(pelist_p, no_sync_c)

    """
    Subroutine: pyfms_set_pelist_npes
    This method is used to set a npes variable of the cFMS module it wraps
    """

    @classmethod
    def set_pelist_npes(cls, npes_in: int = None):
        _cfms_set_npes = cls.lib().cFMS_set_pelist_npes

        npes_in_c, npes_in_t = setscalar_Cint32(npes_in)

        _cfms_set_npes.argtypes = [npes_in_t]
        _cfms_set_npes.restype = None

        if npes_in is not None:
            _cfms_set_npes(npes_in_c)
