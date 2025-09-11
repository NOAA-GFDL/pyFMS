from typing import Any

import numpy as np
import numpy.typing as npt

from pyfms.py_fms.fms import FATAL
from pyfms.py_horiz_interp import _functions
from pyfms.py_mpp.mpp import error
from pyfms.utils.ctypes_utils import set_array, set_c_bool, set_c_int, set_list, set_c_str, setNone


# enumerations used by horiz_interp_types.F90 (FMS)
_CONSERVATIVE = 1
_BILINEAR = 2

_libpath = None
_lib = None

_cFMS_create_xgrid_2dx2d_order1 = None
_get_maxxgrid = None
_cFMS_horiz_interp_init = None
_cFMS_horiz_interp_2d_new_cdouble = None
_cFMS_horiz_interp_2d_new_cfloat = None
_cFMS_get_i_src = None
_cFMS_get_j_src = None
_cFMS_get_i_dst = None
_cFMS_get_j_dst = None
_cFMS_get_nlon_src = None
_cFMS_get_nlat_src = None
_cFMS_get_nlon_dst = None
_cFMS_get_nlat_dst = None
_cFMS_get_interp_method = None
_cFMS_get_area_frac_dst_double = None
_cFMS_get_nxgrid = None
_cFMS_horiz_interp_news = {}


def get_maxxgrid() -> np.int32:

    """
    Defines the maximum number of exchange cells
    that can be created by create_xgrid_*
    """

    return _get_maxxgrid()


def create_xgrid_2dx2d_order1(
    nlon_src: int,
    nlat_src: int,
    nlon_tgt: int,
    nlat_tgt: int,
    lon_src: npt.NDArray[np.float64],
    lat_src: npt.NDArray[np.float64],
    lon_tgt: npt.NDArray[np.float64],
    lat_tgt: npt.NDArray[np.float64],
    mask_src: npt.NDArray[np.float64],
) -> dict:

    """
    Creates the exchange grid that can be used
    for first order conservative interpolation
    """

    maxxgrid = get_maxxgrid()

    arglist = []
    set_c_int(nlon_src, arglist)
    set_c_int(nlat_src, arglist)
    set_c_int(nlon_tgt, arglist)
    set_c_int(nlat_tgt, arglist)
    set_array(lon_src, arglist)
    set_array(lat_src, arglist)
    set_array(lon_tgt, arglist)
    set_array(lat_tgt, arglist)
    set_array(mask_src, arglist)
    set_c_int(maxxgrid, arglist)
    i_src = set_array(np.zeros(maxxgrid, dtype=np.int32), arglist)
    j_src = set_array(np.zeros(maxxgrid, dtype=np.int32), arglist)
    i_tgt = set_array(np.zeros(maxxgrid, dtype=np.int32), arglist)
    j_tgt = set_array(np.zeros(maxxgrid, dtype=np.int32), arglist)
    xarea = set_array(np.zeros(maxxgrid, dtype=np.float64), arglist)

    nxgrid = _cFMS_create_xgrid_2dx2d_order1(*arglist)

    return {
        "nxgrid": nxgrid,
        "i_src": i_src[:nxgrid],
        "j_src": j_src[:nxgrid],
        "i_tgt": i_tgt[:nxgrid],
        "j_tgt": j_tgt[:nxgrid],
        "xarea": xarea[:nxgrid],
    }


def init(ninterp: int = None):

    """
    initializes horiz_interp in FMS
    """

    arglist = []
    set_c_int(ninterp, arglist)

    _cFMS_horiz_interp_init(*arglist)


