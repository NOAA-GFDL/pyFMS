from ctypes import POINTER, c_bool, c_char_p, c_int

import numpy as np


def define(lib):

    # cFMS_data_override_init
    lib.cFMS_data_override_init.restype = None
    lib.cFMS_data_override_init.argtypes = [
        POINTER(c_int),  # atm_domain_id
        POINTER(c_int),  # ocn_domain_id
        POINTER(c_int),  # ice_domain_id
        POINTER(c_int),  # land_domain_id
        POINTER(c_int),  # land_domainUG_id
        POINTER(c_int),  # mode
    ]

    # cFMS_data_override_set_time
    lib.cFMS_data_override_set_time.restype = None
    lib.cFMS_data_override_set_time.argtypes = [
        POINTER(c_int),  # year
        POINTER(c_int),  # month
        POINTER(c_int),  # day
        POINTER(c_int),  # hour
        POINTER(c_int),  # minute
        POINTER(c_int),  # second
        POINTER(c_int),  # tick
        c_char_p,  # err_msg
    ]

    # cFMS_data_override_0d_cfloat
    lib.cFMS_data_override_0d_cfloat.restype = None
    lib.cFMS_data_override_0d_cfloat.argtypes = [
        c_char_p,  # gridname
        c_char_p,  # fieldname
        np.ctypeslib.ndpointer(np.float32, ndim=1),  # data
        POINTER(c_bool),  # override
        POINTER(c_int),  # data_index
    ]

    # cFMS_data_override_0d_cdouble
    lib.cFMS_data_override_0d_cdouble.restype = None
    lib.cFMS_data_override_0d_cdouble.argtypes = [
        c_char_p,  # gridname
        c_char_p,  # fieldname
        np.ctypeslib.ndpointer(np.float64, ndim=1),  # data
        POINTER(c_bool),  # override
        POINTER(c_int),  # data_index
    ]

    # cFMS_data_override_2d_cfloat
    lib.cFMS_data_override_2d_cfloat.restype = None
    lib.cFMS_data_override_2d_cfloat.argtypes = [
        c_char_p,  # gridname
        c_char_p,  # fieldname
        np.ctypeslib.ndpointer(np.int32, shape=(2)),  # datashape
        np.ctypeslib.ndpointer(np.float32, ndim=2),  # data
        POINTER(c_bool),  # override
        POINTER(c_int),  # is_in
        POINTER(c_int),  # ie_in
        POINTER(c_int),  # js_in
        POINTER(c_int),  # je_in
    ]

    # cFMS_data_override_3d_cfloat
    lib.cFMS_data_override_3d_cfloat.restype = None
    lib.cFMS_data_override_3d_cfloat.argtypes = [
        c_char_p,  # gridname
        c_char_p,  # fieldname
        np.ctypeslib.ndpointer(np.int32, shape=(3)),  # datashape
        np.ctypeslib.ndpointer(np.float32, ndim=3),  # data
        POINTER(c_bool),  # override
        POINTER(c_int),  # is_in
        POINTER(c_int),  # ie_in
        POINTER(c_int),  # js_in
        POINTER(c_int),  # je_in
    ]

    # cFMS_data_override_2d_cdouble
    lib.cFMS_data_override_2d_cdouble.restype = None
    lib.cFMS_data_override_2d_cdouble.argtypes = [
        c_char_p,  # gridname
        c_char_p,  # fieldname
        np.ctypeslib.ndpointer(np.int32, shape=(2)),  # datashape
        np.ctypeslib.ndpointer(np.float64, ndim=2),  # data
        POINTER(c_bool),  # override
        POINTER(c_int),  # is_in
        POINTER(c_int),  # ie_in
        POINTER(c_int),  # js_in
        POINTER(c_int),  # je_in
    ]

    # cFMS_data_override_3d_cdouble
    lib.cFMS_data_override_3d_cdouble.restype = None
    lib.cFMS_data_override_3d_cdouble.argtypes = [
        c_char_p,  # gridname
        c_char_p,  # fieldname
        np.ctypeslib.ndpointer(np.int32, shape=(3)),  # datashape
        np.ctypeslib.ndpointer(np.float64, ndim=3),  # data
        POINTER(c_bool),  # override
        POINTER(c_int),  # is_in
        POINTER(c_int),  # ie_in
        POINTER(c_int),  # js_in
        POINTER(c_int),  # je_in
    ]
