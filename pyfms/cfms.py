import ctypes
import os

import pyfms


class cfms:

    __libpath: str = os.path.dirname(__file__) + "/../cFMS/cLIBFMS/lib/libcFMS.so"
    __lib: type[ctypes.CDLL] = ctypes.cdll.LoadLibrary(__libpath)
    lib = None

    @classmethod
    def init(cls):
        pyfms.constants.setlib(cls.libpath(), cls.lib())
        pyfms.data_override.setlib(cls.libpath(), cls.lib())
        pyfms.fms.setlib(cls.libpath(), cls.lib())
        pyfms.diag_manager.setlib(cls.libpath(), cls.lib())
        pyfms.grid_utils.setlib(cls.libpath(), cls.lib())
        pyfms.horiz_interp.setlib(cls.libpath(), cls.lib())
        pyfms.mpp.setlib(cls.libpath(), cls.lib())
        pyfms.mpp_domains.setlib(cls.libpath(), cls.lib())

    @classmethod
    def changelib(cls, libpath: str):
        cls.__libpath = libpath
        cls.__lib = ctypes.cdll.LoadLibrary(cls.__libpath)
        cls.init()

    @classmethod
    def lib(cls) -> type[ctypes.CDLL]:
        return cls.__lib

    @classmethod
    def libpath(cls) -> str:
        return cls.__libpath
