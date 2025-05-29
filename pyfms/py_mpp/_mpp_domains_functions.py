from ctypes import POINTER, c_bool, c_char_p, c_int

import numpy as np

from pyfms.utils.ctypes_utils import NDPOINTERi32


npptr = np.ctypeslib.ndpointer
C = "C_CONTIGUOUS"


def define(lib):

    """
    Sets the restype and argtypes of all
    public functions in cFMS
    This function is to be used internally
    during package initialization
    """

    # cFMS_get_compute/data_domain
    for function in [lib.cFMS_get_compute_domain, lib.cFMS_get_data_domain]:
        function.restype = None
        function.argtypes = [
            POINTER(c_int),  # domain_id
            POINTER(c_int),  # xbegin
            POINTER(c_int),  # xend
            POINTER(c_int),  # ybegin
            POINTER(c_int),  # yend
            POINTER(c_int),  # xsize
            POINTER(c_int),  # xmax_size
            POINTER(c_int),  # ysize
            POINTER(c_int),  # ymax_size
            POINTER(c_bool),  # x_is_global
            POINTER(c_bool),  # y_is_global
            POINTER(c_int),  # tile_count
            POINTER(c_int),  # position
            POINTER(c_int),  # whalo
            POINTER(c_int),  # shalo
        ]

    # cFMS_set_compute/data_domain
    for function in [lib.cFMS_set_compute_domain, lib.cFMS_set_data_domain]:
        function.restype = None
        function.argtypes = [
            POINTER(c_int),  # domain_id
            POINTER(c_int),  # xbegin
            POINTER(c_int),  # xend
            POINTER(c_int),  # ybegin
            POINTER(c_int),  # yend
            POINTER(c_int),  # xsize
            POINTER(c_int),  # ysize
            POINTER(c_bool),  # x_is_global
            POINTER(c_bool),  # y_is_global
            POINTER(c_int),  # tile_count
            POINTER(c_int),  # whalo
            POINTER(c_int),  # shalo
        ]

    # cFMS_set_global_domain
    lib.cFMS_set_global_domain.restype = None
    lib.cFMS_set_global_domain.argtypes = [
        POINTER(c_int),  # domain_id
        POINTER(c_int),  # xbegin
        POINTER(c_int),  # xend
        POINTER(c_int),  # ybegin
        POINTER(c_int),  # yend
        POINTER(c_int),  # xsize
        POINTER(c_int),  # ysize
        POINTER(c_int),  # tile_count
        POINTER(c_int),  # whalo
        POINTER(c_int),  # shalo
    ]

    # cFMS_define_domains
    lib.cFMS_define_domains.restype = c_int
    lib.cFMS_define_domains.argtypes = [
        npptr(np.int32, shape=(4), flags=C),  # global_indices
        npptr(np.int32, shape=(2), flags=C),  # layout
        POINTER(c_int),  # npelist
        NDPOINTERi32(npptr(np.int32, ndim=(1), flags=C)),  # pelist
        POINTER(c_int),  # xflags
        POINTER(c_int),  # yflags
        POINTER(c_int),  # xhalo
        POINTER(c_int),  # yhalo
        NDPOINTERi32(npptr(np.int32, ndim=(1), flags=C)),  # xextent
        NDPOINTERi32(npptr(np.int32, ndim=(1), flags=C)),  # yextent
        NDPOINTERi32(npptr(np.bool, ndim=(2), flags=C)),  # maskmap
        c_char_p,  # name
        POINTER(c_bool),  # symmetry
        NDPOINTERi32(npptr(np.int32, shape=(2), flags=C)),  # memory_size
        POINTER(c_int),  # whalo
        POINTER(c_int),  # ehalo
        POINTER(c_int),  # shalo
        POINTER(c_int),  # nhalo
        POINTER(c_bool),  # is_mosaic
        POINTER(c_int),  # tile_count
        POINTER(c_int),  # tile_id
        POINTER(c_bool),  # complete
        POINTER(c_int),  # x_cyclic_offset
        POINTER(c_int),  # y_cyclic_offset
    ]

    # cFMS_define_io_domain
    lib.cFMS_define_io_domain.restype = None
    lib.cFMS_define_io_domain.argtypes = [
        npptr(np.int32, shape=(2), flags=C),  # io_layout
        POINTER(c_int),  # domain_id
    ]

    # cFMS_define_layout
    lib.cFMS_define_layout.restype = None
    lib.cFMS_define_layout.argtypes = [
        npptr(np.int32, shape=(4), flags=C),  # global_indices
        POINTER(c_int),  # ndivs
        npptr(np.int32, shape=(2), flags=C),  # layout
    ]

    # cFMS_define_nest_domains
    lib.cFMS_define_nest_domains.restype = c_int
    lib.cFMS_define_nest_domains.argtypes = [
        POINTER(c_int),  # num_nest
        POINTER(c_int),  # ntiles
        npptr(np.int32, ndim=(1), flags=C),  # nest_level
        npptr(np.int32, ndim=(1), flags=C),  # tile_fine
        npptr(np.int32, ndim=(1), flags=C),  # tile_corase
        npptr(np.int32, ndim=(1), flags=C),  # istart_coarse
        npptr(np.int32, ndim=(1), flags=C),  # icount_coarse
        npptr(np.int32, ndim=(1), flags=C),  # jstart_coarse
        npptr(np.int32, ndim=(1), flags=C),  # jcount_coarse
        npptr(np.int32, ndim=(1), flags=C),  # npes_nest_tiles
        npptr(np.int32, ndim=(1), flags=C),  # x_refine
        npptr(np.int32, ndim=(1), flags=C),  # y_refine
        POINTER(c_int),  # domain_id
        POINTER(c_int),  # extra_halo
        c_char_p,  # name
    ]

    # cFMS_domain_is_initialized
    lib.cFMS_domain_is_initialized.restype = c_bool
    lib.cFMS_domain_is_initialized.argtypes = [POINTER(c_int)]  # domain_id

    # cFMS_get_domain_name
    lib.cFMS_get_domain_name.restype = None
    lib.cFMS_get_domain_name.argtypes = [c_char_p, POINTER(c_int)]  # name  # domain_id

    # cFMS_get_layout
    lib.cFMS_get_layout.restype = None
    lib.cFMS_get_layout.argtypes = [
        npptr(np.int32, shape=(2), flags=C),  # layout
        POINTER(c_int),  # domain_id
    ]

    # cFMS_get_domain_pelist
    lib.cFMS_get_domain_pelist.restype = None
    lib.cFMS_get_domain_pelist.argtypes = [
        npptr(np.int32, ndim=1, flags=C),  # pelist
        POINTER(c_int),  # domain_id
    ]

    # cFMS_set_current_domain
    lib.cFMS_set_current_domain.restype = None
    lib.cFMS_set_current_domain.argtypes = [POINTER(c_int)]  # domain_id

    # cFMS_update_domains_int/float/double_2/3/4/5d
    dtypes = {"int": np.int32, "float": np.float32, "double": np.float64}

    for ndim in range(2, 6):
        for name, dtype in dtypes.items():
            function = getattr(lib, f"cFMS_update_domains_{name}_{ndim}d")
            function.restype = None
            function.argtypes = [
                npptr(np.int32, shape=(ndim), flags=C),  # fieldshape
                npptr(dtype, ndim=(ndim), flags=C),  # field
                POINTER(c_int),  # domain_id
                POINTER(c_int),  # flags
                POINTER(c_bool),  # complete
                POINTER(c_int),  # position
                POINTER(c_int),  # whalo
                POINTER(c_int),  # ehalo
                POINTER(c_int),  # shalo
                POINTER(c_int),  # nhalo
                c_char_p,  # name
                POINTER(c_int),  # tile_count
            ]

    # cFMS_v_update_domains_float/double_2/3/4/5d
    dtypes = {"float": np.float32, "double": np.float64}

    for ndim in range(2, 6):
        for name, dtype in dtypes.items():
            function = getattr(lib, f"cFMS_v_update_domains_{name}_{ndim}d")
            function.restype = None
            function.argtypes = [
                npptr(np.int32, shape=(ndim), flags=C),  # fieldxshape
                npptr(dtype, ndim=(ndim), flags=C),  # fieldx
                npptr(np.int32, shape=(ndim), flags=C),  # fieldyshape
                npptr(dtype, ndim=(ndim), flags=C),  # fieldy
                POINTER(c_int),  # domain_id
                POINTER(c_int),  # flags
                POINTER(c_int),  # grid_type
                POINTER(c_bool), # complete
                POINTER(c_int),  # whalo
                POINTER(c_int),  # ehalo
                POINTER(c_int),  # shalo
                POINTER(c_int),  # nhalo
                c_char_p,  # name
                POINTER(c_int),  # tile_count
            ]