#TODO names should be consistent between in/src and out/dst
#this problem is in part to inconsistency in FMS
def get_weights(
    lon_in: npt.NDArray[np.float32|np.float64],
    lat_in: npt.NDArray[np.float32|np.float64],
    lon_out: npt.NDArray[np.float32|np.float64],
    lat_out: npt.NDArray[np.float32|np.float64],
    mask_in: npt.NDArray[np.float32|np.float64] = None,
    mask_out: npt.NDArray[np.float32|np.float64] = None,
    interp_method: str = None,
    verbose: int = 0,
    max_dist: np.float32|np.float64 = None,
    src_modulo: bool = False,
    is_latlon_in: bool = False,
    is_latlon_out: bool = False,
) -> int:
    """
    Performs horizontal interpolation for 2D data
    using double precision floating point numbers.
    """

    try:
        _cFMS_horiz_interp_new = _cFMS_horiz_interp_news[lon_in.dtype.name]
    except:
        raise RuntimeError(f"horiz_interp.get_weights: grid of type {lon_in.dtype} not supported")

    arglist = []
    set_array(lon_in, arglist)
    set_array(lat_in, arglist)
    set_list(lat_in.shape, np.int32, arglist)
    set_array(lon_out, arglist)
    set_array(lat_out, arglist)
    set_list(lat_out.shape, np.int32, arglist)
    set_array(mask_in, arglist)
    set_array(mask_out, arglist)
    set_c_str(interp_method, arglist)
    set_c_int(verbose, arglist)
    set_array(max_dist, arglist)
    set_c_bool(src_modulo, arglist)
    set_c_bool(is_latlon_in, arglist)
    set_c_bool(is_latlon_out, arglist)

    return _cFMS_horiz_interp_new(*arglist)


def get_nxgrid(interp_id: int):

    arglist = []
    set_c_int(interp_id, arglist)
    nxgrid = set_c_int(0, arglist)

    _cFMS_get_nxgrid(*arglist)
    return nxgrid.value


def get_nlon_src(interp_id: int):

    arglist = []
    set_c_int(interp_id, arglist)
    nlon_src = set_c_int(0, arglist)

    _cFMS_get_nlon_src(*arglist)
    return nlon_src.value


def get_nlat_src(interp_id: int):

    arglist = []
    set_c_int(interp_id, arglist)
    nlat_src = set_c_int(0, arglist)

    _cFMS_get_nlat_src(*arglist)
    return nlat_src.value


def get_nlon_dst(interp_id: int):

    arglist = []
    set_c_int(interp_id, arglist)
    nlon_dst = set_c_int(0, arglist)

    _cFMS_get_nlon_dst(*arglist)
    return nlon_dst.value


def get_nlat_dst(interp_id: int):

    arglist = []
    set_c_int(interp_id, arglist)
    nlat_dst = set_c_int(0, arglist)

    _cFMS_get_nlat_dst(*arglist)
    return nlat_dst.value


def get_i_src(interp_id: int):

    nxgrid = get_nxgrid(interp_id)

    arglist = []
    set_c_int(interp_id, arglist)
    i_src = set_array(np.zeros(nxgrid, dtype=np.int32), arglist)

    _cFMS_get_i_src(*arglist)

    return i_src

    
def get_j_src(interp_id: int):

    nxgrid = get_nxgrid(interp_id)

    arglist = []
    set_c_int(interp_id, arglist)
    j_src = set_array(np.zeros(nxgrid, dtype=np.int32), arglist)

    _cFMS_get_j_src(*arglist)
    return j_src
    

def get_i_dst(interp_id: int):

    nxgrid = get_nxgrid(interp_id)
    
    arglist = []
    set_c_int(interp_id, arglist)
    i_dst = set_array(np.zeros(nxgrid, dtype=np.int32), arglist)

    _cFMS_get_i_dst(*arglist)
    return i_dst


def get_j_dst(interp_id: int):

    nxgrid = get_nxgrid(interp_id)
    
    arglist = []
    set_c_int(interp_id, arglist)
    j_dst = set_array(np.zeros(nxgrid, dtype=np.int32), arglist)

    _cFMS_get_j_dst(*arglist)
    return j_dst


