from ctypes import POINTER, c_int, c_char, c_bool

import numpy as np
from pyfms.utils.ctypes_utils import NDPOINTERd, NDPOINTERf, NDPOINTERi32


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

    # cFMS_horiz_interp_2d (for floats and doubles)
    lib.cFMS_horiz_interp_2d_cdouble.restype = c_int
    lib.cFMS_horiz_interp_2d_cdouble.argtypes = [ npptr(np.float64, ndim=1, flags=C), # lon_in_ptr
                                                  npptr(np.int32, ndim=1, flags=C),  # lon_in_shape
                                                  npptr(np.float64, ndim=1, flags=C), # lat_in_ptr
                                                  npptr(np.int32, ndim=1, flags=C),  # lat_in_shape
                                                  npptr(np.float64, ndim=1, flags=C), # lon_out_ptr
                                                  npptr(np.int32, ndim=1, flags=C),  # lon_out_shape
                                                  npptr(np.float64, ndim=1, flags=C), # lat_out_ptr
                                                  npptr(np.int32, ndim=1, flags=C),  # lat_out_shape
                                                  POINTER(c_char), # interp_method
                                                  POINTER(c_int), # verbose
                                                  NDPOINTERd(npptr(np.float64, ndim=1, flags=C)), # max_dist
                                                  POINTER(c_bool), # src_modulo
                                                  NDPOINTERd(npptr(np.float64, ndim=1, flags=C)), # mask_in_ptr
                                                  NDPOINTERd(npptr(np.float64, ndim=1, flags=C)), # mask_out_ptr
                                                  POINTER(c_bool), # is_latlon_in
                                                  POINTER(c_bool)  # is_latlon_out
                                                ]

    lib.cFMS_horiz_interp_2d_cfloat.restype = c_int
    lib.cFMS_horiz_interp_2d_cfloat.argtypes = [  npptr(np.float32, ndim=1, flags=C), # lon_in_ptr
                                                  npptr(np.int32, ndim=1, flags=C),  # lon_in_shape
                                                  npptr(np.float32, ndim=1, flags=C), # lat_in_ptr
                                                  npptr(np.int32, ndim=1, flags=C),  # lat_in_shape
                                                  npptr(np.float32, ndim=1, flags=C), # lon_out_ptr
                                                  npptr(np.int32, ndim=1, flags=C),  # lon_out_shape
                                                  npptr(np.float32, ndim=1, flags=C), # lat_out_ptr
                                                  npptr(np.int32, ndim=1, flags=C),  # lat_out_shape
                                                  POINTER(c_char), # interp_method
                                                  POINTER(c_int), # verbose
                                                  NDPOINTERd(npptr(np.float32, ndim=1, flags=C)), # max_dist
                                                  POINTER(c_bool), # src_modulo
                                                  NDPOINTERd(npptr(np.float32, ndim=1, flags=C)), # mask_in_ptr
                                                  NDPOINTERd(npptr(np.float32, ndim=1, flags=C)), # mask_out_ptr
                                                  POINTER(c_bool), # is_latlon_in
                                                  POINTER(c_bool)  # is_latlon_out
                                                ]

    # getter routine for most of the fields used by conservative
    lib.cFMS_get_interp_cfloat.restype = None
    lib.cFMS_get_interp_cfloat.argtypes = [ POINTER(c_int), # interp_id
                                            NDPOINTERi32(npptr(np.int32, ndim=1, flags=C)), # i_src
                                            NDPOINTERi32(npptr(np.int32, ndim=1, flags=C)), # j_src
                                            NDPOINTERi32(npptr(np.int32, ndim=1, flags=C)), # i_dst
                                            NDPOINTERi32(npptr(np.int32, ndim=1, flags=C)), # j_dst
                                            NDPOINTERf(npptr(np.float32, ndim=1, flags=C)), # area_frac_dst,
                                            POINTER(c_int), # version
                                            POINTER(c_int), # nxgrid
                                            POINTER(c_int), # nlon_src
                                            POINTER(c_int), # nlat_src
                                            POINTER(c_int), # nlon_dst
                                            POINTER(c_int), # nlat_dst
                                            POINTER(c_bool), # is_allocated
                                            POINTER(c_int) #interp method
                                            ]
    lib.cFMS_get_interp_cdouble.restype = None
    lib.cFMS_get_interp_cdouble.argtypes = [ POINTER(c_int), # interp_id
                                             NDPOINTERi32(npptr(np.int32, ndim=1, flags=C)), # i_src
                                             NDPOINTERi32(npptr(np.int32, ndim=1, flags=C)), # j_src
                                             NDPOINTERi32(npptr(np.int32, ndim=1, flags=C)), # i_dst
                                             NDPOINTERi32(npptr(np.int32, ndim=1, flags=C)), # j_dst
                                             NDPOINTERf(npptr(np.float64, ndim=1, flags=C)), # area_frac_dst,
                                             POINTER(c_int), # version
                                             POINTER(c_int), # nxgrid
                                             POINTER(c_int), # nlon_src
                                             POINTER(c_int), # nlat_src
                                             POINTER(c_int), # nlon_dst
                                             POINTER(c_int), #nlat_dst
                                             POINTER(c_bool), # is_allocated
                                             POINTER(c_int) #interp method
                                            ]

    # getter routines for individual fields
    lib.cFMS_get_wti_cfloat.restype = None
    lib.cFMS_get_wti_cfloat.argtypes = [ POINTER(c_int), npptr(np.float32, ndim=3, flags=C)]
    lib.cFMS_get_wti_cdouble.restype = None
    lib.cFMS_get_wti_cdouble.argtypes = [ POINTER(c_int), npptr(np.float64, ndim=3, flags=C)]
    lib.cFMS_get_wtj_cfloat.restype = None
    lib.cFMS_get_wtj_cfloat.argtypes = [ POINTER(c_int), npptr(np.float32, ndim=3, flags=C)]
    lib.cFMS_get_wtj_cdouble.restype = None
    lib.cFMS_get_wtj_cdouble.argtypes = [ POINTER(c_int), npptr(np.float64, ndim=3, flags=C)]
