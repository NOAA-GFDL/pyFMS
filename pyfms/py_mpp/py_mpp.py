import ctypes
from typing import Optional

import numpy as np
from numpy.typing import NDArray

from ..pyfms_utils.data_handling import (
    set_Cchar,
    setarray_Cint32,
    setscalar_Cbool,
    setscalar_Cint32,
)


class pyFMS_mpp:

    def __init__(self, cFMS: ctypes.CDLL = None):
        self.cFMS = cFMS

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

    def declare_pelist(
        self,
        pelist: NDArray,
        name: Optional[str] = None,
        commID: Optional[int] = None,
    ) -> int | None:
        _cfms_declare_pelist = self.cFMS.cFMS_declare_pelist

        pelist_p, pelist_t = setarray_Cint32(pelist)
        name_c, name_t = set_Cchar(name)
        commID_c, commID_t = setscalar_Cint32(commID)

        _cfms_declare_pelist.argtypes = [pelist_t, name_t, commID_t]
        _cfms_declare_pelist.restype = None

        _cfms_declare_pelist(pelist_p, name_c, commID_c)

        if commID is not None:
            commID = commID_c.value
        return commID

    """
    Subroutine: pyfms_error

    Error messaging method

    Returns: No return
    """

    def pyfms_error(self, errortype: int, errormsg: Optional[str] = None):
        # truncating string
        if errormsg is not None:
            errormsg = errormsg[:128]

        _cfms_error = self.cFMS.cFMS_error

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

    def get_current_pelist(
        self,
        name: Optional[str] = None,
        commID: Optional[int] = None,
    ) -> NDArray:

        npes = ctypes.c_int.in_dll(self.cFMS, "cFMS_pelist_npes")
        pelist = np.empty(shape=npes.value, dtype=np.int32, order="C")

        _cfms_get_current_pelist = self.cFMS.cFMS_get_current_pelist

        pelist_p, pelist_t = setarray_Cint32(pelist)
        name_c, name_t = set_Cchar(name)
        commID_c, commID_t = setscalar_Cint32(commID)

        _cfms_get_current_pelist.argtypes = [pelist_t, name_t, commID_t]
        _cfms_get_current_pelist.restype = None

        _cfms_get_current_pelist(pelist_p, name_c, commID_c)

        # TODO: allow for return of name after cFMS fix

        # if name is not None:
        #     name = name_c.value.decode("utf-8")

        # return commID, name

        return pelist

    """
    Function: npes

    Returns: number of pes in use
    """

    def npes(self) -> int:
        _cfms_npes = self.cFMS.cFMS_npes

        _cfms_npes.restype = ctypes.c_int32

        return _cfms_npes()

    """
    Function: pe

    Returns: pe number of calling pe
    """

    def pe(self) -> int:
        _cfms_pe = self.cFMS.cFMS_pe

        _cfms_pe.restype = ctypes.c_int32

        return _cfms_pe()

    """
    Subroutine: set_current_pelist

    Passed pelist will be used to set the current pelist

    The size of the passed pelist must match the current number
    of npes; pelist(npes)

    Returns: No return
    """

    def set_current_pelist(
        self, pelist: Optional[NDArray] = None, no_sync: Optional[bool] = None
    ):
        _cfms_set_current_pelist = self.cFMS.cFMS_set_current_pelist

        pelist_p, pelist_t = setarray_Cint32(pelist)
        no_sync_c, no_sync_t = setscalar_Cbool(no_sync)

        _cfms_set_current_pelist.argtypes = [pelist_t, no_sync_t]
        _cfms_set_current_pelist.restype = None

        _cfms_set_current_pelist(pelist_p, no_sync_c)
