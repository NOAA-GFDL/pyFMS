from typing import Any

import numpy as np
import numpy.typing as npt

from pyfms.utils import _grid_utils_functions
from pyfms.utils.ctypes_utils import set_array, set_c_int


_libpath = None
_lib = None

_cFMS_get_grid_area = None


def get_grid_area(
    lon: npt.NDArray[np.float64],
    lat: npt.NDArray[np.float64],
    convert_cf_order: bool = False,
) -> npt.NDArray[np.float64]:

    """
    Returns the cell areas of grids defined
    on lon and lat
    """

    if convert_cf_order:
        nlon, nlat = lon.shape
    else:
        nlat, nlon = lon.shape
    nlat -= 1
    nlon -= 1

    arglist = []
    set_c_int(nlon, arglist)
    set_c_int(nlat, arglist)
    if convert_cf_order:
        set_array(lon.T, arglist)
        set_array(lat.T, arglist)
    else:
        set_array(lon, arglist)
        set_array(lat, arglist)
    area = set_array(np.zeros((nlat, nlon), dtype=np.float64), arglist)

    _cFMS_get_grid_area(*arglist)

    if convert_cf_order:
        return area.T
    return area


def _init_functions():

    global _cFMS_get_grid_area

    _grid_utils_functions.define(_lib)

    _cFMS_get_grid_area = _lib.cFMS_get_grid_area


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
