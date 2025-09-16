from ctypes import POINTER, c_bool, c_char_p, c_double, c_float, c_int

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

    # cFMS_diag_end
    lib.cFMS_diag_end.restype = None
    lib.cFMS_diag_end.argtypes = None

    # cFMS_diag_init
    lib.cFMS_diag_init.restype = None
    lib.cFMS_diag_init.argtypes = [
        POINTER(c_int),  # diag_model_subset
        NDPOINTERi32(npptr(np.int32, shape=(6), flags=C)),  # time_init
        c_char_p,  # err_msg
    ]

    # cFMS_send_complete
    lib.cFMS_diag_send_complete.restype = None
    lib.cFMS_diag_send_complete.argtypes = [
        POINTER(c_int),  # diag_field_id
        c_char_p,  # err_msg
    ]

    # cFMS_diag_set_field_init_time
    lib.cFMS_diag_set_field_init_time.restype = None
    lib.cFMS_diag_set_field_init_time.argtypes = [
        POINTER(c_int),  # year
        POINTER(c_int),  # month
        POINTER(c_int),  # day
        POINTER(c_int),  # hour
        POINTER(c_int),  # minute
        POINTER(c_int),  # second
        POINTER(c_int),  # tick
        c_char_p,  # err_msg
    ]

    # cFMS_set_field_timestep
    lib.cFMS_diag_set_field_timestep.restype = None
    lib.cFMS_diag_set_field_timestep.argtypes = [
        POINTER(c_int),  # diag_field_id
        POINTER(c_int),  # dseconds
        POINTER(c_int),  # ddays
        POINTER(c_int),  # dticks
        c_char_p,  # err_msg
    ]

    # cFMS_diag_advance_field_time
    lib.cFMS_diag_advance_field_time.restype = None
    lib.cFMS_diag_advance_field_time.argtypes = [POINTER(c_int)]

    # cFMS_diag_set_time_end
    lib.cFMS_diag_set_time_end.restype = None
    lib.cFMS_diag_set_time_end.argtypes = [
        POINTER(c_int),  # year
        POINTER(c_int),  # month
        POINTER(c_int),  # day
        POINTER(c_int),  # hour
        POINTER(c_int),  # minute
        POINTER(c_int),  # second
        POINTER(c_int),  # tick
        c_char_p,  # err_msg
    ]

    # cFMS_diag_axis_init_[cfloat,c_double]
    dtypes = {"cfloat": np.float32, "cdouble": np.float64}

    for name, dtype in dtypes.items():
        function = getattr(lib, f"cFMS_diag_axis_init_{name}")
        function.restype = c_int
        function.argtypes = [
            c_char_p,  # name
            POINTER(c_int),  # naxis
            npptr(dtype, flags=C),  # axis
            c_char_p,  # units
            c_char_p,  # cart_name
            POINTER(c_int),  # domain_id
            c_char_p,  # long_name
            POINTER(c_int),  # direction
            c_char_p,  # set_name
            POINTER(c_int),  # edges
            c_char_p,  # aux
            c_char_p,  # req
            POINTER(c_int),  # tile_count
            POINTER(c_int),  # domain_position
            POINTER(c_bool),  # not_xy
        ]

    # cFMS_register_diag_field_scalar
    dtypes = {
        "cint": [np.float32, c_int, NDPOINTERi32],
        "cfloat": [np.float32, c_float, NDPOINTERf],
        "cdouble": [np.float64, c_double, NDPOINTERd],
    }

    for name, [dtype, ictype, NDPOINTER] in dtypes.items():
        function = getattr(lib, f"cFMS_register_diag_field_scalar_{name}")
        function.restype = c_int
        function.argtypes = [
            c_char_p,  # module_name
            c_char_p,  # field_name
            c_char_p,  # long_name
            c_char_p,  # units
            c_char_p,  # standard_name
            POINTER(ictype),  # missing_value
            NDPOINTER(npptr(dtype, shape=(2), flags=C)),  # range
            POINTER(c_bool),  # do_not_log
            c_char_p,  # err_msg
            POINTER(c_int),  # area
            POINTER(c_int),  # volume
            c_char_p,  # realm
            POINTER(c_bool),  # multiple_send_data
        ]

    # cFMS_register_diag_field_array
    dtypes = {
        "cfloat": [np.float32, c_float, NDPOINTERf],
        "cdouble": [np.float64, c_double, NDPOINTERd],
    }

    for name, [dtype, ictype, NDPOINTER] in dtypes.items():
        function = getattr(lib, f"cFMS_register_diag_field_array_{name}")
        function.restype = c_int
        function.argtypes = [
            c_char_p,  # module_name
            c_char_p,  # field_name
            npptr(np.int32, shape=(5), flags=C),  # axes
            c_char_p,  # long_name
            c_char_p,  # units
            POINTER(ictype),  # missing_value
            NDPOINTER(npptr(dtype, shape=(2), flags=C)),  # range
            POINTER(c_bool),  # mask_variant
            c_char_p,  # standard_name
            POINTER(c_bool),  # verbose
            POINTER(c_bool),  # do_not_log
            c_char_p,  # err_msg
            c_char_p,  # interp_method
            POINTER(c_int),  # tile_count
            POINTER(c_int),  # area
            POINTER(c_int),  # volume
            c_char_p,  # realm
            POINTER(c_bool),  # multiple_send_data
        ]

    # cFMS_diag_send_data for ints, floats, doubles
    dtypes = {"cint": np.int32, "cfloat": np.float32, "cdouble": np.float64}

    for ndim in range(2, 5):
        for name, dtype in dtypes.items():
            function = getattr(lib, f"cFMS_diag_send_data_{ndim}d_{name}")
            function.restype = c_bool
            function.argtypes = [
                POINTER(c_int),  # diag_field_id
                npptr(np.int32, shape=(ndim), flags=C),  # field_shape
                npptr(dtype, ndim=ndim, flags=C),  # field
                c_char_p,  # err_msg
                POINTER(c_bool),  # convert_cf_order
            ]
