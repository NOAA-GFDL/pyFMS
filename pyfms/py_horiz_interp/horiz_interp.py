from ctypes import POINTER, c_int32
from typing import Any

import numpy as np
import numpy.typing as npt

from pyfms.py_horiz_interp import _functions
from pyfms.utils.ctypes_utils import NDPOINTERi32, set_array, set_c_int, set_c_bool, set_list


_libpath = None
_lib = None

_cFMS_create_xgrid_2dx2d_order1 = None
_get_maxxgrid = None
_cFMS_horiz_interp_init = None
_cFMS_set_current_interp = None


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


def set_current_interp(interp_id: int = None):

    arglist = []
    set_c_int(interp_id, arglist)

    _cFMS_set_current_interp(*arglist)

    
# TODO shape arguments are not really needed
def horiz_interp_2d_cdouble(
    lon_in_ptr: npt.NDArray[np.float64],
    lon_in_shape: list[int],
    lat_in_ptr: npt.NDArray[np.float64],
    lat_in_shape: list[int],
    lon_out_ptr: npt.NDArray[np.float64],
    lon_out_shape: list[int],
    lat_out_ptr: npt.NDArray[np.float64],
    lat_out_shape: list[int],
    interp_method: str,
    verbose: int = 0,
    max_dist: npt.NDArray[np.float64] = None,
    src_modulo: bool = False,
    mask_in_ptr: npt.NDArray[np.float64] = None,
    mask_out_ptr: npt.NDArray[np.float64] = None,
    is_latlon_in: bool = False,
    is_latlon_out: bool = False,
) -> int:
    """
    Performs horizontal interpolation for 2D data
    using double precision floating point numbers.
    """

    npptr = np.ctypeslib.ndpointer
    C = "C_CONTIGUOUS"

    arglist = []
    set_array(lon_in_ptr, arglist)
    set_list( lon_in_shape, np.int32, arglist)
    set_array(lat_in_ptr, arglist)
    set_list( lat_in_shape, np.int32, arglist)
    set_array(lon_out_ptr, arglist)
    set_list( lon_out_shape, np.int32, arglist)
    set_array(lat_out_ptr, arglist)
    set_list( lat_out_shape, np.int32, arglist)
    interp_method = interp_method.encode('utf-8')
    set_array(interp_method, arglist)
    set_c_int(verbose, arglist)
    set_array(max_dist, arglist)
    set_c_bool(src_modulo, arglist)
    set_array(mask_in_ptr, arglist)
    set_array(mask_out_ptr, arglist)
    set_c_bool(is_latlon_in, arglist)
    set_c_bool(is_latlon_out, arglist)

    ret_val = _cFMS_horiz_interp_2d_cdouble(*arglist)


def _init_functions():

    global _cFMS_create_xgrid_2dx2d_order1
    global _get_maxxgrid
    global _cFMS_horiz_interp_init
    global _cFMS_set_current_interp
    global _cFMS_horiz_interp_2d_cdouble
    global _cFMS_horiz_interp_2d_cfloat

    _cFMS_create_xgrid_2dx2d_order1 = _lib.cFMS_create_xgrid_2dx2d_order1
    _get_maxxgrid = _lib.get_maxxgrid
    _cFMS_horiz_interp_init = _lib.cFMS_horiz_interp_init
    _cFMS_set_current_interp = _lib.cFMS_set_current_interp
    _cFMS_horiz_interp_2d_cdouble = _lib.cFMS_horiz_interp_2d_cdouble
    _cFMS_horiz_interp_2d_cfloat = _lib.cFMS_horiz_interp_2d_cfloat

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
