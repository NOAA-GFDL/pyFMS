import os

import numpy as np

import pyfms


def test_constants():

    inputnml = open("input.nml", "w")
    inputnml.close()

    pyfms.fms.init()

    answer = np.float64(3.14159265358979323846)

    assert type(pyfms.constants.PI) is np.float64
    assert pyfms.constants.PI == answer

    os.remove("input.nml")


if __name__ == "__main__":
    test_constants()
