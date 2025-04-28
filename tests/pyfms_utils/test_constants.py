import os

import numpy as np

import pyfms


def test_constants():

    inputnml = open("input.nml", "w")
    inputnml.close()

    lib = pyfms.pyFMS().cFMS
    constants_obj = pyfms.constants(cFMS=lib)

    answer = np.float64(3.14159265358979323846)

    assert type(constants_obj.PI) is np.float64
    assert constants_obj.PI == answer

    os.remove("input.nml")
