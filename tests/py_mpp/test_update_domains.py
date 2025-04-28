import os

import numpy as np
import pytest

from pyfms import mpp, mpp_domains, pyFMS


@pytest.mark.create
def test_create_input_nml():
    inputnml = open("input.nml", "w")
    inputnml.close()
    assert os.path.isfile("input.nml")


@pytest.mark.parallel
def test_update_domains():

    nx = 8
    ny = 8
    npes = 4
    whalo = 2
    ehalo = 2
    nhalo = 2
    shalo = 2
    domain_id = 0

    pyfms_obj = pyFMS(cFMS_path="./cFMS/libcFMS/.libs/libcFMS.so")
    mpp_obj = mpp(cFMS=pyfms_obj.cFMS)
    mpp_domains_obj = mpp_domains(cFMS=pyfms_obj.cFMS)

    global_indices = [0, (nx - 1), 0, (ny - 1)]

    layout = mpp_domains_obj.define_layout(global_indices=global_indices, ndivs=npes)

    domain = mpp_domains_obj.define_domains(
        global_indices=global_indices,
        layout=layout,
        whalo=whalo,
        ehalo=ehalo,
        shalo=shalo,
        nhalo=nhalo,
        xflags=mpp_domains_obj.CYCLIC_GLOBAL_DOMAIN,
        yflags=mpp_domains_obj.CYCLIC_GLOBAL_DOMAIN,
    )

    answers = np.array(
        [
            [
                [66, 76, 6, 16, 26, 36, 46, 56],
                [67, 77, 7, 17, 27, 37, 47, 57],
                [60, 70, 0, 10, 20, 30, 40, 50],
                [61, 71, 1, 11, 21, 31, 41, 51],
                [62, 72, 2, 12, 22, 32, 42, 52],
                [63, 73, 3, 13, 23, 33, 43, 53],
                [64, 74, 4, 14, 24, 34, 44, 54],
                [65, 75, 5, 15, 25, 35, 45, 55],
            ],
            [
                [62, 72, 2, 12, 22, 32, 42, 52],
                [63, 73, 3, 13, 23, 33, 43, 53],
                [64, 74, 4, 14, 24, 34, 44, 54],
                [65, 75, 5, 15, 25, 35, 45, 55],
                [66, 76, 6, 16, 26, 36, 46, 56],
                [67, 77, 7, 17, 27, 37, 47, 57],
                [60, 70, 0, 10, 20, 30, 40, 50],
                [61, 71, 1, 11, 21, 31, 41, 51],
            ],
            [
                [26, 36, 46, 56, 66, 76, 6, 16],
                [27, 37, 47, 57, 67, 77, 7, 17],
                [20, 30, 40, 50, 60, 70, 0, 10],
                [21, 31, 41, 51, 61, 71, 1, 11],
                [22, 32, 42, 52, 62, 72, 2, 12],
                [23, 33, 43, 53, 63, 73, 3, 13],
                [24, 34, 44, 54, 64, 74, 4, 14],
                [25, 35, 45, 55, 65, 75, 5, 15],
            ],
            [
                [22, 32, 42, 52, 62, 72, 2, 12],
                [23, 33, 43, 53, 63, 73, 3, 13],
                [24, 34, 44, 54, 64, 74, 4, 14],
                [25, 35, 45, 55, 65, 75, 5, 15],
                [26, 36, 46, 56, 66, 76, 6, 16],
                [27, 37, 47, 57, 67, 77, 7, 17],
                [20, 30, 40, 50, 60, 70, 0, 10],
                [21, 31, 41, 51, 61, 71, 1, 11],
            ],
        ],
        dtype=np.float32,
    )

    compute = mpp_domains_obj.get_compute_domain(
        domain_id=domain.domain_id, whalo=whalo, shalo=shalo
    )
    data = mpp_domains_obj.get_data_domain(
        domain_id=domain.domain_id, whalo=whalo, shalo=shalo
    )

    isc = compute["xbegin"]
    jsc = compute["ybegin"]
    xsize_c = compute["xsize"]
    ysize_c = compute["ysize"]
    xsize_d = data["xsize"]
    ysize_d = data["ysize"]

    global_data = np.zeros(
        shape=(nx + ehalo + whalo, ny + ehalo + whalo), dtype=np.float32
    )
    for ix in range(nx):
        for iy in range(ny):
            global_data[whalo + ix][shalo + iy] = iy * 10 + ix

    idata = np.zeros(shape=(xsize_d, ysize_d), dtype=np.float32)
    for i in range(xsize_c):
        for j in range(ysize_c):
            idata[whalo + i][shalo + j] = global_data[isc + i][jsc + j]

    mpp_domains_obj.update_domains(
        field=idata,
        domain_id=domain_id,
        whalo=whalo,
        ehalo=ehalo,
        shalo=shalo,
        nhalo=nhalo,
    )

    assert np.array_equal(idata, answers[mpp_obj.pe()])

    pyfms_obj.pyfms_end()


@pytest.mark.remove
def test_remove_input_nml():
    os.remove("input.nml")
    assert not os.path.isfile("input.nml")


if __name__ == "__main__":
    test_update_domains()