def get_area_frac_dst(interp_id: int):

    nxgrid = get_nxgrid(interp_id)
    
    arglist = []
    set_c_int(interp_id, arglist)
    area_frac_dst = set_array(np.zeros(nxgrid, dtype=np.float64), arglist)
    
    _cFMS_get_area_frac_dst_double(*arglist)
    return area_frac_dst


def get_interp_method(interp_id: int):

    interp_method_dict = {1: "conservative",
                          2: "bilinear",
                          3: "spherical",
                          4: "bicubic"
    }
    
    arglist = []
    set_c_int(interp_id, arglist)
    interp_method = set_c_int(0, arglist)

    _cFMS_get_interp_method(*arglist)

    return interp_method_dict[interp_method.value]


def _init_functions():

    global _cFMS_create_xgrid_2dx2d_order1
    global _get_maxxgrid
    global _cFMS_horiz_interp_init
    global _cFMS_horiz_interp_news
    global _cFMS_horiz_interp_new_2d_cdouble
    global _cFMS_horiz_interp_new_2d_cfloat
    global _cFMS_get_wti_cfloat
    global _cFMS_get_wti_cdouble
    global _cFMS_get_wtj_cfloat
    global _cFMS_get_wtj_cdouble
    global _cFMS_get_i_src
    global _cFMS_get_j_src
    global _cFMS_get_i_dst
    global _cFMS_get_j_dst
    global _cFMS_get_nlon_src
    global _cFMS_get_nlat_src
    global _cFMS_get_nlon_dst
    global _cFMS_get_nlat_dst
    global _cFMS_get_interp_method
    global _cFMS_get_area_frac_dst_double
    global _cFMS_get_nxgrid
        

    _cFMS_create_xgrid_2dx2d_order1 = _lib.cFMS_create_xgrid_2dx2d_order1
    _get_maxxgrid = _lib.get_maxxgrid
    _cFMS_horiz_interp_init = _lib.cFMS_horiz_interp_init
    _cFMS_horiz_interp_new_2d_cdouble = _lib.cFMS_horiz_interp_new_2d_cdouble
    _cFMS_horiz_interp_new_2d_cfloat = _lib.cFMS_horiz_interp_new_2d_cfloat

    _cFMS_get_wti_cfloat = _lib.cFMS_get_wti_cfloat
    _cFMS_get_wti_cdouble = _lib.cFMS_get_wti_cdouble
    _cFMS_get_wtj_cfloat = _lib.cFMS_get_wtj_cfloat
    _cFMS_get_wtj_cdouble = _lib.cFMS_get_wtj_cdouble

    _cFMS_get_i_src = _lib.cFMS_get_i_src
    _cFMS_get_j_src = _lib.cFMS_get_j_src
    _cFMS_get_i_dst = _lib.cFMS_get_i_dst
    _cFMS_get_j_dst = _lib.cFMS_get_j_dst
    _cFMS_get_nlon_src = _lib.cFMS_get_nlon_src
    _cFMS_get_nlat_src = _lib.cFMS_get_nlat_src
    _cFMS_get_nlon_dst = _lib.cFMS_get_nlon_dst
    _cFMS_get_nlat_dst = _lib.cFMS_get_nlat_dst
    _cFMS_get_nxgrid = _lib.cFMS_get_nxgrid
    _cFMS_get_interp_method = _lib.cFMS_get_interp_method
    _cFMS_get_area_frac_dst_double = _lib.cFMS_get_area_frac_dst_cdouble
    
    _cFMS_horiz_interp_news = {"float32": _cFMS_horiz_interp_new_2d_cfloat,
                               "float64": _cFMS_horiz_interp_new_2d_cdouble
    }
                                          
    _functions.define(_lib)


def _init(libpath: str, lib: Any):

    """
    Sets _libpath and _lib module variables associated
    with the loaded cFMS library.  This function is
    to be used internally by the cfms module
    """

    global _libpath, _lib

    _libpath = libpath
    _lib = lib

    _init_functions()
