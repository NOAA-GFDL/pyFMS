from ctypes import POINTER, c_int

import numpy as np


npptr = np.ctypeslib.ndpointer
C = "C_CONTIGUOUS"


def define(lib):

    """
    Sets the restype and argtypes of all
    public functions in cFMS
    This function is to be used internally
    during package initialization
    """

    # create_xgrid_2dx2d_order1
    lib.cFMS_create_xgrid_2dx2d_order1.restype = c_int
    lib.cFMS_create_xgrid_2dx2d_order1.argtypes = [
        POINTER(c_int),  # nlon_src
        POINTER(c_int),  # nlat_src
        POINTER(c_int),  # nlon_tgt
        POINTER(c_int),  # nlat_tgt
        npptr(np.float64, ndim=1, flags=C),  # lon_src
        npptr(np.float64, ndim=1, flags=C),  # lat_src
        npptr(np.float64, ndim=1, flags=C),  # lon_tgt
        npptr(np.float64, ndim=1, flags=C),  # lat_tgt
        npptr(np.float64, ndim=1, flags=C),  # mask_src
        POINTER(c_int),  # maxxgrid
        npptr(np.int32, ndim=1, flags=C),  # i_src
        npptr(np.int32, ndim=1, flags=C),  # j_src
        npptr(np.int32, ndim=1, flags=C),  # i_tgt
        npptr(np.int32, ndim=1, flags=C),  # j_tgt
        npptr(np.float64, ndim=1, flags=C),  # xarea
    ]

    # get_maxxgrid
    lib.get_maxxgrid.restype = c_int
    lib.get_maxxgrid.argtypes = None

    # cFMS_horiz_interp_init
    lib.cFMS_horiz_interp_init.restype = None
    lib.cFMS_horiz_interp_init.argtypes = [POINTER(c_int)]

    # cFMS_set_current_interp
    lib.cFMS_set_current_interp.restype = None
    lib.cFMS_set_current_interp.argtypes = [POINTER(c_int)]
