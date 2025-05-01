import os

import numpy as np
import pytest

import pyfms


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

    pyfms.fms.init()

    global_indices = [0, (nx - 1), 0, (ny - 1)]
    layout = pyfms.mpp_domains.define_layout(global_indices=global_indices, ndivs=npes)

    domain = pyfms.mpp_domains.define_domains(
        global_indices=[0, (nx - 1), 0, (ny - 1)],
        layout=layout,
        whalo=whalo,
        ehalo=ehalo,
        shalo=shalo,
        nhalo=nhalo,
        xflags=pyfms.mpp_domains.CYCLIC_GLOBAL_DOMAIN,
        yflags=pyfms.mpp_domains.CYCLIC_GLOBAL_DOMAIN,
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

    global_data = np.zeros(
        shape=(nx + ehalo + whalo, ny + ehalo + whalo), dtype=np.float32
    )
    for ix in range(nx):
        for iy in range(ny):
            global_data[whalo + ix][shalo + iy] = iy * 10 + ix

    isc, jsc = domain.isc, domain.jsc
    idata = np.zeros(shape=(domain.xsize_d, domain.ysize_d), dtype=np.float32)
    for i in range(domain.xsize_c):
        for j in range(domain.ysize_c):
            idata[whalo + i][shalo + j] = global_data[isc + i][jsc + j]

    pyfms.mpp_domains.update_domains(
        field=idata,
        domain_id=domain.domain_id,
        whalo=whalo,
        ehalo=ehalo,
        shalo=shalo,
        nhalo=nhalo,
    )

    assert np.array_equal(idata, answers[pyfms.mpp.pe()])

    pyfms.fms.end()


@pytest.mark.remove
def test_remove_input_nml():
    os.remove("input.nml")
    assert not os.path.isfile("input.nml")


if __name__ == "__main__":
    test_update_domains()
