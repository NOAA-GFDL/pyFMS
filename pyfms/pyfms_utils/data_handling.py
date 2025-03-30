#!/usr/bin/env python3

import ctypes
from typing import Tuple

import numpy as np
import numpy.typing as npt


"""
This module allows for conversion between Python object and ctypes objects.
for use in the C based methods which wrap the Fortan FMS source methods.

Array methods: Will return an instance of the object passed and a pointer to
               the object. Arrays are mutable types in Python and do not
               require the a ctypes object to wrap it. If the array object
               is updated by the method the original Python object will
               also contain these updates

Scalar methods: Will return a reference to a ctypes object wrapping the passed
                Python object and a pointer to the new ctypes object.
                Scalar Python types are not mutable, and if method calling a
                pyFMS_data_handling method is expected to update the passed
                Python object, the calling method should not only create an
                explicit ctypes object to wrap passed Python object, but also
                return the value of the ctypes object to update the value.

All passed in NumPy arrays must make use of the "FORTRAN" flag during
initialization

Example: Wrapping C function that updates an integer and an array

def wrapper_func(py_scalar_obj: int, py_array_obj: npt.NDArray[int])-> int:
    _c_func = clib.c_func

    c_scalar_obj = ctypes.c_int(py_scalar_obj)
    c_array_p, c_array_t = setarray_Cint32(py_array_obj)

    _c_func.argtypes = [ctype.POINTER(ctype.c_int), c_array_t]
    _c_func.restype = None

    _c_func(ctypes.byref(c_scalar_obj), c_array_p)

    return c_scalar_obj.value


x = # some value
var_array = # some numpy array

x = wrapper_func(x, var_array)
"""


"""
Array setting methods
"""


def set_ndpointer(arg: npt.NDArray) -> np.ctypeslib.ndpointer:
    c_type = np.ctypeslib.as_ctypes_type(arg.dtype)
    return np.ctypeslib.ndpointer(
        dtype=c_type, ndim=arg.ndim, shape=arg.shape, flags="FORTRAN"
    )


def setarray_Cbool(
    arg: npt.NDArray[np.bool_],
) -> Tuple[npt.NDArray[np.bool_], np.ctypeslib.ndpointer]:
    if arg is None:
        return arg, ctypes.POINTER(ctypes.c_bool)
    else:
        return arg, set_ndpointer(arg)


def setarray_Cdouble(
    arg: npt.NDArray[np.float64],
) -> Tuple[npt.NDArray[np.float64], np.ctypeslib.ndpointer]:
    if arg is None:
        return arg, ctypes.POINTER(ctypes.c_double)
    else:
        return arg, set_ndpointer(arg)


def setarray_Cfloat(
    arg: npt.NDArray[np.float32],
) -> Tuple[npt.NDArray[np.float32], np.ctypeslib.ndpointer]:
    if arg is None:
        return arg, ctypes.POINTER(ctypes.c_float)
    else:
        return arg, set_ndpointer(arg)


def setarray_Cint32(
    arg: npt.NDArray[np.int32],
) -> Tuple[npt.NDArray[np.int32], np.ctypeslib.ndpointer]:
    if arg is None:
        return arg, ctypes.POINTER(ctypes.c_int)
    return arg, set_ndpointer(arg)


"""
set_multipointer:
    For converting NumPy arrays to pointer equivalent
    This method is able to convert a Numpy array of
    up to 5 dimensions to quintuple pointer (*****).

    If an array of <= 1 or > 5 dimensions is passed
    as an argument, the method will default to the
    returning the passed array and the result of a
    pass to set_ndpointer.

    This method is expected to be slow, and when
    possible avoided.
"""


