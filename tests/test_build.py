import os


def test_shared_object_exists():
    assert os.path.exists(os.path.dirname(__file__) + "/../pyfms/cLIBFMS/lib/libcFMS.so")
