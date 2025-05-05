import os
import sys

import pytest

import pyfms

curr_dir = os.path.dirname(os.path.abspath(__file__))
par_dir = os.path.dirname(curr_dir)


def test_write_module():
    myfile = open("module1.py", "w")
    myfile.write(
        """
import pyfms
class Module1Class():
    module1_lib_id = id(pyfms.cfms.lib())
        """
    )
    myfile.close()


def test_share_same_library():
    assert id(pyfms.cfms.lib()) == id(pyfms.mpp_domains.lib())


def test_load_library_same_object():
    sys.path.append(par_dir)
    import module1

    myclass = module1.Module1Class()
    assert id(pyfms.cfms.lib()) == myclass.module1_lib_id


@pytest.mark.xfail
def test_library_load_fail():
    pyfms.cfms.changelib(libpath="do_not_exist")


def test_remove_module():
    os.remove("module1.py")


if __name__ == "__main__":
    test_write_module()
