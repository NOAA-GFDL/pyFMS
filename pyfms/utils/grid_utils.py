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
) -> npt.NDArray[np.float64]:

    """
    Returns the cell areas of grids defined
    on lon and lat
    """

    nlon, nlat = lon.shape
    
    arglist = []
    set_c_int(nlon, arglist)
    set_c_int(nlat, arglist)
    set_array(lon, arglist)
    set_array(lat, arglist)
    area = set_array(np.zeros((nlon, nlat), dtype=np.float64), arglist)

    _cFMS_get_grid_area(*arglist)

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
