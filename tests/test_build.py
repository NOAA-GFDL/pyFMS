import os


def test_shared_object_exists():
    assert os.path.exists(os.path.dirname(__file__) + "/../cFMS/cLIBFMS/lib/libcFMS.so")
