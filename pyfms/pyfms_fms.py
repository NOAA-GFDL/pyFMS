#!/usr/bin/env python3

import ctypes
import os
from typing import Optional

from pyfms.pyfms_data_handling import set_Cchar, setscalar_Cint32


class pyFMS:
    def __init__(
        self,
        clibFMS_path: str = os.path.dirname(__file__)
        + "/../cFMS/cgnuFMS/lib/libcFMS.so",
        clibFMS: ctypes.CDLL = None,
        alt_input_nml_path: str = None,
        localcomm: int = None,
        ndomain: int = 1,
        nnest_domain: int = 1,
    ):
        self.clibFMS_path = clibFMS_path
        self.clibFMS = clibFMS
        self.alt_input_nml_path = alt_input_nml_path
        self.localcomm = localcomm
        self.ndomain = ndomain
        self.nnest_domain = nnest_domain

        if self.clibFMS_path is None:
            raise ValueError(
                "Please define the library file path, e.g., as  libFMS(clibFMS_path=./libcFMS.so)"
            )

        if not os.path.isfile(self.clibFMS_path):
            raise ValueError(f"Library {self.clibFMS_path} does not exist")

        if self.clibFMS is None:
            self.clibFMS = ctypes.cdll.LoadLibrary(self.clibFMS_path)

        self.pyfms_init(
            self.localcomm, self.alt_input_nml_path, self.ndomain, self.nnest_domain
        )

    """
    Subroutine: pyfms_end

    Calls the termination routines for all modules in the MPP package.
    Termination routine for the fms module. It also calls destructor routines
    for the mpp, mpp_domains, and mpp_io modules. If this routine is called
    more than once it will return silently. There are no arguments.
    """

    def pyfms_end(self):
        _cfms_end = self.clibFMS.cFMS_end

        _cfms_end.restype = None

        _cfms_end()

    """
    Subroutine: pyfms_init

    Initializes the FMS module and also calls the initialization routines for
    all modules in the MPP package. Will be called automatically if the user
    does not call it.
    Initialization routine for the fms module. It also calls initialization
    routines for the mpp, mpp_domains, and mpp_io modules. Although this
    routine will be called automatically by other fms_mod routines, users
    should explicitly call fms_init. If this routine is called more than once
    it will return silently. There are no arguments.
    """

    def pyfms_init(
        self,
        localcomm: Optional[int] = None,
        alt_input_nml_path: Optional[str] = None,
        ndomain: Optional[int] = None,
        nnest_domain: Optional[int] = None,
    ):
        _cfms_init = self.clibFMS.cFMS_init

        localcomm_c, localcomm_t = setscalar_Cint32(localcomm)
        alt_input_nml_path_c, alt_input_nml_path_t = set_Cchar(alt_input_nml_path)
        ndomain_c, ndomain_t = setscalar_Cint32(ndomain)
        nnest_domain_c, nnest_domain_t = setscalar_Cint32(nnest_domain)

        _cfms_init.argtypes = [
            localcomm_t,
            alt_input_nml_path_t,
            ndomain_t,
            nnest_domain_t,
        ]
        _cfms_init.restype = None

        _cfms_init(
            localcomm_c,
            alt_input_nml_path_c,
            ndomain_c,
            nnest_domain_c,
        )

    """
    Subroutine: pyfms_set_pelist_npes

    This method is used to set a npes variable of the cFMS module it wraps
    """

    def set_pelist_npes(self, npes_in: int):
        _cfms_set_npes = self.clibFMS.cFMS_set_pelist_npes

        npes_in_c, npes_in_t = setscalar_Cint32(npes_in)

        _cfms_set_npes.argtypes = [npes_in_t]
        _cfms_set_npes.restype = None

        _cfms_set_npes(npes_in_c)
