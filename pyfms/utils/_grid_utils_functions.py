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

    # cFMS_get_grid_area
    lib.cFMS_get_grid_area.restype = None
    lib.cFMS_get_grid_area.argtypes = [
        POINTER(c_int),  # nlon
        POINTER(c_int),  # nlat
        npptr(dtype=np.float64, ndim=(1), flags=C),  # lon
        npptr(dtype=np.float64, ndim=(1), flags=C),  # lat
        npptr(dtype=np.float64, ndim=(1), flags=C),  # area
    ]
