import ctypes

import pyfms


_libpath = None
_lib = None


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

    if _lib is not None:
        ctypes.CDLL(None).dlclose(_lib._handle)
    # todo reset all _function parameters to None

    if libpath is None:
        _libpath = "libcFMS.so"
        try:
            _lib = ctypes.cdll.LoadLibrary(_libpath)
        except Exception as e:
            print(f"{type(e).__name__}: {e}")
            return
    else:
        _libpath = libpath
        _lib = ctypes.cdll.LoadLibrary(_libpath)

    pyfms.utils.constants._init(_libpath, _lib)
    pyfms.utils.grid_utils._init(_libpath, _lib)
    pyfms.py_data_override.data_override._init(_libpath, _lib)
    pyfms.py_fms.fms._init(_libpath, _lib)
    pyfms.py_diag_manager.diag_manager._init(_libpath, _lib)
    pyfms.py_horiz_interp.horiz_interp._init(_libpath, _lib)
    pyfms.py_mpp.mpp._init(_libpath, _lib)
    pyfms.py_mpp.mpp_domains._init(_libpath, _lib)


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
