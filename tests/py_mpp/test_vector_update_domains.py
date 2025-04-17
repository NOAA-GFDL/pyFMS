import os

import numpy as np
import pytest

from pyfms import pyDomain, pyFMS, pyFMS_mpp, pyFMS_mpp_domains


@pytest.mark.create
def test_create_input_nml():
    inputnml = open("input.nml", "w")
    inputnml.close()
    assert os.path.isfile("input.nml")


@pytest.mark.parallel
def test_vector_update_domains():

    nx = 8
    ny = 8
    npes = 2
    whalo = 2
    ehalo = 2
    shalo = 2
    nhalo = 2
    domain_id = 0

    # TODO: Change after refactor
    pyfms = pyFMS(cFMS_path="./cFMS/libcFMS/.libs/libcFMS.so")
    mpp = pyFMS_mpp(cFMS=pyfms.cFMS)
    mpp_domains = pyFMS_mpp_domains(cFMS=pyfms.cFMS)

    global_indices = [0, (nx - 1), 0, (ny - 1)]
    # TODO: Use module level variable after refactor
    cyclic_global_domain = 2
    fold_north_edge = 2**5

    layout = mpp_domains.define_layout(global_indices=global_indices, ndivs=npes)

    domain = pyDomain(
        global_indices=global_indices,
        layout=layout,
        mpp_domains_obj=mpp_domains,
        domain_id=domain_id,
        whalo=whalo,
        ehalo=ehalo,
        shalo=shalo,
        nhalo=nhalo,
        xflags=cyclic_global_domain,
        yflags=fold_north_edge,
    )

    xdatasize = whalo + nx + ehalo
    ydatasize = shalo + ny + nhalo
    isc = domain.compute_domain.xbegin.value
    jsc = domain.compute_domain.ybegin.value
    xsize_c = domain.compute_domain.xsize.value
    ysize_c = domain.compute_domain.ysize.value
    xsize_d = domain.data_domain.xsize.value
    ysize_d = domain.data_domain.ysize.value

    global_data1 = np.zeros(shape=(xdatasize, ydatasize), dtype=np.float64)
    global_data2 = np.zeros(shape=(xdatasize, ydatasize), dtype=np.float64)

    x_data = np.zeros(shape=(xsize_d, ysize_d), dtype=np.float64)
    y_data = np.zeros(shape=(xsize_d, ysize_d), dtype=np.float64)

    for i in range(nx):
        for j in range(ny):
            global_data1[i + whalo][j + shalo] = (
                1 + (i + whalo) * 1e-3 + (j + shalo) * 1e-6
            )
            global_data2[i + whalo][j + shalo] = (
                1 + (i + whalo) * 1e-3 + (j + shalo) * 1e-6
            )

    for i in range(whalo):
        for j in range(shalo, ny + shalo):
            global_data1[i][j] = global_data1[i + nx][j]
            global_data1[i + nx + whalo][j] = global_data1[i + whalo][j]
            global_data2[i][j] = global_data2[i + nx][j]
            global_data2[i + nx + whalo][j] = global_data2[i + whalo][j]

    for i in range(nx + ehalo + 1):
        for j in range(nhalo):
            global_data1[i][j + ny + shalo] = -global_data1[nx + ehalo - i][ny + 1 - j]
            global_data1[nx + whalo + 1][j + ny + shalo] = -global_data1[nx - 1][
                ny + 1 - j
            ]

    for i in range(whalo + nx + ehalo):
        for j in range(nhalo):
            global_data2[i][j + ny + shalo] = -global_data2[whalo + nx + 1 - i][ny - j]

    for i in range(xsize_c):
        for j in range(ysize_c):
            x_data[i + whalo][j + shalo] = global_data1[i + isc][j + jsc]
            y_data[i + whalo][j + shalo] = global_data2[i + isc][j + jsc]

    # TODO: change to module variable after refactor
    gridtype = 2 + 2**5 + 2**3

    mpp_domains.vector_update_domains(
        fieldx=x_data,
        fieldy=y_data,
        domain_id=domain_id,
        gridtype=gridtype,
        whalo=whalo,
        ehalo=ehalo,
        shalo=shalo,
        nhalo=nhalo,
    )

    for i in range(ehalo + whalo):
        global_data2[nx - whalo + i][ny + 1] = -global_data2[nx - whalo - 1 - i][ny + 1]

    for i in range(whalo):
        global_data2[i][ny + 1] = -global_data2[nx + i][ny + 1]
        global_data2[nx + whalo + i][ny + 1] = -global_data2[whalo + i][ny + 1]

    global_start = [0, mpp.pe() * ysize_c]
    global_stop = [xsize_d, mpp.pe() * ysize_c + ysize_d]
    pe = mpp.pe()
    assert np.array_equal(
        x_data,
        global_data1[
            global_start[0] : global_stop[0], global_start[1] : global_stop[1]
        ],
    )
    assert np.array_equal(
        y_data,
        global_data2[
            global_start[0] : global_stop[0], global_start[1] : global_stop[1]
        ],
    )

    pyfms.pyfms_end()


@pytest.mark.remove
def test_remove_input_nml():
    os.remove("input.nml")
    assert not os.path.isfile("input.nml")


if __name__ == "__main__":
    test_vector_update_domains()
