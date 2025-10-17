from ctypes import CDLL, POINTER, c_bool, c_char_p, c_double, c_float, c_int
from typing import Union

import numpy as np
import numpy.typing as npt


ctypelist = Union[type(c_int), type(c_float), type(c_double), type(c_bool)]

nptypelist = Union[np.int32, np.int64, np.float32, np.float64, np.bool]


def setNone(arglist) -> None:
    arglist.append(None)
    return None


def set_c_bool(arg: ctypelist | None, arglist: list) -> ctypelist | None:

    if arg is None:
        return setNone(arglist)

    arg_c = c_bool(arg)
    arglist.append(arg_c)
    return arg_c


def set_c_double(arg: ctypelist | None, arglist: list) -> ctypelist | None:

    if arg is None:
        return setNone(arglist)

    arg_c = c_double(arg)
    arglist.append(arg_c)
    return arg_c


def set_c_float(arg: ctypelist | None, arglist: list) -> ctypelist | None:

    if arg is None:
        return setNone(arglist)

    arg_c = c_float(arg)
    arglist.append(arg_c)
    return arg_c


def set_c_int(arg: ctypelist | None, arglist: list) -> ctypelist | None:

    if arg is None:
        return setNone(arglist)

    arg_c = c_int(arg)
    arglist.append(arg_c)
    return arg_c


def set_list(
    arg: list | None, nptype: nptypelist, arglist: list
) -> npt.ArrayLike | None:

    if arg is None:
        return setNone(arglist)

    arg_c = np.array(arg, dtype=nptype)
    arglist.append(arg_c)
    return arg_c


def set_c_str(arg: str | None, arglist: list) -> type(c_char_p) | None:

    if arg is None:
        return setNone(arglist)

    arg_c = c_char_p(arg.encode("utf-8"))
    arglist.append(arg_c)
    return arg_c


def set_array(arg: npt.ArrayLike | None, arglist: list) -> npt.ArrayLike | None:

    if arg is None:
        return setNone(arglist)

    if not arg.flags["FORC"]:
        arglist.append(np.ascontiguousarray(arg))
    else:
        arglist.append(arg)
    return arg


def get_constant_int(lib: type[CDLL], constant: str) -> int:
    return int(c_int.in_dll(lib, constant).value)


def get_constant_double(lib: type[CDLL], constant: str) -> int:
    return np.float64(c_double.in_dll(lib, constant).value)


def check_str(arg: str, length: int, whoami: str):

    if arg is not None:
        if len(arg) > length:
            raise RuntimeError(
                f"{whoami}: '{arg}' must be less than {length} cahracters"
            )


class NDPOINTERi32:

    """
    wrapper to np.ctypeslib.ndpointer for ints
    to accept None as function argument
    """

    def __init__(self, thispointer):
        self.thispointer = thispointer
        self.ctypes = c_int

    def from_param(self, obj):
        if obj is None:
            return POINTER(self.ctypes).from_param(obj)
        return self.thispointer.from_param(obj)


class NDPOINTERf:

    """
    wrapper to np.ctypeslib.ndpointer for floats
    to accept None as function argument
    """

    def __init__(self, thispointer):
        self.thispointer = thispointer
        self.ctypes = c_float

    def from_param(self, obj):
        if obj is None:
            return POINTER(self.ctypes).from_param(obj)
        return self.thispointer.from_param(obj)


class NDPOINTERd:

    """
    wrapper to np.ctypeslib.ndpointer for doubles
    to accept None as function argument
    """

    def __init__(self, thispointer):
        self.thispointer = thispointer
        self.ctypes = c_double

    def from_param(self, obj):
        if obj is None:
            return POINTER(self.ctypes).from_param(obj)
        return self.thispointer.from_param(obj)


ctypes_dict = {np.int32: c_int, np.float32: c_float, np.float64: c_double}


class NDPOINTER:

    """
    wrapper to np.ctypeslib.ndpointer for doubles
    to accept None as function argument
    """

    def __init__(self, dtype, ndim=None, shape=None, flags=None):
        self.ndpointer = np.ctypeslib.ndpointer(
            dtype=dtype, ndim=ndim, shape=shape, flags=flags
        )
        self.ctypes = ctypes_dict[dtype]

    def from_param(self, obj):
        if obj is None:
            return POINTER(self.ctypes).from_param(obj)
        return self.ndpointer.from_param(obj)
