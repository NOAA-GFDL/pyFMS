from ctypes import POINTER, c_bool, c_char, c_double, c_float, c_int

import numpy as np

from pyfms.utils.ctypes_utils import NDPOINTERd, NDPOINTERf


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
        npptr(np.float64, ndim=2, flags=C),  # lon_src
        npptr(np.float64, ndim=2, flags=C),  # lat_src
        npptr(np.float64, ndim=2, flags=C),  # lon_tgt
        npptr(np.float64, ndim=2, flags=C),  # lat_tgt
        npptr(np.float64, ndim=2, flags=C),  # mask_src
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

    # cFMS_horiz_interp_2d (for floats and doubles)
    lib.cFMS_horiz_interp_new_2d_cdouble.restype = c_int
    lib.cFMS_horiz_interp_new_2d_cdouble.argtypes = [
        npptr(np.float64, ndim=2, flags=C),  # lon_in_ptr
        npptr(np.float64, ndim=2, flags=C),  # lat_in_ptr
        npptr(np.int32, ndim=1, flags=C),  # lonlat_in_shape
        npptr(np.float64, ndim=2, flags=C),  # lon_out_ptr
        npptr(np.float64, ndim=2, flags=C),  # lat_out_ptr
        npptr(np.int32, ndim=1, flags=C),  # lonlat_out_shape
        NDPOINTERd(npptr(np.float64, ndim=2, flags=C)),  # mask_in_ptr
        NDPOINTERd(npptr(np.float64, ndim=2, flags=C)),  # mask_out_ptr
        POINTER(c_char),  # interp_method
        POINTER(c_int),  # verbose
        NDPOINTERd(npptr(np.float64, ndim=1, flags=C)),  # max_dist
        POINTER(c_bool),  # src_modulo
        POINTER(c_bool),  # is_latlon_in
        POINTER(c_bool),  # is_latlon_out
    ]

    # cFMS_horiz_interp_2d (for floats and doubles)
    lib.cFMS_horiz_interp_new_2d_cfloat.restype = c_int
    lib.cFMS_horiz_interp_new_2d_cfloat.argtypes = [
        npptr(np.float32, ndim=2, flags=C),  # lon_in_ptr
        npptr(np.float32, ndim=2, flags=C),  # lat_in_ptr
        npptr(np.int32, ndim=1, flags=C),  # lonlat_in_shape
        npptr(np.float32, ndim=2, flags=C),  # lon_out_ptr
        npptr(np.float32, ndim=2, flags=C),  # lat_out_ptr
        npptr(np.int32, ndim=1, flags=C),  # lonlat_out_shape
        NDPOINTERf(npptr(np.float32, ndim=2, flags=C)),  # mask_in_ptr
        NDPOINTERf(npptr(np.float32, ndim=2, flags=C)),  # mask_out_ptr
        POINTER(c_char),  # interp_method
        POINTER(c_int),  # verbose
        NDPOINTERf(npptr(np.float32, ndim=1, flags=C)),  # max_dist
        POINTER(c_bool),  # src_modulo
        POINTER(c_bool),  # is_latlon_in
        POINTER(c_bool),  # is_latlon_out
    ]

    # cFMS_horiz_interp-base_2d
    lib.cFMS_horiz_interp_base_2d_cfloat.restype = None
    lib.cFMS_horiz_interp_base_2d_cfloat.argtypes = [
        POINTER(c_int),  # interp_id
        npptr(np.float32, ndim=2, flags=C),  # data_in_ptr
        npptr(np.int32, ndim=1, flags=C),  # data_in_shape
        npptr(np.float32, ndim=2, flags=C),  # data_out_ptr
        npptr(np.int32, ndim=1, flags=C),  # data_out_shape
        NDPOINTERf(npptr(np.float32, ndim=2, flags=C)),  # mask_in
        NDPOINTERf(npptr(np.float32, ndim=2, flags=C)),  # mask_out
        POINTER(c_int),  # verbose
        POINTER(c_float),  # missing_value
        POINTER(c_int),  # missing_permit
        POINTER(c_bool),  # new_missing_handle
    ]

    # cFMS_horiz_interp-base_2d
    lib.cFMS_horiz_interp_base_2d_cdouble.restype = None
    lib.cFMS_horiz_interp_base_2d_cdouble.argtypes = [
        POINTER(c_int),  # interp_id
        npptr(np.float64, ndim=2, flags=C),  # data_in_ptr
        npptr(np.int32, ndim=1, flags=C),  # data_in_shape
        npptr(np.float64, ndim=2, flags=C),  # data_out_ptr
        npptr(np.int32, ndim=1, flags=C),  # data_out_shape
        NDPOINTERd(npptr(np.float64, ndim=2, flags=C)),  # mask_in
        NDPOINTERd(npptr(np.float64, ndim=2, flags=C)),  # mask_out
        POINTER(c_int),  # verbose
        POINTER(c_double),  # missing_value
        POINTER(c_int),  # missing_permit
        POINTER(c_bool),  # new_missing_handle
    ]

    # getter routines for individual fields
    lib.cFMS_get_wti_cfloat.restype = None
    lib.cFMS_get_wti_cfloat.argtypes = [
        POINTER(c_int),
        npptr(np.float32, ndim=3, flags=C),
    ]
    lib.cFMS_get_wti_cdouble.restype = None
    lib.cFMS_get_wti_cdouble.argtypes = [
        POINTER(c_int),
        npptr(np.float64, ndim=3, flags=C),
    ]
    lib.cFMS_get_wtj_cfloat.restype = None
    lib.cFMS_get_wtj_cfloat.argtypes = [
        POINTER(c_int),
        npptr(np.float32, ndim=3, flags=C),
    ]
    lib.cFMS_get_wtj_cdouble.restype = None
    lib.cFMS_get_wtj_cdouble.argtypes = [
        POINTER(c_int),
        npptr(np.float64, ndim=3, flags=C),
    ]

    # cFMS_get_interp_method
    lib.cFMS_get_interp_method.restype = None
    lib.cFMS_get_interp_method.argtypes = [POINTER(c_int), POINTER(c_int)]

    # cFMS_get_i_src
    lib.cFMS_get_i_src.restype = None
    lib.cFMS_get_i_src.argtypes = [POINTER(c_int), npptr(np.int32, ndim=1, flags=C)]

    # cFMS_get_j_src
    lib.cFMS_get_j_src.restype = None
    lib.cFMS_get_j_src.argtypes = [POINTER(c_int), npptr(np.int32, ndim=1, flags=C)]

    # cFMS_get_i_dst
    lib.cFMS_get_i_dst.restype = None
    lib.cFMS_get_i_dst.argtypes = [POINTER(c_int), npptr(np.int32, ndim=1, flags=C)]

    # cFMS_get_j_dst
    lib.cFMS_get_j_dst.restype = None
    lib.cFMS_get_j_dst.argtypes = [POINTER(c_int), npptr(np.int32, ndim=1, flags=C)]

    # cFMS_get_area_frac_dst
    lib.cFMS_get_area_frac_dst_cdouble.restype = None
    lib.cFMS_get_area_frac_dst_cdouble.argtypes = [
        POINTER(c_int),
        npptr(np.float64, ndim=1, flags=C),
    ]

    # cFMS_get_nlon_src
    lib.cFMS_get_nlon_src.restype = None
    lib.cFMS_get_nlon_src.argtypes = [POINTER(c_int), POINTER(c_int)]

    # cFMS_get_nlat_src
    lib.cFMS_get_nlat_src.restype = None
    lib.cFMS_get_nlat_src.argtypes = [POINTER(c_int), POINTER(c_int)]

    # cFMS_get_nlon_dst
    lib.cFMS_get_nlon_dst.restype = None
    lib.cFMS_get_nlon_dst.argtypes = [POINTER(c_int), POINTER(c_int)]

    # cFMS_get_nlat_dst
    lib.cFMS_get_nlat_dst.restype = None
    lib.cFMS_get_nlat_dst.argtypes = [POINTER(c_int), POINTER(c_int)]

    # cFMS_get_nxgrid
    lib.cFMS_get_nxgrid.restype = None
    lib.cFMS_get_nxgrid.argtypes = [POINTER(c_int), POINTER(c_int)]
