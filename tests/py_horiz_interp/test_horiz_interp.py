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

# same as the test in cFMS, but using the Python interface 
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

    # TODO theres probably a better way to do this
    lon_in_1d = []
    lat_in_1d = []
    lon_out_1d = []
    lat_out_1d = []
    for i in range(lon_in_size):
        lon_in_1d.append((lon_bnds[0] + float(dlon_src * i)) * float(DEG_TO_RAD))
    for i in range(lat_in_size):
        lat_in_1d.append((lat_bnds[0] + float(dlat_src * i)) * float(DEG_TO_RAD))
    for i in range(lon_out_size):  
        lon_out_1d.append((lon_bnds[0] + float(dlon_dst * i)) * float(DEG_TO_RAD))
    for i in range(lat_out_size):
        lat_out_1d.append((lat_bnds[0] + float(dlat_dst * i)) * float(DEG_TO_RAD))
    lon_src = []
    lat_src = []
    lon_dst = []
    lat_dst = []
    for i in range(lon_in_size):
        for j in range(lat_in_size):
            lon_src.append(lon_in_1d[i])
            lat_src.append(lat_in_1d[j])
    for i in range(lon_out_size):
        for j in range(lat_out_size):
            lon_dst.append(lon_out_1d[i])
            lat_dst.append(lat_out_1d[j])
    lon_src = np.array(lon_src, dtype=np.float64)
    lat_src = np.array(lat_src, dtype=np.float64)
    lon_dst = np.array(lon_dst, dtype=np.float64)
    lat_dst = np.array(lat_dst, dtype=np.float64)

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

    # get the interpolation results from the type in the form of a dictionary
    interp_type_vals_double = pyfms.horiz_interp.horiz_interp_get_interp_double(interp_id)
    print(interp_type_vals_double)
    
    # check our interpolation results
    if( pyfms.mpp.npes() == 1 ):
        nxgrid = 232632 
    elif( pyfms.mpp.npes() == 4 ):
        nxgrid = 115992
    assert interp_type_vals_double["interp_id"] == interp_id
    assert interp_type_vals_double["nxgrid"] == (nxgrid)
    assert interp_type_vals_double["i_src"].shape == (nxgrid,)
    assert interp_type_vals_double["j_src"].shape == (nxgrid,)
    assert interp_type_vals_double["i_dst"].shape == (nxgrid,)
    assert interp_type_vals_double["j_dst"].shape == (nxgrid,)
    assert interp_type_vals_double["is_allocated"] is True
    assert interp_type_vals_double["interp_method"] == 1 # conservative 
    assert interp_type_vals_double["version"] == 2
    assert interp_type_vals_double["nlon_src"] == ni_src
    assert interp_type_vals_double["nlat_src"] == nj_src
    assert interp_type_vals_double["nlon_dst"] == iec-isc
    assert interp_type_vals_double["nlat_dst"] == jec-jsc

    # one more time with floats
    pyfms.horiz_interp.set_current_interp(1)

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

    interp_type_vals_float = pyfms.horiz_interp.horiz_interp_get_interp_float(interp_id)
    print(interp_type_vals_float)
    
    if( pyfms.mpp.npes() == 1 ):
        nxgrid = 254880 
    elif( pyfms.mpp.npes() == 4 ):
        nxgrid = 119448
    assert interp_type_vals_float["interp_id"] == interp_id
    assert interp_type_vals_float["nxgrid"] == (nxgrid)
    assert interp_type_vals_float["i_src"].shape == (nxgrid,)
    assert interp_type_vals_float["j_src"].shape == (nxgrid,)
    assert interp_type_vals_float["i_dst"].shape == (nxgrid,)
    assert interp_type_vals_float["j_dst"].shape == (nxgrid,)
    assert interp_type_vals_float["is_allocated"] is True
    assert interp_type_vals_float["interp_method"] == 1 # conservative 
    assert interp_type_vals_float["version"] == 2
    assert interp_type_vals_float["nlon_src"] == ni_src
    assert interp_type_vals_float["nlat_src"] == nj_src
    assert interp_type_vals_float["nlon_dst"] == iec-isc
    assert interp_type_vals_float["nlat_dst"] == jec-jsc

    pyfms.fms.end()

def test_remove_input_nml():
    os.remove("input.nml")
    assert not os.path.isfile("input.nml")


if __name__ == "__main__":
    test_create_xgrid()
    test_horiz_interp_conservative()