def set_multipointer(arg: npt.NDArray, num_ptr: int) -> Tuple:
    if arg is not None:
        c_type = np.ctypeslib.as_ctypes_type(arg.dtype)
    match num_ptr:
        case 2:
            if arg is not None:
                arg_ptr = (ctypes.POINTER(c_type) * arg.shape[0])()
                for i in range(arg.shape[0]):
                    arg_ptr[i] = arg[i].ctypes.data_as(ctypes.POINTER(c_type))
                return arg_ptr, ctypes.POINTER(ctypes.POINTER(c_type))
            else:
                return arg, ctypes.POINTER(ctypes.POINTER(ctypes.c_int))
        case 3:
            if arg is not None:
                arg_ptr = (ctypes.POINTER(ctypes.POINTER(c_type)) * arg.shape[0])()
                for i in range(arg.shape[0]):
                    arg_ptr[i] = (ctypes.POINTER(c_type) * arg.shape[1])()
                    for j in range(arg.shape[1]):
                        arg_ptr[i][j] = arg[i][j].ctypes.data_as(ctypes.POINTER(c_type))
                return arg_ptr, ctypes.POINTER(ctypes.POINTER(ctypes.POINTER(c_type)))
            else:
                return arg, ctypes.POINTER(ctypes.POINTER(ctypes.POINTER(ctypes.c_int)))
        case 4:
            if arg is not None:
                arg_ptr = (
                    ctypes.POINTER(ctypes.POINTER(ctypes.POINTER(c_type)))
                    * arg.shape[0]
                )()
                for i in range(arg.shape[0]):
                    arg_ptr[i] = (
                        ctypes.POINTER(ctypes.POINTER(c_type)) * arg.shape[1]
                    )()
                    for j in range(arg.shape[1]):
                        arg_ptr[i][j] = (ctypes.POINTER(c_type) * arg.shape[2])()
                        for k in range(arg.shape[2]):
                            arg_ptr[i][j][k] = arg[i][j][k].ctypes.data_as(
                                ctypes.POINTER(c_type)
                            )
                return arg_ptr, ctypes.POINTER(
                    ctypes.POINTER(ctypes.POINTER(ctypes.POINTER(c_type)))
                )
            else:
                return arg, ctypes.POINTER(
                    ctypes.POINTER(ctypes.POINTER(ctypes.POINTER(ctypes.c_int)))
                )
        case 5:
            if arg is not None:
                arg_ptr = (
                    ctypes.POINTER(
                        ctypes.POINTER(ctypes.POINTER(ctypes.POINTER(c_type)))
                    )
                    * arg.shape[0]
                )()
                for i in range(arg.shape[0]):
                    arg_ptr[i] = (
                        ctypes.POINTER(ctypes.POINTER(ctypes.POINTER(c_type)))
                        * arg.shape[1]
                    )()
                    for j in range(arg.shape[1]):
                        arg_ptr[i][j] = (
                            ctypes.POINTER(ctypes.POINTER(c_type)) * arg.shape[2]
                        )()
                        for k in range(arg.shape[2]):
                            arg_ptr[i][j][k] = (ctypes.POINTER(c_type) * arg.shape[3])()
                            for n in range(arg.shape[3]):
                                arg_ptr[i][j][k][n] = arg[i][j][k][n].ctypes.data_as(
                                    ctypes.POINTER(c_type)
                                )
                return arg_ptr, ctypes.POINTER(
                    ctypes.POINTER(
                        ctypes.POINTER(ctypes.POINTER(ctypes.POINTER(c_type)))
                    )
                )
            else:
                return arg, ctypes.POINTER(
                    ctypes.POINTER(
                        ctypes.POINTER(ctypes.POINTER(ctypes.POINTER(ctypes.c_int)))
                    )
                )
        case _:
            if arg is not None:
                return arg, set_ndpointer(arg)
            else:
                return arg, ctypes.POINTER(ctypes.c_int)


"""
Scalar setting methods
"""


def setscalar_Cbool(arg) -> Tuple:
    if ctypes.c_bool == type(arg) or arg is None:
        return arg, ctypes.POINTER(ctypes.c_bool)
    else:
        return ctypes.c_bool(arg), ctypes.POINTER(ctypes.c_bool)


def set_Cchar(arg) -> Tuple:
    if arg is None:
        return arg, ctypes.c_char_p
    else:
        return ctypes.c_char_p(arg.encode("utf-8")), ctypes.c_char_p


def setscalar_Cdouble(arg) -> Tuple:
    if ctypes.c_double == type(arg) or arg is None:
        return arg, ctypes.POINTER(ctypes.c_double)
    else:
        return ctypes.c_double(arg), ctypes.POINTER(ctypes.c_double)


def setscalar_Cfloat(arg) -> Tuple:
    if ctypes.c_float == type(arg) or arg is None:
        return arg, ctypes.POINTER(ctypes.c_float)
    else:
        return ctypes.c_float(arg), ctypes.POINTER(ctypes.c_float)


def setscalar_Cint32(arg) -> Tuple:
    if ctypes.c_int == type(arg) or arg is None:
        return arg, ctypes.POINTER(ctypes.c_int)
    else:
        return ctypes.c_int(arg), ctypes.POINTER(ctypes.c_int)
