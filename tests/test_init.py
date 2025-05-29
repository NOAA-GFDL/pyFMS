import os

import pytest

import pyfms


def test_library_loaded():

    """
    Test to ensure library loaded automatically
    """

    assert pyfms.cfms._lib is not None
    

def test_share_same_library():

    """
    Test to ensure pyfms modules use the same
    ctypes CDLL library object
    """

    assert id(pyfms.cfms._lib) == id(pyfms.mpp_domains._lib)


@pytest.mark.xfail
def test_library_load_fail():

    """
    Partial test to ensure the changelib function
    works
    """

    pyfms.cfms.changelib(libpath="do_not_exist")
