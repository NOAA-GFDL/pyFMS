from typing import Any

import numpy as np
import numpy.typing as npt

from pyfms.py_horiz_interp import _functions
from pyfms.utils.ctypes_utils import set_array, set_c_int


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


def _init_functions():

    global _cFMS_create_xgrid_2dx2d_order1
    global _get_maxxgrid
    global _cFMS_horiz_interp_init
    global cFMS_set_current_interp

    _cFMS_create_xgrid_2dx2d_order1 = _lib.cFMS_create_xgrid_2dx2d_order1
    _get_maxxgrid = _lib.get_maxxgrid
    _cFMS_horiz_interp_init = _lib.cFMS_horiz_interp_init
    _cFMS_set_current_interp = _lib.cFMS_set_current_interp

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
