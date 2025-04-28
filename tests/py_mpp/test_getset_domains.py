import os

import pytest

import pyfms


@pytest.mark.create
def test_create_input_nml():
    inputnml = open("input.nml", "w")
    inputnml.close()
    assert os.path.isfile("input.nml")


@pytest.mark.parallel
def test_getset_domains():
    """
    copied from cFMS
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
    global_indices = [0, 3, 0, 3]
    whalo = 2
    ehalo = 2
    shalo = 2
    nhalo = 2
    name = "test domain"

    pyfms_obj = pyfms.pyFMS(cFMS_path="./cFMS/libcFMS/.libs/libcFMS.so")
    mpp_obj = pyfms.mpp(cFMS=pyfms_obj.cFMS)
    mpp_domains_obj = pyfms.mpp_domains(cFMS=pyfms_obj.cFMS)

    # set domain

    layout = mpp_domains_obj.define_layout(global_indices=global_indices, ndivs=4)

    domain = mpp_domains_obj.define_domains(
        global_indices=global_indices,
        layout=layout,
        name=name,
        whalo=whalo,
        ehalo=ehalo,
        shalo=shalo,
        nhalo=nhalo,
    )

    assert mpp_domains_obj.domain_is_initialized(domain.domain_id)

    mpp_obj.set_current_pelist()

    """
    flipping the domain:
    pe 0: isc=2, iec=3, jsc=2, jec=3 --> pe 3
    pe 1: isc=4, iec=5, jsc=2, jec=3 --> pe 2
    pe 2: isc=2, iec=3, jsc=4, jec=5 --> pe 1
    pe 3: isc=4, iec=5, jsc=4, jec=5 --> pe 0
    """

    isc = [4, 2, 4, 2]
    iec = [5, 3, 5, 3]
    jsc = [4, 4, 2, 2]
    jec = [5, 5, 3, 3]

    """
    pe 0: isd=0, ied=5, jsd=0, jed=5 --> pe 3
    pe 1: isd=2, ied=7, jsd=0, jed=5 --> pe 2
    pe 2: isd=0, ied=5, jsd=2, jed=7 --> pe 1
    pe 3: isd=2, ied=7, jsd=2, jed=7 --> pe 0
    """

    isd = [2, 0, 2, 0]
    ied = [7, 5, 7, 5]
    jsd = [2, 2, 0, 0]
    jed = [7, 7, 5, 5]

    pe = mpp_obj.pe()
    tile_count = 0
    x_is_global = False
    y_is_global = False

    # set compute and data domains

    mpp_domains_obj.set_compute_domain(
        domain_id=domain.domain_id,
        xbegin=isc[pe],
        xend=iec[pe],
        ybegin=jsc[pe],
        yend=jec[pe],
        xsize=2,
        ysize=2,
        x_is_global=x_is_global,
        y_is_global=y_is_global,
        whalo=whalo,
        shalo=shalo,
    )

    mpp_domains_obj.set_data_domain(
        domain_id=domain.domain_id,
        xbegin=isd[pe],
        xend=ied[pe],
        ybegin=jsd[pe],
        yend=jed[pe],
        xsize=6,
        ysize=6,
        x_is_global=x_is_global,
        y_is_global=y_is_global,
        whalo=whalo,
        shalo=shalo,
    )

    compute = mpp_domains_obj.get_compute_domain(
        domain_id=domain.domain_id, whalo=whalo, shalo=shalo
    )
    data = mpp_domains_obj.get_data_domain(
        domain_id=domain.domain_id, whalo=whalo, shalo=shalo
    )

    # get domain

    assert compute["xbegin"] == isc[pe]
    assert compute["xend"] == iec[pe]
    assert compute["ybegin"] == jsc[pe]
    assert compute["yend"] == jec[pe]
    assert compute["xsize"] == 2
    assert compute["ysize"] == 2
    assert compute["xmax_size"] == 2
    assert compute["ymax_size"] == 2
    assert compute["x_is_global"] is False
    assert compute["y_is_global"] is False

    assert data["xbegin"] == isd[pe]
    assert data["xend"] == ied[pe]
    assert data["ybegin"] == jsd[pe]
    assert data["yend"] == jed[pe]
    assert data["xsize"] == 6
    assert data["ysize"] == 6
    assert data["xmax_size"] == 6
    assert data["ymax_size"] == 6

    pyfms_obj.pyfms_end()


@pytest.mark.remove
def test_remove_input_nml():
    os.remove("input.nml")
    assert not os.path.isfile("input.nml")


if __name__ == "__main__":
    test_getset_domains()
