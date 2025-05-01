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

    pyfms.fms.init()

    # set domain

    layout = pyfms.mpp_domains.define_layout(global_indices=global_indices, ndivs=4)

    domain = pyfms.mpp_domains.define_domains(
        global_indices=global_indices,
        layout=layout,
        name=name,
        whalo=whalo,
        ehalo=ehalo,
        shalo=shalo,
        nhalo=nhalo,
    )

    assert pyfms.mpp_domains.domain_is_initialized(domain.domain_id)

    pyfms.mpp.set_current_pelist()

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

    pe = pyfms.mpp.pe()

    # set compute and data domains

    pyfms.mpp_domains.set_compute_domain(
        domain_id=domain.domain_id,
        xbegin=isc[pe],
        xend=iec[pe],
        ybegin=jsc[pe],
        yend=jec[pe],
        xsize=2,
        ysize=2,
        whalo=whalo,
        shalo=shalo,
    )

    pyfms.mpp_domains.set_data_domain(
        domain_id=domain.domain_id,
        xbegin=isd[pe],
        xend=ied[pe],
        ybegin=jsd[pe],
        yend=jed[pe],
        xsize=6,
        ysize=6,
        whalo=whalo,
        shalo=shalo,
    )

    compute = pyfms.mpp_domains.get_compute_domain(
        domain_id=domain.domain_id, whalo=whalo, shalo=shalo
    )
    data = pyfms.mpp_domains.get_data_domain(
        domain_id=domain.domain_id, whalo=whalo, shalo=shalo
    )

    domain.update(compute)
    domain.update(data)

    # get domain

    assert domain.isc == isc[pe]
    assert domain.iec == iec[pe]
    assert domain.jsc == jsc[pe]
    assert domain.jec == jec[pe]
    assert domain.xsize_c == 2
    assert domain.ysize_c == 2
    assert domain.xmax_size_c == 2
    assert domain.ymax_size_c == 2
    assert domain.x_is_global_c is False
    assert domain.y_is_global_c is False

    assert domain.isd == isd[pe]
    assert domain.ied == ied[pe]
    assert domain.jsd == jsd[pe]
    assert domain.jed == jed[pe]
    assert domain.xsize_d == 6
    assert domain.ysize_d == 6
    assert domain.xmax_size_d == 6
    assert domain.ymax_size_d == 6

    pyfms.fms.end()


@pytest.mark.remove
def test_remove_input_nml():
    os.remove("input.nml")
    assert not os.path.isfile("input.nml")


if __name__ == "__main__":
    test_getset_domains()
