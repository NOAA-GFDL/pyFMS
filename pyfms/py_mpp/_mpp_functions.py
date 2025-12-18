from ctypes import POINTER, c_bool, c_char_p, c_int

import numpy as np

from pyfms.utils.ctypes_utils import NDPOINTER


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
    gatherdict = {
        np.int32: lib.cFMS_gather_pelist_2d_cint,
        np.float32: lib.cFMS_gather_pelist_2d_cfloat,
        np.float64: lib.cFMS_gather_pelist_2d_cdouble,
    }
    for nptype, cFMS_gather in gatherdict.items():
        cFMS_gather.restype = None
        cFMS_gather.argtypes = [
            POINTER(c_int),  # is
            POINTER(c_int),  # ie
            POINTER(c_int),  # js
            POINTER(c_int),  # je
            POINTER(c_int),  # npes
            ndpointer(dtype=np.int32, ndim=1, flags=C),  # pelist
            ndpointer(dtype=nptype, ndim=2, flags=C),  # array_seg
            NDPOINTER(dtype=np.int32, shape=(2,), flags=C),  # gather_data_c_shape
            NDPOINTER(dtype=nptype, ndim=2, flags=C),  # gather_data
            POINTER(c_bool),  # is_root_pe
            POINTER(c_int),  # ishift
            POINTER(c_int),  # jshift
            POINTER(c_bool),  # convert_cf_order
        ]

    # cFMS_gather_1d: set restype/argtypes for supported numpy dtypes
    gatherdict = {
        np.int32: lib.cFMS_gather_1d_cint,
        np.float32: lib.cFMS_gather_1d_cfloat,
        np.float64: lib.cFMS_gather_1d_cdouble,
    }
    for nptype, cFMS_gather in gatherdict.items():
        cFMS_gather.restype = None
        cFMS_gather.argtypes = [
            POINTER(c_int),  # sbufsize
            POINTER(c_int),  # rbufsize
            ndpointer(dtype=nptype, ndim=1, flags=C),  # sbuf
            ndpointer(dtype=nptype, ndim=1, flags=C),  # rbuf
            NDPOINTER(dtype=np.int32, ndim=1, flags=C),  # pelist
            POINTER(c_int),  # npes
        ]

    gatherdict = {
        np.int32: lib.cFMS_gatherv_1d_cint,
        np.float32: lib.cFMS_gatherv_1d_cfloat,
        np.float64: lib.cFMS_gatherv_1d_cdouble,
    }
    for nptype, cFMS_gather in gatherdict.items():
        cFMS_gather.restype = None
        cFMS_gather.argtypes = [
            POINTER(c_int),  # npes
            POINTER(c_int),  # sbuf_size
            POINTER(c_int),  # rbuf_size
            ndpointer(dtype=nptype, ndim=1, flags=C),  # sbuf
            POINTER(c_int),  # ssize
            ndpointer(dtype=nptype, ndim=1, flags=C),  # rbuf
            ndpointer(dtype=np.int32, ndim=1, flags=C),  # rsize
            NDPOINTER(dtype=np.int32, ndim=1, flags=C),  # pelist
        ]

    # cFMS_get_current_pelist
    lib.cFMS_get_current_pelist.restype = None
    lib.cFMS_get_current_pelist.argtypes = [
        POINTER(c_int),  # npes
        NDPOINTER(dtype=np.int32, ndim=(1), flags=C),  # pelist
        c_char_p,  # name
        POINTER(c_int),  # commID
    ]

    # cFMS_npes
    lib.cFMS_npes.restype = c_int
    lib.cFMS_npes.argtypes = None

    # cFMS_pe
    lib.cFMS_pe.restype = c_int
    lib.cFMS_pe.argtypes = None

    # cFMS_root_pe
    lib.cFMS_root_pe.restype = c_int
    lib.cFMS_root_pe.argtypes = None

    # cFMS_set_current_pelist
    lib.cFMS_set_current_pelist.restype = None
    lib.cFMS_set_current_pelist.argtypes = [
        POINTER(c_int),  # npes
        NDPOINTER(dtype=np.int32, ndim=(1), flags=C),  # pelist
        POINTER(c_bool),  # no_sync
    ]

    lib.cFMS_sync.restype = None
    lib.cFMS_sync.argtypes = None
