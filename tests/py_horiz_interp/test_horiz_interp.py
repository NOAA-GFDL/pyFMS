import os

import numpy as np

import pyfms
from pyfms.utils.constants import DEG_TO_RAD


def test_create_input_nml():
    inputnml = open("input.nml", "w")
    inputnml.close()
    assert os.path.isfile("input.nml")


def test_create_xgrid():

    pyfms.fms.init()
    create_xgrid = pyfms.horiz_interp.create_xgrid_2dx2d_order1

    refine = 1
    lon_init = 0.0
    lat_init = -np.pi / 4.0
    nlon_src = 10
    nlat_src = 10
    nlon_tgt = nlon_src * refine
    nlat_tgt = nlat_src * refine
    dlon_src = np.pi / nlon_src
    dlat_src = (np.pi / 2.0) * nlat_src
    dlon_tgt = dlon_src / refine
    dlat_tgt = dlat_src / refine

    lon_src = np.array(
        [lon_init + (dlon_src * i) for i in range(nlon_src + 1)] * (nlat_src + 1),
        dtype=np.float64,
    )
    lat_src = np.array(
        [
            lat_init + (dlat_src * i)
            for i in range(nlat_src + 1)
            for j in range(nlon_src + 1)
        ],
        dtype=np.float64,
    )
    lon_tgt = np.array(
        [lon_init + (dlon_tgt * i) for i in range(nlon_tgt + 1)] * (nlat_tgt + 1),
        dtype=np.float64,
    )
    lat_tgt = np.array(
        [
            lat_init + (dlat_tgt * i)
            for i in range(nlat_tgt + 1)
            for j in range(nlon_tgt + 1)
        ],
        dtype=np.float64,
    )
    mask_src = np.ones((nlon_src + 1) * (nlat_src + 1), dtype=np.float64)

    xgrid = create_xgrid(
        nlon_src=nlon_src,
        nlat_src=nlat_src,
        nlon_tgt=nlon_tgt,
        nlat_tgt=nlat_tgt,
        lon_src=lon_src,
        lat_src=lat_src,
        lon_tgt=lon_tgt,
        lat_tgt=lat_tgt,
        mask_src=mask_src,
    )

    # answer checking
    area = pyfms.grid_utils.get_grid_area(
        nlon=nlon_src, nlat=nlat_src, lon=lon_src, lat=lat_src
    )

    assert xgrid["nxgrid"] == nlon_src * nlat_src
    assert np.array_equal(xgrid["i_src"], xgrid["i_tgt"])
    assert np.array_equal(xgrid["j_src"], xgrid["j_tgt"])
    assert np.array_equal(xgrid["xarea"], area)

