from ctypes import POINTER, c_bool, c_char_p, c_int

import numpy as np

from pyfms.utils.ctypes_utils import NDPOINTERi32


ndpointer = np.ctypeslib.ndpointer
C = "C_CONTIGUOUS"


def define(lib):

    """
    Sets the restype and argtypes of all
    public functions in cFMS
    This function is to be used internally
    during package initialization
    """

    # cFMS_declare_pelist
    lib.cFMS_declare_pelist.restype = None
    lib.cFMS_declare_pelist.argtypes = [
        POINTER(c_int),  # npes
        ndpointer(dtype=np.int32, ndim=(1), flags=C),  # pelist
        c_char_p,  # name
    ]

    # cFMS_error
    lib.cFMS_error.restype = None
    lib.cFMS_error.argtypes = [POINTER(c_int), c_char_p]  # errortype  # errormsg

    # cFMS_gather_pelist_2ds
    gatherdict = {np.int32: lib.cFMS_gather_pelist_2d_cint,
                np.float64: lib.cFMS_gather_pelist_2d_cdouble,
                np.float32: lib.cFMS_gather_pelist_2d_cfloat
    }
    for nptype, cFMS_gather_pelist_2d in gatherdict.items():
        cFMS_gather_pelist_2d.restype = None
        cFMS_gather_pelist_2d.argtypes = [
            POINTER(c_int), # is
            POINTER(c_int), # ie
            POINTER(c_int), # js
            POINTER(c_int), # je
            POINTER(c_int), # npes
            ndpointer(dtype=np.int32, ndim=(1), flags=C), #pelist
            ndpointer(dtype=nptype, ndim=(2), flags=C), #array_seg
            ndpointer(dtype=np.int32, shape=(2,), flags=C), #gather_data_c_shape
            ndpointer(dtype=nptype, ndim=(2), flags=C), #gather_data
            POINTER(c_bool), #is root_pe
            POINTER(c_int), # ishift
            POINTER(c_int), # jshift
            POINTER(c_bool), #convert_cf_order
        ]
        

    # cFMS_get_current_pelist
    lib.cFMS_get_current_pelist.restype = None
    lib.cFMS_get_current_pelist.argtypes = [
        POINTER(c_int),  # npes
        ndpointer(dtype=np.int32, ndim=(1), flags=C),  # pelist
        c_char_p,  # name
        POINTER(c_int),  # commID
    ]

    # cFMS_npes
    lib.cFMS_npes.restype = c_int
    lib.cFMS_npes.argtypes = None

    # cFMS_pe
    lib.cFMS_pe.restype = c_int
    lib.cFMS_pe.argtypes = None

    # cFMS_set_current_pelist
    lib.cFMS_set_current_pelist.restype = None
    lib.cFMS_set_current_pelist.argtypes = [
        POINTER(c_int),  # npes
        NDPOINTERi32(ndpointer(dtype=np.int32, ndim=(1), flags=C)),  # pelist
        POINTER(c_bool),  # no_sync
    ]
