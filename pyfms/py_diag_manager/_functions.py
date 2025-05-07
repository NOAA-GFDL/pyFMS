from ctypes import c_bool, c_char_p, c_double, c_float, c_int, POINTER
import numpy as np

ndpntr = np.ctypeslib.ndpointer
C = "C_CONTIGUOUS"

def define(lib):

    #cFMS_diag_end
    lib.cFMS_diag_end.restype = None
    lib.cFMS_diag_end.argtypes = None

    #cFMS_diag_init
    lib.cFMS_diag_init.restype = None
    lib.cFMS_diag_init.argtypes = [POINTER(c_int),                       #diag_model_subset
                                  ndpntr(np.int32, shape=(6), flags=C), #time_init
                                  c_char_p                              #err_msg
    ]

    #cFMS_send_complete
    lib.cFMS_diag_send_complete.restype = None
    lib.cFMS_diag_send_complete.argtypes = [POINTER(c_int), #diag_field_id
                                            c_char_p        #err_msg
    ]

    #cFMS_diag_set_field_init_time
    lib.cFMS_diag_set_field_init_time.restype = None
    lib.cFMS_diag_set_field_init_time.argtypes = [POINTER(c_int), #year
                                                  POINTER(c_int), #month
                                                  POINTER(c_int), #day
                                                  POINTER(c_int), #hour
                                                  POINTER(c_int), #minute
                                                  POINTER(c_int), #second
                                                  POINTER(c_int), #tick
                                                  c_char_p        #err_msg
    ]

    #cFMS_set_field_timestep
    lib.cFMS_diag_set_field_timestep.restype = None
    lib.cFMS_diag_set_field_timestep.argtypes = [POINTER(c_int), #diag_field_id
                                                 POINTER(c_int), #dseconds
                                                 POINTER(c_int), #ddays
                                                 POINTER(c_int), #dticks
                                                 c_char_p        #err_msg
    ]

    #cFMS_diag_advance_field_time
    lib.cFMS_diag_advance_field_time.restype = None
    lib.cFMS_diag_advance_field_time.argtypes = [POINTER(c_int)] #diag_field_id

    #cFMS_diag_set_time_end
    lib.cFMS_diag_set_time_end.restype = None
    lib.cFMS_diag_set_time_end.argtypes = [POINTER(c_int), #year
                                           POINTER(c_int), #month
                                           POINTER(c_int), #day
                                           POINTER(c_int), #hour
                                           POINTER(c_int), #minute
                                           POINTER(c_int), #second
                                           POINTER(c_int), #tick
                                           c_char_p        #err_msg
    ]
    
    #cFMS_diag_axis_init_[cfloat,c_double]
    functions = {"cFMS_diag_axis_init_cfloat": np.float32,
                 "cFMS_diag_axis_init_cdouble": np.float64
    }
    for ifunction, dtype in functions.items():
        function = lib[ifunction]
        function.restype = c_int
        function.argtypes = [ c_char_p,                    #name
                              POINTER(c_int),              #naxis 
                              ndpntr(dtype=dtype, flags=C),#axis
                              c_char_p,                    #units
                              c_char_p,                    #cart_name
                              POINTER(c_int),              #domain_id
                              c_char_p,                    #long_name
                              c_char_p,                    #set_name
                              POINTER(c_int),              #direction
                              POINTER(c_int),              #edges
                              c_char_p,                    #aux
                              c_char_p,                    #req
                              POINTER(c_int),              #tile_count
                              POINTER(c_int),              #domain_position
                              POINTER(c_bool)              #not_xy
        ]

    #cFMS_register_diag_field_scalar
    functions = {"cFMS_register_diag_field_scalar_cint": np.int32,
                 "cFMS_register_diag_field_scalar_cfloat": np.float32,
                 "cFMS_register_diag_field_scalar_cdouble": np.float64
    }
    for ifunction, dtype in functions.items():        
        function = lib[ifunction]
        function.restype = c_int
        function.argtypes = [c_char_p,                          #module_name
                             c_char_p,                          #field_name
                             c_char_p,                          #long_name
                             c_char_p,                          #units
                             c_char_p,                          #standard_name
                             POINTER(c_int),                    #missing_value
                             ndpntr(dtype, shape=(2), flags=C), #range
                             POINTER(c_bool),                   #do_not_log
                             c_char_p,                          #err_msg
                             POINTER(c_int),                    #area
                             POINTER(c_int),                    #volume
                             c_char_p,                          #realm
                             POINTER(c_bool)                    #multiple_send_data
        ]

    #cFMS_register_diag_field_array
    functions = {"cFMS_register_diag_field_array_cfloat": np.float32,
                 "cFMS_register_diag_field_array_cdouble": np.float64
    }
    for ifunction, dtype in functions.items():
        function = lib[ifunction]
        function.restype = c_int
        function.argtypes = [c_char_p,                            #module_name
                             c_char_p,                            #field_name
                             ndpntr(np.int32, shape=(5), flags=C),#axes
                             c_char_p,                            #long_name
                             c_char_p,                            #units
                             POINTER(c_float),                    #missing_value
                             ndpntr(dtype, shape=(2), flags=C),   #range
                             POINTER(c_bool),                     #mask_variant
                             c_char_p,                            #standard_name
                             POINTER(c_bool),                     #verbose
                             POINTER(c_bool),                     #do_not_log
                             c_char_p,                            #err_msg
                             c_char_p,                            #interp_method
                             POINTER(c_int),                      #tile_count
                             POINTER(c_int),                      #area
                             POINTER(c_int),                      #volume
                             c_char_p,                            #realm
                             POINTER(c_bool),                     #multiple_send_data
        ]

    #cFMS_diag_send_data for ints
    functions = {"cFMS_diag_send_data_2d_cint": 2,
                 "cFMS_diag_send_data_3d_cint": 3,
                 "cFMS_diag_send_data_4d_cint": 4
    }
    
    for ifunction, ndim in functions.items():
        function = lib[ifunction]
        function.restype = c_bool
        function.argtypes = [POINTER(c_int),                         #diag_field_id
                             ndpntr(np.int32, shape=(ndim), flags=C),#field_shape
                             ndpntr(np.int32, ndim=ndim, flags=C),   #field
                             c_char_p,                               #err_msg
        ]


    #cFMS_diag_send_data for cfloats
    functions = {"cFMS_diag_send_data_2d_cfloat": 2,
                 "cFMS_diag_send_data_3d_cfloat": 3,
                 "cFMS_diag_send_data_4d_cfloat": 4
    }
    
    for ifunction, ndim in functions.items():
        function = lib[ifunction]
        function.restype = c_bool
        function.argtypes = [POINTER(c_int),                           #diag_field_id
                             ndpntr(np.float32, shape=(ndim), flags=C),#field_shape
                             ndpntr(np.float32, ndim=ndim, flags=C),   #field
                             c_char_p,                                 #err_msg
        ]
        
    #cFMS_diag_send_data for cdoubles
    functions = {"cFMS_diag_send_data_2d_cdouble": 2,
                 "cFMS_diag_send_data_3d_cdouble": 3, 
                 "cFMS_diag_send_data_4d_cdouble": 4, 
    }
    
    for ifunction, ndim in functions.items():
        function = lib[ifunction]
        function.restype = c_bool
        function.argtypes = [POINTER(c_int),                           #diag_field_id
                             ndpntr(np.float64, shape=(ndim), flags=C),#field_shape
                             ndpntr(np.float64, ndim=ndim, flags=C),   #field
                             c_char_p,                                 #err_msg
        ]


                               
