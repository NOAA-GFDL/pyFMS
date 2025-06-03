import os

import pytest

import pyfms

@pytest.mark.create
def test_create_input_nml():
    inputnml = open("input.nml", "w")
    inputnml.close()
    os.path.isfile("input.nml")

@pytest.mark.parallel
def test_define_cubic_mosaic():
    jsc_check = [3, 13, 23, 31, 41, 3, 13, 23, 31, 41, 3, 13, 23, 31, 41, 
        3, 13, 23, 31, 41, 3, 13, 23, 31, 41, 3, 13, 23, 31, 41]
    jec_check = [12, 22, 30, 40, 50, 12, 22, 30, 40, 50, 12, 22, 30, 40, 50, 
        12, 22, 30, 40, 50, 12, 22, 30, 40, 50, 12, 22, 30, 40, 50]
    jsd_check = [0, 10, 20, 28, 38, 0, 10, 20, 28, 38, 0, 10, 20, 28, 38, 
        0, 10, 20, 28, 38, 0, 10, 20, 28, 38, 0, 10, 20, 28, 38]
    jed_check = [15, 25, 33, 43, 53, 15, 25, 33, 43, 53, 15, 25, 33, 43, 53, 
        15, 25, 33, 43, 53, 15, 25, 33, 43, 53, 15, 25, 33, 43, 53]
    ysize_c_check = [10, 10, 8, 10, 10, 10, 10, 8, 10, 10, 10, 10, 8, 10, 10, 
        10, 10, 8, 10, 10, 10, 10, 8, 10, 10, 10, 10, 8, 10, 10]
    ysize_d_check = [16, 16, 14, 16, 16, 16, 16, 14, 16, 16, 16, 16, 14, 16, 16, 
        16, 16, 14, 16, 16, 16, 16, 14, 16, 16, 16, 16, 14, 16, 16]
    nx = 48
    ny = 48
    whalo = 3
    shalo = 3
    ntiles = 6

    global_indices = [0, nx-1, 0, ny-1]
    layout = [1,5]

    ni = [nx, nx, nx, nx, nx, nx]
    nj = [ny, ny, ny, ny, ny, ny]

    halo = 3
    use_memsize = False

    pyfms.fms.init()

    domain_id = pyfms.mpp_domains.define_cubic_mosaic(
        ni=ni,
        nj=nj,
        global_indices=global_indices,
        layout=layout,
        ntiles=ntiles,
        halo=halo,
        use_memsize=use_memsize,
    )

    pe = pyfms.mpp.pe()

    compute_domain = pyfms.mpp_domains.get_compute_domain(domain_id=domain_id, whalo=whalo, shalo=shalo)
    data_domain = pyfms.mpp_domains.get_data_domain(domain_id=domain_id, whalo=whalo, shalo=shalo)

    assert compute_domain["isc"] == 3
    assert compute_domain["iec"] == 50
    assert compute_domain["jsc"] == jsc_check[pe]
    assert compute_domain["jec"] == jec_check[pe]
    assert data_domain["isd"] == 0
    assert data_domain["ied"] == 53
    assert data_domain["jsd"] == jsd_check[pe]
    assert data_domain["jed"] == jed_check[pe]
    assert compute_domain["xsize_c"] == 48
    assert compute_domain["ysize_c"] == ysize_c_check[pe]
    assert data_domain["xsize_d"] == 54
    assert data_domain["ysize_d"] == ysize_d_check[pe]
    assert compute_domain["xmax_size_c"] == 48
    assert compute_domain["ymax_size_c"] == 10
    assert data_domain["xmax_size_d"] == 54
    assert data_domain["ymax_size_d"] == 16

    pyfms.fms.end()

@pytest.mark.remove
def test_remove_input_nml():
    os.remove("input.nml")
    assert not os.path.isfile("input.nml")


if __name__ == "__main__":
    test_define_cubic_mosaic()


