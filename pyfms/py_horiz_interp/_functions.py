from ctypes import POINTER, c_bool, c_char, c_double, c_float, c_int

import numpy as np

from pyfms.utils.ctypes_utils import NDPOINTER


ndpointer = np.ctypeslib.ndpointer
C = ("C_CONTIGUOUS")


def define(lib):

    """
    Sets the restype and argtypes of all
    public functions in cFMS
    This function is to be used internally
    during package initialization
    """

    lib.c_horiz_interp_is_initialized.restype = c_bool
    lib.c_horiz_interp_is_initialized.argtypes = None

    # create_xgrid_2dx2d_order1
    lib.cFMS_create_xgrid_2dx2d_order1.restype = c_int
    lib.cFMS_create_xgrid_2dx2d_order1.argtypes = [
        POINTER(c_int),  # nlon_src
        POINTER(c_int),  # nlat_src
        POINTER(c_int),  # nlon_tgt
        POINTER(c_int),  # nlat_tgt
        ndpointer(np.float64, ndim=2, flags=C),  # lon_src
        ndpointer(np.float64, ndim=2, flags=C),  # lat_src
        ndpointer(np.float64, ndim=2, flags=C),  # lon_tgt
        ndpointer(np.float64, ndim=2, flags=C),  # lat_tgt
        ndpointer(np.float64, ndim=2, flags=C),  # mask_src
        POINTER(c_int),  # maxxgrid
        ndpointer(np.int32, ndim=1, flags=C),  # i_src
        ndpointer(np.int32, ndim=1, flags=C),  # j_src
        ndpointer(np.int32, ndim=1, flags=C),  # i_tgt
        ndpointer(np.int32, ndim=1, flags=C),  # j_tgt
        ndpointer(np.float64, ndim=1, flags=C),  # xarea
    ]

    # get_maxxgrid
    lib.get_maxxgrid.restype = c_int
    lib.get_maxxgrid.argtypes = None

    # cFMS_horiz_interp_init
    lib.cFMS_horiz_interp_init.restype = None
    lib.cFMS_horiz_interp_init.argtypes = [POINTER(c_int)]

    # cFMS_horiz_interp_end
    lib.cFMS_horiz_interp_end.restype = None
    lib.cFMS_horiz_interp_end.argtypes = None

    # cFMS_horiz_interp_2d (for floats and doubles)
    news = [
        (np.float32, lib.cFMS_horiz_interp_new_2d_cfloat),
        (np.float64, lib.cFMS_horiz_interp_new_2d_cdouble),
    ]
    for np_float, cFMS_horiz_interp_new in news:
        cFMS_horiz_interp_new.restype = c_int
        cFMS_horiz_interp_new.argtypes = [
            POINTER(c_int),  # nlon_in
            POINTER(c_int),  # nlat_in
            POINTER(c_int),  # nlon_out
            POINTER(c_int),  # nlat_out
            ndpointer(np_float, ndim=2, flags=C),  # lon_in_ptr
            ndpointer(np_float, ndim=2, flags=C),  # lat_in_ptr
            ndpointer(np_float, ndim=2, flags=C),  # lon_out_ptr
            ndpointer(np_float, ndim=2, flags=C),  # lat_out_ptr
            NDPOINTER(np_float, ndim=2, flags=C),  # mask_in_ptr
            NDPOINTER(np_float, ndim=2, flags=C),  # mask_out_ptr
            POINTER(c_char),  # interp_method
            POINTER(c_int),  # verbose
            NDPOINTER(np_float, ndim=1, flags=C),  # max_dist
            POINTER(c_bool),  # src_modulo
            POINTER(c_bool),  # is_latlon_in
            POINTER(c_bool),  # is_latlon_out
            POINTER(c_bool),  # save_xgrid_area
            POINTER(c_bool),  # as_fregrid
            POINTER(c_bool),  # convert_cf_order
        ]

    # cFMS_horiz_interp_base_2d
    bases = [
        (np.float32, c_float, lib.cFMS_horiz_interp_base_2d_cfloat),
        (np.float64, c_double, lib.cFMS_horiz_interp_base_2d_cdouble),
    ]
    for np_float, c_real, cFMS_horiz_interp_base in bases:
        cFMS_horiz_interp_base.restype = None
        cFMS_horiz_interp_base.argtypes = [
            POINTER(c_int),  # interp_id
            ndpointer(np_float, ndim=2, flags=C),  # data_in_ptr
            ndpointer(np_float, ndim=2, flags=C),  # data_out_ptr
            NDPOINTER(np_float, ndim=2, flags=C),  # mask_in
            NDPOINTER(np_float, ndim=2, flags=C),  # mask_out
            POINTER(c_int),  # verbose
            POINTER(c_real),  # missing_value
            POINTER(c_int),  # missing_permit
            POINTER(c_bool),  # new_missing_handle
            POINTER(c_bool),  # convert_cf_order
        ]

    lib.cFMS_horiz_interp_read_weights_conserve.restype = c_int
    lib.cFMS_horiz_interp_read_weights_conserve.argtypes = [        
        POINTER(c_char),  # weight_filename
        POINTER(c_char),  # weight_file_src
        POINTER(c_int),  # nlon_src
        POINTER(c_int),  # nlat_src
        POINTER(c_int),  # nlon_dst
        POINTER(c_int),  # nlat_dst
        POINTER(c_int),  # isw
        POINTER(c_int),  # iew
        POINTER(c_int),  # jsw
        POINTER(c_int),  # jew
        POINTER(c_int),  # src_tile
        POINTER(c_bool)  # save_xgrid_area
    ]
        
    # getter routines for individual fields
    lib.cFMS_get_wti_cfloat.restype = None
    lib.cFMS_get_wti_cfloat.argtypes = [
        POINTER(c_int),
        ndpointer(np.float32, ndim=3, flags=C),
    ]
    lib.cFMS_get_wti_cdouble.restype = None
    lib.cFMS_get_wti_cdouble.argtypes = [
        POINTER(c_int),
        ndpointer(np.float64, ndim=3, flags=C),
    ]
    lib.cFMS_get_wtj_cfloat.restype = None
    lib.cFMS_get_wtj_cfloat.argtypes = [
        POINTER(c_int),
        ndpointer(np.float32, ndim=3, flags=C),
    ]
    lib.cFMS_get_wtj_cdouble.restype = None
    lib.cFMS_get_wtj_cdouble.argtypes = [
        POINTER(c_int),
        ndpointer(np.float64, ndim=3, flags=C),
    ]

    # cFMS_get_interp_method
    lib.cFMS_get_interp_method.restype = None
    lib.cFMS_get_interp_method.argtypes = [POINTER(c_int), POINTER(c_int)]

    # cFMS_get_i_src
    lib.cFMS_get_i_src.restype = None
    lib.cFMS_get_i_src.argtypes = [POINTER(c_int), ndpointer(np.int32, ndim=1, flags=C)]

    # cFMS_get_j_src
    lib.cFMS_get_j_src.restype = None
    lib.cFMS_get_j_src.argtypes = [POINTER(c_int), ndpointer(np.int32, ndim=1, flags=C)]

    # cFMS_get_i_dst
    lib.cFMS_get_i_dst.restype = None
    lib.cFMS_get_i_dst.argtypes = [POINTER(c_int), ndpointer(np.int32, ndim=1, flags=C)]

    # cFMS_get_j_dst
    lib.cFMS_get_j_dst.restype = None
    lib.cFMS_get_j_dst.argtypes = [POINTER(c_int), ndpointer(np.int32, ndim=1, flags=C)]

    # cFMS_get_area_frac_dst
    lib.cFMS_get_area_frac_dst_cdouble.restype = None
    lib.cFMS_get_area_frac_dst_cdouble.argtypes = [
        POINTER(c_int),
        ndpointer(np.float64, ndim=1, flags=C),
    ]

    # cFMS_get_area_frac_dst
    lib.cFMS_get_xgrid_area_cdouble.restype = None
    lib.cFMS_get_xgrid_area_cdouble.argtypes = [
        POINTER(c_int),
        ndpointer(np.float64, ndim=1, flags=C),
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
