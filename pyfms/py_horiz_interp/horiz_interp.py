from ctypes import POINTER, c_int32
from typing import Any, Optional

import numpy as np
import numpy.typing as npt

from pyfms.py_mpp.mpp import error
from pyfms.py_fms.fms import FATAL
from pyfms.py_horiz_interp import _functions
from pyfms.utils.ctypes_utils import NDPOINTERi32, set_array, set_c_int, set_c_bool, set_c_str, set_list, setNone

# enumerations used by horiz_interp_types.F90 (FMS)
_CONSERVATIVE = 1
_BILINEAR = 2

_libpath = None
_lib = None

_cFMS_create_xgrid_2dx2d_order1 = None
_get_maxxgrid = None
_cFMS_horiz_interp_init = None
_cFMS_set_current_interp = None
_cFMS_get_interp_cdouble = None
_cFMS_get_interp_cfloat = None
_cFMS_horiz_interp_2d_cdouble = None
_cFMS_horiz_interp_2d_cfloat = None


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
def horiz_interp_2d_double(
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

def horiz_interp_2d_float(
    lon_in_ptr: npt.NDArray[np.float32],
    lon_in_shape: list[int],
    lat_in_ptr: npt.NDArray[np.float32],
    lat_in_shape: list[int],
    lon_out_ptr: npt.NDArray[np.float32],
    lon_out_shape: list[int],
    lat_out_ptr: npt.NDArray[np.float32],
    lat_out_shape: list[int],
    interp_method: str,
    verbose: int = 0,
    max_dist: npt.NDArray[np.float32] = None,
    src_modulo: bool = False,
    mask_in_ptr: npt.NDArray[np.float32] = None,
    mask_out_ptr: npt.NDArray[np.float32] = None,
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

    ret_val = _cFMS_horiz_interp_2d_cfloat(*arglist)

def horiz_interp_get_interp_double(
        interp_id: int = None
) -> dict:
    """
    Returns the values of the fields in a horiz_interp_type instance as a dictionary
    Will return values corresponding to the given interp_id, regardless of the current interp
    """

    # get nxgrid first so we know how big our output variables will be
    arglist = []
    if interp_id is None:
        setNone(arglist)
    else:
        set_c_int(interp_id, arglist)
    setNone(arglist) # i_src
    setNone(arglist) # j_src
    setNone(arglist) # i_dst
    setNone(arglist) # j_dst
    setNone(arglist) # area_frac_dst
    setNone(arglist) # version
    nxgrid = set_c_int(-1, arglist) # nxgrid
    setNone(arglist) # nlon_src
    setNone(arglist) # nlat_src
    setNone(arglist) # nlon_dst
    setNone(arglist) # nlat_dst
    setNone(arglist) # is_allocated
    interp_method = set_c_int(0, arglist) # interp_method

    ret_val = _cFMS_get_interp_cdouble(*arglist)

    arglist = []
    if interp_id is None:
        setNone(arglist)
    else:
        set_c_int(interp_id, arglist)
    # certain fields are only allocated by either the bilinear or conservative
    if interp_method.value == _CONSERVATIVE:
        i_src = set_array(np.zeros(nxgrid.value, dtype=np.int32), arglist)
        j_src = set_array(np.zeros(nxgrid.value, dtype=np.int32), arglist)
        i_dst = set_array(np.zeros(nxgrid.value, dtype=np.int32), arglist)
        j_dst = set_array(np.zeros(nxgrid.value, dtype=np.int32), arglist)
        area_frac_dst = set_array(np.zeros(nxgrid.value, dtype=np.float64), arglist)
    elif interp_method.value == _BILINEAR:
        i_src = setNone(arglist)
        j_src = setNone(arglist)
        i_dst = setNone(arglist)
        j_dst = setNone(arglist)
        area_frac_dst = setNone(arglist)
    else:
        error(FATAL, f"invalid interp_method value: {interp_method.value}")
    version = set_c_int(0, arglist)
    nxgrid = set_c_int(0, arglist)
    nlon_src = set_c_int(0, arglist)
    nlat_src = set_c_int(0, arglist)
    nlon_dst = set_c_int(0, arglist)
    nlat_dst = set_c_int(0, arglist)
    is_allocated = set_c_bool(False, arglist)
    interp_method = set_c_int(0, arglist)

    _cFMS_get_interp_cdouble(*arglist)

    if(interp_method.value == _BILINEAR):
        arglist = []
        if interp_id is None:
            setNone(arglist)
        else:
            set_c_int(interp_id, arglist)
        wti = set_array(np.zeros( (nlon_dst.value, nlat_dst.value, 2), dtype=np.float64), arglist)
        _cFMS_get_wti_cdouble(*arglist)

        arglist = []
        if interp_id is None:
            setNone(arglist)
        else:
            set_c_int(interp_id, arglist)
        wtj = set_array(np.zeros( (nlon_dst.value, nlat_dst.value, 2), dtype=np.float64), arglist)
        _cFMS_get_wtj_cdouble(*arglist)


    return dict(
        interp_id=interp_id,
        i_src=i_src,
        j_src=j_src,
        i_dst=i_dst,
        j_dst=j_dst,
        area_frac_dst=area_frac_dst,
        nxgrid=nxgrid.value,
        version=version.value,
        nlon_src=nlon_src.value,
        nlat_src=nlat_src.value,
        nlon_dst=nlon_dst.value,
        nlat_dst=nlat_dst.value,
        is_allocated=is_allocated.value,
        interp_method=interp_method.value,
        wti=wti if interp_method.value == _BILINEAR else None,
        wtj=wtj if interp_method.value == _BILINEAR else None,
    )

def horiz_interp_get_interp_float(
        interp_id: int = None
) -> dict:
    """
    Returns the values of the fields in a horiz_interp_type instance as a dictionary
    Will return values corresponding to the given interp_id, regardless of the current interp
    """
    # get nxgrid first so we know how big our output variables will be
    arglist = []
    if interp_id is None:
        setNone(arglist)
    else:
        set_c_int(interp_id, arglist)
    setNone(arglist) # i_src
    setNone(arglist) # j_src
    setNone(arglist) # i_dst
    setNone(arglist) # j_dst
    setNone(arglist) # area_frac_dst
    setNone(arglist) # version
    nxgrid = set_c_int(-1, arglist) # nxgrid
    setNone(arglist) # nlon_src
    setNone(arglist) # nlat_src
    setNone(arglist) # nlon_dst
    setNone(arglist) # nlat_dst
    setNone(arglist) # is_allocated
    interp_method = set_c_int(0, arglist) # interp_method

    ret_val = _cFMS_get_interp_cfloat(*arglist)

    arglist = []
    if interp_id is None:
        setNone(arglist)
    else:
        set_c_int(interp_id, arglist)
    # certain fields are only allocated by either the bilinear or conservative
    if interp_method.value == _CONSERVATIVE:
        i_src = set_array(np.zeros(nxgrid.value, dtype=np.int32), arglist)
        j_src = set_array(np.zeros(nxgrid.value, dtype=np.int32), arglist)
        i_dst = set_array(np.zeros(nxgrid.value, dtype=np.int32), arglist)
        j_dst = set_array(np.zeros(nxgrid.value, dtype=np.int32), arglist)
        area_frac_dst = set_array(np.zeros(nxgrid.value, dtype=np.float32), arglist)
    elif interp_method.value == _BILINEAR:
        i_src = setNone(arglist)
        j_src = setNone(arglist)
        i_dst = setNone(arglist)
        j_dst = setNone(arglist)
        area_frac_dst = setNone(arglist)
    else:
        error(FATAL, f"invalid interp_method value: {interp_method.value}")
    version = set_c_int(0, arglist)
    nxgrid = set_c_int(0, arglist)
    nlon_src = set_c_int(0, arglist)
    nlat_src = set_c_int(0, arglist)
    nlon_dst = set_c_int(0, arglist)
    nlat_dst = set_c_int(0, arglist)
    is_allocated = set_c_bool(False, arglist)
    interp_method = set_c_int(0, arglist)

    _cFMS_get_interp_cfloat(*arglist)

    if(interp_method.value == _BILINEAR):
        arglist = []
        if interp_id is None:
            setNone(arglist)
        else:
            set_c_int(interp_id, arglist)
        wti = set_array(np.zeros( (nlon_dst.value, nlat_dst.value, 2), dtype=np.float32), arglist)
        _cFMS_get_wti_cfloat(*arglist)

        arglist = []
        if interp_id is None:
            setNone(arglist)
        else:
            set_c_int(interp_id, arglist)
        wtj = set_array(np.zeros( (nlon_dst.value, nlat_dst.value, 2), dtype=np.float32), arglist)
        _cFMS_get_wtj_cfloat(*arglist)


    return dict(
        interp_id=interp_id,
        i_src=i_src,
        j_src=j_src,
        i_dst=i_dst,
        j_dst=j_dst,
        area_frac_dst=area_frac_dst,
        nxgrid=nxgrid.value,
        version=version.value,
        nlon_src=nlon_src.value,
        nlat_src=nlat_src.value,
        nlon_dst=nlon_dst.value,
        nlat_dst=nlat_dst.value,
        is_allocated=is_allocated.value,
        interp_method=interp_method.value,
        wti=wti if interp_method.value == _BILINEAR else None,
        wtj=wtj if interp_method.value == _BILINEAR else None,
    )


def _init_functions():

    global _cFMS_create_xgrid_2dx2d_order1
    global _get_maxxgrid
    global _cFMS_horiz_interp_init
    global _cFMS_set_current_interp
    global _cFMS_horiz_interp_2d_cdouble
    global _cFMS_horiz_interp_2d_cfloat
    global _cFMS_get_interp_cdouble
    global _cFMS_get_interp_cfloat
    global _cFMS_get_wti_cfloat
    global _cFMS_get_wti_cdouble
    global _cFMS_get_wtj_cfloat
    global _cFMS_get_wtj_cdouble

    _cFMS_create_xgrid_2dx2d_order1 = _lib.cFMS_create_xgrid_2dx2d_order1
    _get_maxxgrid = _lib.get_maxxgrid
    _cFMS_horiz_interp_init = _lib.cFMS_horiz_interp_init
    _cFMS_set_current_interp = _lib.cFMS_set_current_interp
    _cFMS_horiz_interp_2d_cdouble = _lib.cFMS_horiz_interp_2d_cdouble
    _cFMS_horiz_interp_2d_cfloat = _lib.cFMS_horiz_interp_2d_cfloat
    _cFMS_get_interp_cdouble = _lib.cFMS_get_interp_cdouble
    _cFMS_get_interp_cfloat = _lib.cFMS_get_interp_cfloat
    _cFMS_get_wti_cfloat = _lib.cFMS_get_wti_cfloat
    _cFMS_get_wti_cdouble = _lib.cFMS_get_wti_cdouble
    _cFMS_get_wtj_cfloat = _lib.cFMS_get_wtj_cfloat
    _cFMS_get_wtj_cdouble = _lib.cFMS_get_wtj_cdouble

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
