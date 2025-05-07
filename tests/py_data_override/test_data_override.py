import os
import shutil

import numpy as np
import pytest

import pyfms


@pytest.mark.parallel
def test_data_override():

    nx = 360
    ny = 180
    nz = 5
    ehalo = 2
    whalo = 2
    shalo = 2
    nhalo = 2

    pyfms.fms.init()
    domain = pyfms.mpp_domains.define_domains(
        global_indices=[0, nx - 1, 0, ny - 1],
        layout=[2, 3],
        ehalo=ehalo,
        whalo=whalo,
        shalo=shalo,
        nhalo=nhalo,
    )

    xsize = domain.xsize_c
    ysize = domain.ysize_c

    pyfms.data_override.init(ocn_domain_id=domain.domain_id)
    pyfms.data_override.set_time(
        year=1, month=1, day=3, hour=0, minute=0, second=0, tick=0
    )

    data, override = pyfms.data_override.override_scalar(
        gridname="OCN", fieldname="runoff_scalar", dtype=np.float64
    )

    assert override
    assert data == np.float64(2.0)
    
    data = np.zeros((xsize, ysize), dtype=np.float64)
    override = pyfms.data_override.override(
        gridname="OCN", fieldname="runoff_2d", data=data
    )

    assert override
    assert np.all(data == np.float64(200.0))
    
    data = np.zeros((xsize, ysize, nz), dtype=np.float64)
    override = pyfms.data_override.override(
        gridname="OCN", fieldname="runoff_3d", data=data
    )

    answers = np.array(
        [200 + z + 1 for z in range(nz)] * xsize * ysize, dtype=np.float64
    ).reshape(xsize, ysize, nz)

    assert override
    assert np.all(data == answers)

    pyfms.fms.end()


@pytest.mark.remove
def test_remove_files():
    shutil.rmtree("INPUT")
    os.remove("input.nml")
    os.remove("data_table.yaml")
    assert not os.path.exists("INPUT")
    assert not os.path.isfile("input.nml")
    assert not os.path.isfile("data_table.yaml")