def test_horiz_interp_conservative():
    pyfms.fms.init()
    horiz_interp_double_2d = pyfms.horiz_interp.horiz_interp_2d_double
    horiz_interp_float_2d = pyfms.horiz_interp.horiz_interp_2d_float

    # set up our domain decomposition
    ni_src = 360
    nj_src = 180
    ni_dst = 144
    nj_dst = 72
    halo = 2
    pes=pyfms.mpp.npes()

    domain = pyfms.mpp_domains.define_domains(
        global_indices= [0, ni_src - 1, 0, nj_src - 1],
        layout= pyfms.mpp_domains.define_layout(
            global_indices=[0, ni_src - 1, 0, nj_src - 1],
            ndivs=pes,
            ),
        pelist=pyfms.mpp.get_current_pelist(npes=pes),
        name="horiz_interp_conservative_test",
        whalo=halo,
        ehalo=halo,
        shalo=halo,
        nhalo=halo,
        xflags=pyfms.mpp_domains.CYCLIC_GLOBAL_DOMAIN,
        yflags=pyfms.mpp_domains.CYCLIC_GLOBAL_DOMAIN,
    )

    # set up src/dst grids 
    lon_bnds = (0.0, 360.0) # same start/end value for src and dst
    lat_bnds = (-90.0, 90.0)
    dlon_src = (lon_bnds[1] - lon_bnds[0]) / ni_src
    dlat_src = (lat_bnds[1] - lat_bnds[0]) / nj_src
    dlon_dst = (lon_bnds[1] - lon_bnds[0]) / ni_dst
    dlat_dst = (lat_bnds[1] - lat_bnds[0]) / nj_dst

    compute_indices = pyfms.mpp_domains.get_compute_domain(domain.domain_id)

    isc = compute_indices["isc"]
    iec = compute_indices["iec"]
    jsc = compute_indices["jsc"]
    jec = compute_indices["jec"]

    lon_in_size = ni_src + 1 
    lat_in_size = nj_src + 1
    lon_out_size = iec+1-isc 
    lat_out_size = jec+1-jsc 

    lon_src = np.array(
        [
            lon_bnds[0] + (dlon_src * i)
            for i in range(lon_in_size)
            for j in range(lat_in_size)
        ],
        dtype=np.float64,
    )
    lat_src = np.array(
        [
            lat_bnds[0] + (dlat_src * i)
            for i in range(lon_in_size)
            for j in range(lat_in_size)
        ],
        dtype=np.float64,
    )
    lon_dst = np.array(
        [
            lon_bnds[0] + (dlon_dst * i)
            for i in range(lon_out_size)
            for i in range(lat_out_size)
        ],
        dtype=np.float64,
    )
    lat_dst = np.array(
        [
            lat_bnds[0] + (dlat_dst * i)
            for i in range(lon_out_size)
            for j in range(lat_out_size)
        ],
        dtype=np.float64,
    )
    lat_src = lat_src * DEG_TO_RAD
    lon_src = lon_src * DEG_TO_RAD
    lat_dst = lat_dst * DEG_TO_RAD
    lon_dst = lon_dst * DEG_TO_RAD

    # init and set a horiz_interp type (required for all horiz_interp calls!)
    pyfms.horiz_interp.init(2)
    pyfms.horiz_interp.set_current_interp(0)

    # actually perform the interpolation via C binding
    interp_id = horiz_interp_double_2d(
        lon_in_ptr=lon_src,
        lon_in_shape= [lon_in_size, lat_in_size],
        lat_in_ptr=lat_src,
        lat_in_shape=[lon_in_size, lat_in_size],
        lon_out_ptr=lon_dst,
        lon_out_shape=[lon_out_size, lat_out_size],
        lat_out_ptr=lat_dst,
        lat_out_shape=[lon_out_size, lat_out_size],
        interp_method="conservative",
        verbose=1,
        max_dist=None,
        src_modulo=None,
        mask_in_ptr=None,
        mask_out_ptr=None,
        is_latlon_in=None,
        is_latlon_out=None
    )

    pyfms.horiz_interp.set_current_interp(1)

    # one more time with floats
    interp_id = horiz_interp_float_2d(
        lon_in_ptr=lon_src.astype(np.float32),
        lon_in_shape= [lon_in_size, lat_in_size],
        lat_in_ptr=lat_src.astype(np.float32),
        lat_in_shape=[lon_in_size, lat_in_size],
        lon_out_ptr=lon_dst.astype(np.float32),
        lon_out_shape=[lon_out_size, lat_out_size],
        lat_out_ptr=lat_dst.astype(np.float32),
        lat_out_shape=[lon_out_size, lat_out_size],
        interp_method="conservative",
        verbose=1,
        max_dist=None,
        src_modulo=None,
        mask_in_ptr=None,
        mask_out_ptr=None,
        is_latlon_in=None,
        is_latlon_out=None
    )

    pyfms.fms.end()

def test_remove_input_nml():
    os.remove("input.nml")
    assert not os.path.isfile("input.nml")


if __name__ == "__main__":
    test_create_xgrid()
    test_horiz_interp_conservative()
