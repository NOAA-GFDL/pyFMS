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
def test_vector_update_domains():

    nx = 8
    ny = 8
    npes = 2
    whalo = 2
    ehalo = 2
    shalo = 2
    nhalo = 2
    domain_id = 0

    pyfms.fms.init()

    global_indices = [0, (nx - 1), 0, (ny - 1)]
    layout = pyfms.mpp_domains.define_layout(global_indices=global_indices, ndivs=npes)

    domain = pyfms.mpp_domains.define_domains(
        global_indices=global_indices,
        layout=layout,
        whalo=whalo,
        ehalo=ehalo,
        shalo=shalo,
        nhalo=nhalo,
        xflags=pyfms.mpp_domains.CYCLIC_GLOBAL_DOMAIN,
        yflags=pyfms.mpp_domains.FOLD_NORTH_EDGE,
    )

    xdatasize = whalo + nx + ehalo
    ydatasize = shalo + ny + nhalo
    isc = domain.isc
    jsc = domain.jsc
    xsize_c = domain.xsize_c
    ysize_c = domain.ysize_c
    xsize_d = domain.xsize_d
    ysize_d = domain.ysize_d

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

    """
    Cyclic wrapping of global data
    """
    global_data1[:whalo, shalo : ny + shalo] = global_data1[
        nx : nx + whalo, shalo : ny + shalo
    ]
    global_data1[whalo + nx : whalo + nx + ehalo, shalo : ny + shalo] = global_data1[
        whalo : whalo + 2, shalo : ny + shalo
    ]
    global_data2[:whalo, shalo : ny + shalo] = global_data2[
        nx : nx + whalo, shalo : ny + shalo
    ]
    global_data2[whalo + nx : whalo + nx + ehalo, shalo : ny + shalo] = global_data2[
        whalo : whalo + 2, shalo : ny + shalo
    ]

    """
    Folded xy north edge
    """
    global_data1[: whalo + nx + 1, shalo + ny : shalo + ny + nhalo] = -global_data1[
        whalo + nx :: -1, ny + 1 : ny - 1 : -1
    ]
    global_data1[whalo + nx + 1, shalo + ny : shalo + ny + nhalo] = -global_data1[
        nx - 1, ny + 1 : ny - 1 : -1
    ]
    global_data2[: whalo + nx + ehalo, shalo + ny : shalo + ny + nhalo] = -global_data2[
        whalo + nx + 1 :: -1, ny : ny - 2 : -1
    ]

    """
    Populating compute domains of fields
    """
    x_data[whalo : whalo + xsize_c, shalo : shalo + ysize_c] = global_data1[
        isc : isc + xsize_c, jsc : jsc + ysize_c
    ]
    y_data[whalo : whalo + xsize_c, shalo : shalo + ysize_c] = global_data2[
        isc : isc + xsize_c, jsc : jsc + ysize_c
    ]

    gridtype = pyfms.mpp_domains.CGRID_NE

    pyfms.mpp_domains.vector_update_domains(
        fieldx=x_data,
        fieldy=y_data,
        domain_id=domain_id,
        gridtype=gridtype,
        whalo=whalo,
        ehalo=ehalo,
        shalo=shalo,
        nhalo=nhalo,
    )

    global_data2[nx - whalo : nx + whalo, ny + 1] = -global_data2[
        whalo + 3 : whalo - 1 : -1, ny + 1
    ]
    global_data2[:whalo, ny + 1] = -global_data2[nx : nx + whalo, ny + 1]
    global_data2[whalo + nx : whalo + nx + ehalo, ny + 1] = -global_data2[
        whalo : whalo + 2, ny + 1
    ]

    pe = pyfms.mpp.pe()
    ystart = pe * ysize_c
    yend = ystart + ysize_d
    assert np.array_equal(x_data, global_data1[0:xsize_d, ystart:yend])
    assert np.array_equal(y_data, global_data2[0:xsize_d, ystart:yend])

    pyfms.fms.end()


@pytest.mark.remove
def test_remove_input_nml():
    os.remove("input.nml")
    assert not os.path.isfile("input.nml")


if __name__ == "__main__":
    test_vector_update_domains()
