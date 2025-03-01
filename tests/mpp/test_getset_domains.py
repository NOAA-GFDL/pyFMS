import numpy as np

from pyfms.mpp.pyfms_mpp import pyFMS_mpp
from pyfms.mpp.pyfms_mpp_domains import pyDomain, pyFMS_mpp_domains
from pyfms.pyfms_fms import pyFMS


def test_getset_domains():
    """
    global domain
          *     *     *     *
          *     *     *     *
    * * (2,5) (3,5) (4,5) (5,5) * *
    * * (2,4) (3,4) (4,4) (5,4) * *
    * * (2,3) (3,3) (4,3) (5,3) * *
    * * (2,2) (3,2) (4,2) (5,2) * *
          *     *     *     *
          *     *     *     *
    """
    domain_id = 0
    ndiv = 4
    global_indices = np.array([0, 3, 0, 3], dtype=np.int32, order="C")
    whalo = 2
    ehalo = 2
    shalo = 2
    nhalo = 2
    name = "test domain"

    pyfms = pyFMS(clibFMS_path="./cFMS/libcFMS/.libs/libcFMS.so")
    mpp = pyFMS_mpp(clibFMS=pyfms.clibFMS)
    mpp_domains = pyFMS_mpp_domains(clibFMS=pyfms.clibFMS)

    # set domain

    layout = mpp_domains.define_layout(global_indices=global_indices, ndivs=ndiv)

    domain = pyDomain(
        global_indices=global_indices,
        layout=layout,
        mpp_domains_obj=mpp_domains,
        domain_id=domain_id,
        name=name,
        whalo=whalo,
        ehalo=ehalo,
        shalo=shalo,
        nhalo=nhalo,
    )

    if not mpp_domains.domain_is_initialized(domain_id):
        mpp.pyfms_error(1, "error in setting domain")

    mpp.set_current_pelist()

    """
    flipping the domain:
    pe 0: isc=2, iec=3, jsc=2, jec=3 --> pe 3
    pe 1: isc=4, iec=5, jsc=2, jec=3 --> pe 2
    pe 2: isc=2, iec=3, jsc=4, jec=5 --> pe 1
    pe 3: isc=4, iec=5, jsc=4, jec=5 --> pe 0
    """

    isc = np.array([4, 2, 4, 2], dtype=np.int32, order="C")
    iec = np.array([5, 3, 5, 3], dtype=np.int32, order="C")
    jsc = np.array([4, 4, 2, 2], dtype=np.int32, order="C")
    jec = np.array([5, 5, 3, 3], dtype=np.int32, order="C")

    """
    pe 0: isd=0, ied=5, jsd=0, jed=5 --> pe 3
    pe 1: isd=2, ied=7, jsd=0, jed=5 --> pe 2
    pe 2: isd=0, ied=5, jsd=2, jed=7 --> pe 1
    pe 3: isd=2, ied=7, jsd=2, jed=7 --> pe 0
    """

    isd = np.array([2, 0, 2, 0], dtype=np.int32, order="C")
    ied = np.array([7, 5, 7, 5], dtype=np.int32, order="C")
    jsd = np.array([2, 2, 0, 0], dtype=np.int32, order="C")
    jed = np.array([7, 7, 5, 5], dtype=np.int32, order="C")

    pe = mpp.pe()
    tile_count = 0
    x_is_global = False
    y_is_global = False

    # set compute and data domains

    xsize = 2
    ysize = 2

    domain.set_compute_domain(
        domain_id=domain_id,
        xbegin=isc[pe],
        xend=iec[pe],
        ybegin=jsc[pe],
        yend=jec[pe],
        xsize=xsize,
        ysize=ysize,
        x_is_global=x_is_global,
        y_is_global=y_is_global,
        tile_count=tile_count,
        whalo=whalo,
        shalo=shalo,
    )

    xsize = 6
    ysize = 6

    domain.set_data_domain(
        domain_id=domain_id,
        xbegin=isd[pe],
        xend=ied[pe],
        ybegin=jsd[pe],
        yend=jed[pe],
        xsize=xsize,
        ysize=ysize,
        x_is_global=x_is_global,
        y_is_global=y_is_global,
        tile_count=tile_count,
        whalo=whalo,
        shalo=shalo,
    )

    # get domain

    # out_compute_domain = domain.compute_domain

    assert domain.compute_domain.xbegin.value == isc[pe]
    assert domain.compute_domain.xend.value == iec[pe]
    assert domain.compute_domain.ybegin.value == jsc[pe]
    assert domain.compute_domain.yend.value == jec[pe]
    assert domain.compute_domain.xsize.value == 2
    assert domain.compute_domain.ysize.value == 2
    assert domain.compute_domain.xmax_size.value == 2
    assert domain.compute_domain.ymax_size.value == 2
    assert domain.compute_domain.x_is_global.value is False
    assert domain.compute_domain.y_is_global.value is False

    # out_data_domain = domain.data_domain

    assert domain.data_domain.xbegin.value == isd[pe]
    assert domain.data_domain.xend.value == ied[pe]
    assert domain.data_domain.ybegin.value == jsd[pe]
    assert domain.data_domain.yend.value == jed[pe]
    assert domain.data_domain.xsize.value == 6
    assert domain.data_domain.ysize.value == 6
    assert domain.data_domain.xmax_size.value == 6
    assert domain.data_domain.ymax_size.value == 6

    # xbcd2 = out_compute_domain.xbegin.value
    # xbdd = out_data_domain.xbegin.value
    # xbcd = domain.compute_domain.xbegin.value
    # xbdd = domain.data_domain.xbegin.value
    # xbcd2 = domain.compute_domain.xbegin.value
    # xbdd2 = domain.data_domain.xbegin.value
    # print(f"id of xbcdf = {id(xbcd)},id of xbdd = {id(xbdd)}")
    # print(f"id of xbcd = {id(xbcd)},id of xbcd2 = {id(xbcd2)}")
    # print(f"xbcd = {xbcd}, xbdd = {xbdd}, xbcd2 = {xbcd2}, xbdd2 = {xbdd2}")
    # print(f"xbcd = {xbcd}, xbcd2 = {xbcd2}")
    # print(f"id of domain.compute_domain = {id(domain.compute_domain)}, id of out_compute_domain = {id(out_compute_domain)}")

    pyfms.pyfms_end()


if __name__ == "__main__":
    test_getset_domains()
