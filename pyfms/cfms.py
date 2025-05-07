import ctypes
import os

import pyfms


_libpath: str = os.path.dirname(__file__) + "/../cFMS/cLIBFMS/lib/libcFMS.so"
_lib: type[ctypes.CDLL] = ctypes.cdll.LoadLibrary(_libpath)


def init(libpath: str = None):

    """
    Initializes the pyfms package by
    setting the cFMS library in all modules
    and initializing all constants in each
    module.  pyFMS will use the library
    compiled during installation.  Users can override
    this default library by specifying a cFMS library path
    """

    global _libpath, _lib

    if libpath is not None:
        _libpath = libpath
        _lib = ctypes.cdll.LoadLibrary(_libpath)

    pyfms.constants.setlib(_libpath, _lib)
    pyfms.data_override._init(_libpath, _lib)
    pyfms.fms.setlib(_libpath, _lib)
    pyfms.diag_manager._init(_libpath, _lib)
    pyfms.grid_utils.setlib(_libpath, _lib)
    pyfms.horiz_interp.setlib(_libpath, _lib)
    pyfms.mpp.setlib(_libpath, _lib)
    pyfms.mpp_domains.setlib(_libpath, _lib)

    pyfms.constants.constants_init()
    pyfms.fms.constants_init()
    pyfms.mpp_domains.constants_init()


def lib() -> type[ctypes.CDLL]:

    """
    returns the currently used ctypes.CDLL
    cFMS object
    """

    return _lib


def libpath() -> str:

    """
    returns the library path of the currently
    used cFMS object
    """

    return _libpath
