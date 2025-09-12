import os

import numpy as np
import pytest

import pyfms
from pyfms.utils.constants import DEG_TO_RAD


@pytest.mark.create
def test_create_input_nml():
    inputnml = open("input.nml", "w")
    inputnml.close()
    assert os.path.isfile("input.nml")
    pyfms.fms.init(ndomain=2)


def test_create_xgrid():

    create_xgrid = pyfms.horiz_interp.create_xgrid_2dx2d_order1

    refine = 1
    lon_init, lat_init = 0.0, -np.pi / 4.0
    lon_end, lat_end = np.pi, np.pi / 4.0
    nlon_src = 10
    nlat_src = 10
    nlon_tgt = nlon_src * refine
    nlat_tgt = nlat_src * refine

    lon_src_1d = np.linspace(lon_init, lon_end, nlon_src + 1)
    lat_src_1d = np.linspace(lat_init, lat_end, nlat_src + 1)
    lon_src, lat_src = np.meshgrid(lon_src_1d, lat_src_1d)

    lon_tgt_1d = np.linspace(lon_init, lon_end, nlon_tgt + 1)
    lat_tgt_1d = np.linspace(lat_init, lat_end, nlat_tgt + 1)
    lon_tgt, lat_tgt = np.meshgrid(lon_tgt_1d, lat_tgt_1d)

    lon_src = lon_src.flatten()
    lat_src = lat_src.flatten()
    lon_tgt = lon_tgt.flatten()
    lat_tgt = lat_tgt.flatten()

    mask_src = np.ones(nlon_src * nlat_src, dtype=np.float64)

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

    # set up domain decomposition
    ni_src = 360
    nj_src = 180
    ni_dst = 144
    nj_dst = 72
    halo = 2
    pes = pyfms.mpp.npes()

    global_indices = [0, ni_src - 1, 0, nj_src - 1]
    layout = pyfms.mpp_domains.define_layout(global_indices, ndivs=pes)
    domain = pyfms.mpp_domains.define_domains(
        global_indices=global_indices,
        layout=layout,
        pelist=pyfms.mpp.get_current_pelist(npes=pes),
        name="horiz_interp_conservative_test",
        whalo=halo,
        ehalo=halo,
        shalo=halo,
        nhalo=halo,
        xflags=pyfms.mpp_domains.CYCLIC_GLOBAL_DOMAIN,
        yflags=pyfms.mpp_domains.CYCLIC_GLOBAL_DOMAIN,
    )

    isc = domain.isc
    iec = domain.iec
    jsc = domain.jsc
    jec = domain.jec

    lon_in_size = ni_src + 1
    lat_in_size = nj_src + 1

    lon_in_1d = np.linspace(0, 360, num=lon_in_size, dtype=np.float64) * DEG_TO_RAD
    lat_in_1d = np.linspace(-90, 90, num=lat_in_size, dtype=np.float64) * DEG_TO_RAD

    lat_src, lon_src = np.meshgrid(lat_in_1d, lon_in_1d)

    lon_dst = np.ascontiguousarray(lon_src[isc:iec, jsc:jec])
    lat_dst = np.ascontiguousarray(lat_src[isc:iec, jsc:jec])

    # init and set a horiz_interp type (required for all horiz_interp calls!)
    pyfms.horiz_interp.init(2)

    # get interpolation weights
    interp_id = pyfms.horiz_interp.get_weights(
        lon_in=lon_src,
        lat_in=lat_src,
        lon_out=lon_dst,
        lat_out=lat_dst,
        interp_method="conservative",
        verbose=1,
    )

    # check weights
    nxgrid = (jec - jsc - 1) * (iec - isc - 1)
    interp = pyfms.Interp(interp_id)

    assert interp_id == 0
    assert interp.nxgrid == nxgrid
    assert interp.interp_method == "conservative"
    assert np.all(interp.i_src == np.array(list(range(isc, iec - 1)) * (jec - jsc - 1)))

    j_answer = np.array(
        [j for j in range(jsc, jec - 1) for ilon in range(iec - isc - 1)]
    )
    assert np.all(interp.j_src == j_answer)

    assert interp.nlon_src == ni_src
    assert interp.nlat_src == nj_src
    assert interp.nlon_dst == lon_dst.shape[0] - 1
    assert interp.nlat_dst == lat_dst.shape[1] - 1


