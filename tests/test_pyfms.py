import os

import pytest
from mpi4py import MPI

import pyfms


@pytest.mark.create
def test_create_input_nml():
    inputnml = open("input.nml", "w")
    inputnml.close()
    assert os.path.isfile("input.nml")


@pytest.mark.parallel
def test_pyfms_init():

    fcomm = MPI.COMM_WORLD.py2f()

    pyfms.fms.init(localcomm=fcomm)

    pyfms.fms.end()


@pytest.mark.remove
def test_remove_input_nml():
    os.remove("input.nml")
    assert not os.path.isfile("input.nml")
