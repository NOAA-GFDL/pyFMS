import numpy as np

import pyfms


def test_create_xgrid():

    cfms = pyfms.pyFMS().clibFMS
    create_xgrid = pyfms.HorizInterp(cfms=cfms).create_xgrid_2dx2d_order1

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
    area = pyfms.GridUtils.get_grid_area(
        cfms=cfms, nlon=nlon_src, nlat=nlat_src, lon=lon_src, lat=lat_src
    )

    assert xgrid["nxgrid"] == nlon_src * nlat_src
    assert np.array_equal(xgrid["i_src"], xgrid["i_tgt"])
    assert np.array_equal(xgrid["j_src"], xgrid["j_tgt"])
    assert np.array_equal(xgrid["xarea"], area)
