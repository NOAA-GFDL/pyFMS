from typing import Any

import numpy as np
import numpy.typing as npt

from pyfms.py_horiz_interp import _functions
from pyfms.utils.ctypes_utils import (
    set_array,
    set_c_bool,
    set_c_double,
    set_c_float,
    set_c_int,
    set_c_str,
)
from pyfms.py_mpp.domain import Domain


# enumerations used by horiz_interp_types.F90 (FMS)
_CONSERVATIVE = 1
_BILINEAR = 2

_libpath = None
_lib = None

_cFMS_create_xgrid_2dx2d_order1 = None
_get_maxxgrid = None
_cFMS_horiz_interp_init = None
_cFMS_horiz_interp_end = None
_cFMS_horiz_interp_2d_new_cdouble = None
_cFMS_horiz_interp_2d_new_cfloat = None
_cFMS_horiz_interp_2d_base_cdouble = None
_cFMS_horiz_interp_2d_base_cfloat = None
_cFMS_horiz_interp_read_weights_conserve = None
_cFMS_get_i_src = None
_cFMS_get_j_src = None
_cFMS_get_i_dst = None
_cFMS_get_j_dst = None
_cFMS_get_nlon_src = None
_cFMS_get_nlat_src = None
_cFMS_get_nlon_dst = None
_cFMS_get_nlat_dst = None
_cFMS_get_interp_method = None
_cFMS_get_xgrid_area = None
_cFMS_get_area_frac_dst_double = None
_cFMS_get_nxgrid = None
_cFMS_horiz_interp_new_dict = {}
_cFMS_horiz_interp_base_dict = {}


def get_maxxgrid() -> np.int32:

    """
    Defines the maximum number of exchange cells
    that can be created by create_xgrid_*
    """

    return _get_maxxgrid()


