from ctypes import CDLL, POINTER, byref, c_int

import numpy as np
import numpy.typing as npt


_libpath: str = None
_lib: type[CDLL] = None


def setlib(libpath: str, lib: type[CDLL]):

    """
    Sets _libpath and _lib module variables associated
    with the loaded cFMS library.  This function is
    to be used internally by the cfms module
    """

    global _libpath, _lib

    _libpath = libpath
    _lib = lib


def get_grid_area(
    nlon: int,
    nlat: int,
    lon: npt.NDArray[np.float64],
    lat: npt.NDArray[np.float64],
) -> npt.NDArray[np.float64]:

    """
    Returns the cell areas of grids defined
    on lon and lat
    """

    ncells = nlon * nlat
    ngridpts = (nlon + 1) * (nlat + 1)

    nlon_t = c_int
    nlat_t = c_int
    lon_ndp = np.ctypeslib.ndpointer(
        dtype=np.float64, shape=(ngridpts), flags="C_CONTIGUOUS"
    )
    lat_ndp = np.ctypeslib.ndpointer(
        dtype=np.float64, shape=(ngridpts), flags="C_CONTIGUOUS"
    )
    area_ndp = np.ctypeslib.ndpointer(
        dtype=np.float64, shape=(ncells), flags="C_CONTIGUOUS"
    )

    nlon_c = nlon_t(nlon)
    nlat_c = nlat_t(nlat)
    area = np.zeros(ncells, dtype=np.float64)

    _get_grid_area = _lib.cFMS_get_grid_area

    _get_grid_area.restype = None
    _get_grid_area.argtypes = [
        POINTER(nlon_t),
        POINTER(nlat_t),
        lon_ndp,
        lat_ndp,
        area_ndp,
    ]

    nlon_c = nlon_t(nlon)
    nlat_c = nlat_t(nlat)

    _get_grid_area(byref(nlon_c), byref(nlat_c), lon, lat, area)

    return area
