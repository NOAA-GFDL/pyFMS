import os

import numpy as np
import pytest

from pyfms import pyFMS, pyFMS_mpp, pyFMS_mpp_domains


@pytest.mark.create
def test_create_input_nml():
    inputnml = open("input.nml", "w")
    inputnml.close()
    os.path.isfile("input.nml")


@pytest.mark.parallel
def test_define_domains():

    NX = 96
    NY = 96
    NX_FINE = 48
    NY_FINE = 48
    X_REFINE = 2
    Y_REFINE = 2
    COARSE_NPES = 4
    FINE_NPES = 4

    ndomain = 2
    nnest_domain = 2
    domain_id = 1
    nest_domain_id = 1

    coarse_global_indices = [0, NX - 1, 0, NY - 1]
    coarse_npes = COARSE_NPES
    coarse_pelist = np.empty(shape=COARSE_NPES, dtype=np.int32, order="C")
    coarse_tile_id = 0
    coarse_whalo = 2
    coarse_ehalo = 2
    coarse_shalo = 2
    coarse_nhalo = 2
    coarse_xflags = 3
    coarse_yflags = 2
    is_mosaic = False
    symmetry = False

    fine_global_indices = [0, NX_FINE - 1, 0, NY_FINE - 1]
    fine_npes = FINE_NPES
    fine_pelist = np.empty(shape=FINE_NPES, dtype=np.int32, order="C")
    fine_tile_id = 1
    fine_whalo = 2
    fine_ehalo = 2
    fine_shalo = 2
    fine_nhalo = 2

    cfms_path = "./cFMS/libcFMS/.libs/libcFMS.so"

    assert os.path.exists(cfms_path)

    pyfms = pyFMS(
        cFMS_path=cfms_path,
        ndomain=ndomain,
        nnest_domain=nnest_domain,
    )
    mpp = pyFMS_mpp(cFMS=pyfms.cFMS)
    mpp_domains = pyFMS_mpp_domains(cFMS=pyfms.cFMS)

    assert isinstance(pyfms, pyFMS)

    """get global pelist"""

    npes = mpp.npes()
    pyfms.set_pelist_npes(npes_in=npes)
    global_pelist = mpp.get_current_pelist()

    """set coarse domain as tile=0"""

    for i in range(coarse_npes):
        coarse_pelist[i] = global_pelist[i]
    name_coarse = "test coarse pelist"
    pyfms.set_pelist_npes(npes_in=coarse_npes)
    mpp.declare_pelist(pelist=coarse_pelist, name=name_coarse)

    if mpp.pe() in coarse_pelist:
        pyfms.set_pelist_npes(coarse_npes)
        mpp.set_current_pelist(coarse_pelist)
        name = "test coarse domain"
        maskmap = np.full(shape=(2, 4), fill_value=True, dtype=np.bool_)

        xextent = np.zeros(shape=2, dtype=np.int32, order="C")
        yextent = np.zeros(shape=2, dtype=np.int32, order="C")
        is_mosaic = False

        ndivs = coarse_npes

        layout = mpp_domains.define_layout(
            global_indices=coarse_global_indices,
            ndivs=ndivs,
        )

        mpp_domains.define_domains(
            global_indices=coarse_global_indices,
            layout=layout,
            domain_id=domain_id,
            pelist=coarse_pelist,
            xflags=coarse_xflags,
            yflags=coarse_yflags,
            xextent=xextent,
            yextent=yextent,
            maskmap=maskmap,
            name=name,
            symmetry=symmetry,
            whalo=coarse_whalo,
            ehalo=coarse_ehalo,
            shalo=coarse_shalo,
            nhalo=coarse_nhalo,
            is_mosaic=is_mosaic,
            tile_id=coarse_tile_id,
        )

    mpp.set_current_pelist()

    """set fine domain as tile=1"""

    name_fine = "test fine pelist"
    for i in range(fine_npes):
        fine_pelist[i] = global_pelist[COARSE_NPES + i]
    pyfms.set_pelist_npes(fine_npes)
    mpp.declare_pelist(pelist=fine_pelist, name=name_fine)

    if mpp.pe() in fine_pelist:
        pyfms.set_pelist_npes(fine_npes)
        mpp.set_current_pelist(pelist=fine_pelist)

        name = "test fine domain"
        ndivs = FINE_NPES

        layout = mpp_domains.define_layout(
            global_indices=fine_global_indices,
            ndivs=ndivs,
        )

        mpp_domains.define_domains(
            global_indices=fine_global_indices,
            layout=layout,
            domain_id=domain_id,
            pelist=fine_pelist,
            name=name,
            symmetry=symmetry,
            whalo=fine_whalo,
            ehalo=fine_ehalo,
            shalo=fine_shalo,
            nhalo=fine_nhalo,
            is_mosaic=is_mosaic,
            tile_id=fine_tile_id,
        )

    mpp.set_current_pelist()

    assert mpp_domains.domain_is_initialized(domain_id)

    """set nest domain"""

    name = "test nest domain"
    num_nest = 1
    ntiles = 2
    nest_level = np.array([1], dtype=np.int32, order="C")
    istart_coarse = np.array([24], dtype=np.int32, order="C")
    icount_coarse = np.array([24], dtype=np.int32, order="C")
    jstart_coarse = np.array([24], dtype=np.int32, order="C")
    jcount_coarse = np.array([24], dtype=np.int32, order="C")
    npes_nest_tile = np.array([COARSE_NPES, FINE_NPES], dtype=np.int32, order="C")
    x_refine = np.array([X_REFINE], dtype=np.int32, order="C")
    y_refine = np.array([Y_REFINE], dtype=np.int32, order="C")
    tile_fine = np.array([fine_tile_id], dtype=np.int32, order="C")
    tile_coarse = np.array([coarse_tile_id], dtype=np.int32, order="C")
    nest_domain_id = nest_domain_id
    domain_id = domain_id

    mpp_domains.define_nest_domains(
        num_nest=num_nest,
        ntiles=ntiles,
        nest_level=nest_level,
        tile_fine=tile_fine,
        tile_coarse=tile_coarse,
        istart_coarse=istart_coarse,
        icount_coarse=icount_coarse,
        jstart_coarse=jstart_coarse,
        jcount_coarse=jcount_coarse,
        npes_nest_tile=npes_nest_tile,
        x_refine=x_refine,
        y_refine=y_refine,
        nest_domain_id=nest_domain_id,
        domain_id=domain_id,
        extra_halo=None,
        name=name,
    )

    mpp.set_current_pelist()

    pyfms.pyfms_end()

    # mpp.pyfms_error(errortype=1)


@pytest.mark.remove
def test_remove_input_nml():
    os.remove("input.nml")
    assert not os.path.isfile("input.nml")


if __name__ == "__main__":
    test_define_domains()
