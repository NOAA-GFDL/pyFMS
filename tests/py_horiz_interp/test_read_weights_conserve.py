import numpy as np
import xarray as xr

import pyfms

nx_src = 32
ny_src = 16
nx_dst = nx_src * 2
ny_dst = ny_src * 2

lon = np.deg2rad([[i for i in range(nx_dst+1)] for j in range(ny_dst+1)])
lat = np.deg2rad([[j for i in range(nx_dst+1)] for j in range(ny_dst+1)])

def write_remap():

    tile1 = np.array([1] * (nx_src * ny_src) + [2] * (nx_src * ny_src) +
                     [3] * (nx_src * ny_src) + [4] * (nx_src * ny_src), dtype=np.int32)

    tile1_cell = np.array([[i,j] for j in range(1,ny_src+1) for i in range(1,nx_src+1)] * 4, dtype=np.int32)

    tile2_cell = [[i,j] for j in range(1,ny_src+1) for i in range(1,nx_src+1)]
    tile2_cell += [[i+nx_src,j] for j in range(1,ny_src+1) for i in range(1,nx_src+1)]
    tile2_cell += [[i,j+ny_src] for j in range(1,ny_src+1) for i in range(1,nx_src+1)]
    tile2_cell += [[i+nx_src,j+ny_src] for j in range(1,ny_src+1) for i in range(1,nx_src+1)]
    tile2_cell = np.array(tile2_cell, dtype=np.int32)

    xgrid_area = pyfms.grid_utils.get_grid_area(lon, lat)

    xr.Dataset(data_vars={"tile1": (["ncells"], tile1),
                          "tile1_cell": (["ncells", "two"], tile1_cell),
                          "tile2_cell": (["ncells", "two"], tile2_cell),
                          "xgrid_area": (["ncells"], xgrid_area.flatten())},
    ).to_netcdf("remap.nc")


def test_read_weights_conserve():

    pyfms.fms.init(ndomain=1)
    pyfms.horiz_interp.init(ninterp=1)

    pe = pyfms.mpp.pe()

    if pe == pyfms.mpp.root_pe() :
        write_remap()
    pyfms.mpp.sync()

    domain = pyfms.mpp_domains.define_domains([0, nx_dst-1, 0, ny_dst-1])

    interp_id = pyfms.horiz_interp.read_weights_conserve("remap.nc", "fregrid", nx_src, ny_src, domain, src_tile=pyfms.mpp.pe()+1)

    data_src = np.array([[pe*1000 + j*100 + i for i in range(nx_src)] for j in range(ny_src)], dtype=np.float64)

    data_dst = pyfms.horiz_interp.interp(interp_id, data_src, convert_cf_order=False)

    assert np.all(data_dst == data_src)

    pyfms.fms.end()


if __name__ == "__main__":
    test_read_weights_conserve()