@pytest.mark.skip(reason="test needs to be updated")
def test_horiz_interp_bilinear():
    pyfms.fms.init()
    horiz_interp_double_2d = pyfms.horiz_interp.horiz_interp_2d_double
    horiz_interp_float_2d = pyfms.horiz_interp.horiz_interp_2d_float

    ni_src = 360
    nj_src = 180
    ni_dst = 360
    nj_dst = 180
    halo = 2
    pes = pyfms.mpp.npes()

    # set up domain decomposition
    domain = pyfms.mpp_domains.define_domains(
        global_indices=[0, ni_src - 1, 0, nj_src - 1],
        layout=pyfms.mpp_domains.define_layout(
            global_indices=[0, ni_src - 1, 0, nj_src - 1],
            ndivs=pes,
        ),
        pelist=pyfms.mpp.get_current_pelist(npes=pes),
        name="horiz_interp_bilinear_test",
        whalo=halo,
        ehalo=halo,
        shalo=halo,
        nhalo=halo,
        xflags=pyfms.mpp_domains.CYCLIC_GLOBAL_DOMAIN,
        yflags=pyfms.mpp_domains.CYCLIC_GLOBAL_DOMAIN,
    )

    # set up src/dst grids
    lon_bnds = (0.0, 360.0)  # same start/end value for src and dst
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
    lon_dst_size = iec + 1 - isc
    lat_dst_size = jec + 1 - jsc

    # TODO theres probably a better way to do this
    lon_in_1d = []
    lat_in_1d = []
    lon_dst_1d = []
    lat_dst_1d = []
    for i in range(lon_in_size + 1):
        lon_in_1d.append((lon_bnds[0] + float(dlon_src * i)))
    for i in range(lat_in_size + 1):
        lat_in_1d.append((lat_bnds[0] + float(dlat_src * i)))
    for i in range(lon_dst_size + 1):
        lon_dst_1d.append((lon_bnds[0] + float(dlon_dst * i)))
    for i in range(lat_dst_size + 1):
        lat_dst_1d.append((lat_bnds[0] + float(dlat_dst * i)))
    lon_src = []
    lat_src = []
    for i in range(lon_in_size):
        for j in range(lat_in_size):
            lon_src.append(lon_in_1d[i])
    for i in range(lon_in_size):
        for j in range(lat_in_size):
            lat_src.append(lat_in_1d[j])
    # take midpoints for dst grid
    lon_dst = [None] * (lon_dst_size * lat_dst_size)
    lat_dst = [None] * (lon_dst_size * lat_dst_size)
    for i in range(lon_dst_size):
        midpoint_lon = (lon_dst_1d[i] + lon_dst_1d[i + 1]) * 0.5
        for j in range(lat_dst_size):
            lon_dst[i * lat_dst_size + j] = midpoint_lon
    for i in range(lat_dst_size):
        midpoint_lat = (lat_dst_1d[i] + lat_dst_1d[i + 1]) * 0.5
        for j in range(lon_dst_size):
            lat_dst[i * lon_dst_size + j] = midpoint_lat

    lon_src = np.array(lon_src, dtype=np.float64)
    lat_src = np.array(lat_src, dtype=np.float64)
    lon_dst = np.array(lon_dst, dtype=np.float64)
    lat_dst = np.array(lat_dst, dtype=np.float64)

    # init and set a horiz_interp type (required for all horiz_interp calls!)
    pyfms.horiz_interp.init(2)
    pyfms.horiz_interp.set_current_interp(0)

    lon_src = lon_src * float(DEG_TO_RAD)
    lat_src = lat_src * float(DEG_TO_RAD)
    lon_dst = lon_dst * float(DEG_TO_RAD)
    lat_dst = lat_dst * float(DEG_TO_RAD)

    # actually perform the interpolation via C binding
    interp_id = horiz_interp_double_2d(
        lon_in_ptr=lon_src,
        lon_in_shape=[lon_in_size, lat_in_size],
        lat_in_ptr=lat_src,
        lat_in_shape=[lon_in_size, lat_in_size],
        lon_dst_ptr=lon_dst,
        lon_dst_shape=[lon_dst_size, lat_dst_size],
        lat_dst_ptr=lat_dst,
        lat_dst_shape=[lon_dst_size, lat_dst_size],
        interp_method="bilinear",
        verbose=1,
        max_dist=None,
        src_modulo=None,
        mask_in_ptr=None,
        mask_out_ptr=None,
        is_latlon_in=None,
        is_latlon_dst=None,
    )

    interp_type_vals_double = pyfms.horiz_interp.horiz_interp_get_interp_double()

    assert interp_type_vals_double["interp_id"] == interp_id
    assert interp_type_vals_double["is_allocated"] is True
    assert interp_type_vals_double["interp_method"] == 2  # _BILINEAR
    assert interp_type_vals_double["nlon_src"] == lon_in_size
    assert interp_type_vals_double["nlat_src"] == lat_in_size
    assert interp_type_vals_double["nlon_dst"] == lon_dst_size
    assert interp_type_vals_double["nlat_dst"] == lat_dst_size
    # weights are all 0.5 from taking midpoints
    assert np.allclose(interp_type_vals_double["wti"], 0.5)
    assert np.allclose(interp_type_vals_double["wtj"], 0.5)

    # one more time with floats
    pyfms.horiz_interp.set_current_interp(1)

    lon_src = lon_src.astype(np.float32)
    lat_src = lat_src.astype(np.float32)
    lon_dst = lon_dst.astype(np.float32)
    lat_dst = lat_dst.astype(np.float32)

    # actually perform the interpolation via C binding
    interp_id = horiz_interp_float_2d(
        lon_in_ptr=lon_src,
        lon_in_shape=[lon_in_size, lat_in_size],
        lat_in_ptr=lat_src,
        lat_in_shape=[lon_in_size, lat_in_size],
        lon_dst_ptr=lon_dst,
        lon_dst_shape=[lon_dst_size, lat_dst_size],
        lat_dst_ptr=lat_dst,
        lat_dst_shape=[lon_dst_size, lat_dst_size],
        interp_method="bilinear",
        verbose=1,
        max_dist=None,
        src_modulo=None,
        mask_in_ptr=None,
        mask_out_ptr=None,
        is_latlon_in=None,
        is_latlon_dst=None,
    )

    interp_type_vals_float = pyfms.horiz_interp.horiz_interp_get_interp_float()

    assert interp_type_vals_float["interp_id"] == interp_id
    assert interp_type_vals_float["is_allocated"] is True
    assert interp_type_vals_float["interp_method"] == 2  # _BILINEAR
    assert interp_type_vals_float["nlon_src"] == lon_in_size
    assert interp_type_vals_float["nlat_src"] == lat_in_size
    assert interp_type_vals_float["nlon_dst"] == lon_dst_size
    assert interp_type_vals_float["nlat_dst"] == lat_dst_size
    assert np.allclose(interp_type_vals_float["wti"], 0.5, atol=1e-4)
    assert np.allclose(interp_type_vals_float["wtj"], 0.5, atol=1e-4)

    pyfms.fms.end()


@pytest.mark.remove
def test_remove_input_nml():
    if pyfms.mpp.pe() == 0:
        os.remove("input.nml")
    pyfms.fms.end()