def create_xgrid_2dx2d_order1(
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
    set_c_int(lon_src.shape[0], arglist)
    set_c_int(lon_src.shape[1], arglist)
    set_c_int(lon_tgt.shape[0], arglist)
    set_c_int(lon_tgt.shape[1], arglist)
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


def end():

    """
    Calls cFMS_horiz_interp_end to deallocate interp
    """

    _cFMS_horiz_interp_end()


# TODO names should be consistent between in/src and out/dst
# this problem is in part to inconsistency in FMS
def get_weights(
    lon_in: npt.NDArray[np.float32 | np.float64],
    lat_in: npt.NDArray[np.float32 | np.float64],
    lon_out: npt.NDArray[np.float32 | np.float64],
    lat_out: npt.NDArray[np.float32 | np.float64],
    mask_in: npt.NDArray[np.float32 | np.float64] = None,
    mask_out: npt.NDArray[np.float32 | np.float64] = None,
    nlon_in: int = None,
    nlat_in: int = None,
    nlon_out: int = None,
    nlat_out: int = None,
    interp_method: str = None,
    verbose: int = 0,
    max_dist: np.float32 | np.float64 = None,
    src_modulo: bool = False,
    is_latlon_in: bool = False,
    is_latlon_out: bool = False,
    save_weights_as_fregrid: bool = False,
    convert_cf_order: bool = True,
) -> int:
    """
    Performs horizontal interpolation for 2D data
    using double precision floating point numbers.
    """

    try:
        _cFMS_horiz_interp_new = _cFMS_horiz_interp_new_dict[lon_in.dtype.name]
    except Exception:
        raise RuntimeError(
            f"horiz_interp.new: grid of type {lon_in.dtype} not supported"
        )

    if nlon_in is None:
        nlon_in = lon_in.shape[0] - 1
    if nlat_in is None:
        nlat_in = lon_in.shape[1] - 1
    if nlon_out is None:
        nlon_out = lon_out.shape[0] - 1
    if nlat_out is None:
        nlat_out = lon_out.shape[1] - 1

    arglist = []
    set_c_int(nlon_in, arglist)
    set_c_int(nlat_in, arglist)
    set_c_int(nlon_out, arglist)
    set_c_int(nlat_out, arglist)
    set_array(lon_in, arglist)
    set_array(lat_in, arglist)
    set_array(lon_out, arglist)
    set_array(lat_out, arglist)
    set_array(mask_in, arglist)
    set_array(mask_out, arglist)
    set_c_str(interp_method, arglist)
    set_c_int(verbose, arglist)
    set_array(max_dist, arglist)
    set_c_bool(src_modulo, arglist)
    set_c_bool(is_latlon_in, arglist)
    set_c_bool(is_latlon_out, arglist)
    set_c_bool(save_weights_as_fregrid, arglist)
    set_c_bool(convert_cf_order, arglist)

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


def get_xgrid_area(interp_id: int):

    nxgrid = get_nxgrid(interp_id)
    arglist = []
    set_c_int(interp_id, arglist)
    xgrid_area = set_array(np.zeros(nxgrid, dtype=np.float64), arglist)

    _cFMS_get_xgrid_area(*arglist)
    return xgrid_area


def get_interp_method(interp_id: int):

    interp_method_dict = {
        1: "conservative",
        2: "bilinear",
        3: "spherical",
        4: "bicubic",
    }

    arglist = []
    set_c_int(interp_id, arglist)
    interp_method = set_c_int(0, arglist)

    _cFMS_get_interp_method(*arglist)

    return interp_method_dict[interp_method.value]


def interp(
    interp_id: int,
    data_in: npt.NDArray[np.float32 | np.float64],
    mask_in: npt.NDArray[np.float32 | np.float64] = None,
    mask_out: npt.NDArray[np.float32 | np.float64] = None,
    verbose: int = 0,
    missing_value: np.float32 | np.float64 = None,
    missing_permit: int = None,
    new_missing_handle: bool = None,
    convert_cf_order: bool = True,
) -> npt.NDArray[np.float32 | np.float64]:

    datatype = data_in.dtype
    try:
        _cFMS_horiz_interp_base = _cFMS_horiz_interp_base_dict[datatype.name]
    except Exception:
        raise RuntimeError(
            f"horiz_interp.interp: grid of type {datatype} not supported"
        )

    arglist = []

    nlon_dst = get_nlon_dst(interp_id)
    nlat_dst = get_nlat_dst(interp_id)

    set_c_real = set_c_float if datatype == np.float32 else set_c_double

    set_c_int(interp_id, arglist)
    set_array(data_in, arglist)
    if convert_cf_order:
        data_out = set_array(np.zeros((nlon_dst, nlat_dst), dtype=datatype), arglist)
    else:
        data_out = set_array(np.zeros((nlat_dst, nlon_dst), dtype=datatype), arglist)
    set_array(mask_in, arglist)
    set_array(mask_out, arglist)
    set_c_int(verbose, arglist)
    set_c_real(missing_value, arglist)
    set_c_int(missing_permit, arglist)
    set_c_bool(new_missing_handle, arglist)
    set_c_bool(convert_cf_order, arglist)

    _cFMS_horiz_interp_base(*arglist)

    return data_out


def read_weights_conserve(weight_filename: str,
                          weight_file_src: str,
                          nlon_src: int,
                          nlat_src: int,
                          domain: Domain = None,
                          nlon_tgt: int = None,
                          nlat_tgt: int = None,
                          src_tile: int = None):

    if domain is None:
        if nlon_tgt is None: cFMS_error(FATAL, "must provide nlon_tgt if Domain is not specified")
        if nlat_tgt is None: cFMS_error(FATAL, "must provide nlon_tgt if Domain is not specified")
        isc, iec, jsc, jec = 0, nlon_tgt-1, 0, nlat_tgt-1
    else:
        nlon_tgt = domain.xsize_c
        nlat_tgt = domain.ysize_c
        isc = domain.isc
        iec = domain.iec
        jsc = domain.jsc
        jec = domain.jec

    arglist = []
    set_c_str(weight_filename, arglist)
    set_c_str(weight_file_src, arglist)
    set_c_int(nlon_src, arglist)
    set_c_int(nlat_src, arglist)
    set_c_int(nlon_tgt, arglist)
    set_c_int(nlat_tgt, arglist)
    set_c_int(isc, arglist)
    set_c_int(iec, arglist)
    set_c_int(jsc, arglist)
    set_c_int(jec, arglist)
    set_c_int(src_tile, arglist)

    return _cFMS_horiz_interp_read_weights_conserve(*arglist)


def _init_functions():

    global _cFMS_create_xgrid_2dx2d_order1
    global _get_maxxgrid
    global _cFMS_horiz_interp_init
    global _cFMS_horiz_interp_end
    global _cFMS_horiz_interp_new_dict
    global _cFMS_horiz_interp_new_2d_cdouble
    global _cFMS_horiz_interp_new_2d_cfloat
    global _cFMS_horiz_interp_base_dict
    global _cFMS_horiz_interp_base_2d_cdouble
    global _cFMS_horiz_interp_base_2d_cfloat
    global _cFMS_horiz_interp_read_weights_conserve
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
    global _cFMS_get_xgrid_area
    global _cFMS_get_area_frac_dst_double
    global _cFMS_get_nxgrid

    _cFMS_create_xgrid_2dx2d_order1 = _lib.cFMS_create_xgrid_2dx2d_order1
    _get_maxxgrid = _lib.get_maxxgrid
    _cFMS_horiz_interp_init = _lib.cFMS_horiz_interp_init
    _cFMS_horiz_interp_end = _lib.cFMS_horiz_interp_end

    _cFMS_horiz_interp_new_2d_cdouble = _lib.cFMS_horiz_interp_new_2d_cdouble
    _cFMS_horiz_interp_new_2d_cfloat = _lib.cFMS_horiz_interp_new_2d_cfloat

    _cFMS_horiz_interp_base_2d_cdouble = _lib.cFMS_horiz_interp_base_2d_cdouble
    _cFMS_horiz_interp_base_2d_cfloat = _lib.cFMS_horiz_interp_base_2d_cfloat

    _cFMS_horiz_interp_read_weights_conserve = _lib.cFMS_horiz_interp_read_weights_conserve

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
    _cFMS_get_xgrid_area = _lib.cFMS_get_xgrid_area
    _cFMS_get_area_frac_dst_double = _lib.cFMS_get_area_frac_dst_cdouble

    _cFMS_horiz_interp_new_dict = {
        "float32": _cFMS_horiz_interp_new_2d_cfloat,
        "float64": _cFMS_horiz_interp_new_2d_cdouble,
    }

    _cFMS_horiz_interp_base_dict = {
        "float32": _cFMS_horiz_interp_base_2d_cfloat,
        "float64": _cFMS_horiz_interp_base_2d_cdouble,
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
