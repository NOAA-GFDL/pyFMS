from ctypes import POINTER, c_char_p, c_int


def define(lib):

    """
    Sets the restype and argtypes of all
    public functions in cFMS
    This function is to be used internally
    during package initialization
    """

    # cFMS_init
    lib.cFMS_init.restype = None
    lib.cFMS_init.argtypes = [
        POINTER(c_int),  # localcomm
        c_char_p,  # alt_input_nml_path
        POINTER(c_int),  # ndomain
        POINTER(c_int),  # nnest_domain
        POINTER(c_int),  # calendar_type
    ]

    # cFMS_end
    lib.cFMS_end.restype = None
    lib.cFMS_end.argtypes = None
