import os

import pytest
from mpi4py import MPI

from pyfms import pyFMS


cfms_path = os.path.dirname(__file__) + "/../cFMS/cLIBFMS/lib/libcFMS.so"


@pytest.mark.create
def test_create_input_nml():
    inputnml = open("input.nml", "w")
    inputnml.close()

    assert os.path.isfile("input.nml")


@pytest.mark.parallel
def test_pyfms_init():

    assert os.path.exists(cfms_path)

    fcomm = MPI.COMM_WORLD.py2f()

    pyfmsobj = pyFMS(
        localcomm=fcomm,
        cFMS_path=cfms_path,
    )

    assert isinstance(pyfmsobj, pyFMS)

    pyfmsobj.pyfms_end()


@pytest.mark.remove
def test_remove_input_nml():
    os.remove("input.nml")
    assert not os.path.isfile("input.nml")
