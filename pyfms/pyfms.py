#!/usr/bin/env python3

import ctypes
import os
from typing import Optional

from .pyfms_utils.data_handling import set_Cchar, setscalar_Cint32


class pyFMS:
    def __init__(
        self,
        cFMS_path: Optional[str] = os.path.dirname(__file__)
        + "/../cFMS/cLIBFMS/lib/libcFMS.so",
        cFMS: ctypes.CDLL = None,
        alt_input_nml_path: str = None,
        localcomm: int = None,
        ndomain: int = None,
        nnest_domain: int = None,
        calendar_type: int = None,
    ):
        self.cFMS_path = cFMS_path
        self.cFMS = cFMS
        self.alt_input_nml_path = alt_input_nml_path
        self.localcomm = localcomm
        self.ndomain = ndomain
        self.nnest_domain = nnest_domain
        self.calendar_type = calendar_type

        if self.cFMS_path is None:
            raise ValueError(
                "Please define the library file path, e.g., as  libFMS(cFMS_path=./cFMS.so)"
            )

        if not os.path.isfile(self.cFMS_path):
            raise ValueError(f"Library {self.cFMS_path} does not exist")

        if self.cFMS is None:
            self.cFMS = ctypes.cdll.LoadLibrary(self.cFMS_path)

        self.pyfms_init(
            self.localcomm,
            self.alt_input_nml_path,
            self.ndomain,
            self.nnest_domain,
            self.calendar_type,
        )

    """
    Subroutine: pyfms_end

    Calls the termination routines for all modules in the MPP package.
    Termination routine for the fms module. It also calls destructor routines
    for the mpp, mpp_domains, and mpp_io modules. If this routine is called
    more than once it will return silently. There are no arguments.
    """

    def pyfms_end(self):
        _cfms_end = self.cFMS.cFMS_end

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
        calendar_type: Optional[int] = None,
    ):
        _cfms_init = self.cFMS.cFMS_init

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

    """
    Subroutine: pyfms_set_pelist_npes

    This method is used to set a npes variable of the cFMS module it wraps
    """

    def set_pelist_npes(self, npes_in: int):
        _cfms_set_npes = self.cFMS.cFMS_set_pelist_npes

        npes_in_c, npes_in_t = setscalar_Cint32(npes_in)

        _cfms_set_npes.argtypes = [npes_in_t]
        _cfms_set_npes.restype = None

        _cfms_set_npes(npes_in_c)
