import numpy as np

import pyfms


def test_gather_2d():

    pyfms.fms.init(ndomain=2)

    for convert in [True, False]:

        nx, ny = 12, 24
        global_indices = [0, nx - 1, 0, ny - 1]

        # define domain
        layout = pyfms.mpp_domains.define_layout(global_indices, pyfms.mpp.npes())
        domain = pyfms.mpp_domains.define_domains(global_indices, layout)

        is_root_pe = pyfms.mpp.pe() == pyfms.mpp.root_pe()

        # data to send
        global_data = np.array(
            [[i * 100 + j for j in range(ny)] for i in range(nx)], dtype=np.float64
        )
        send = global_data[domain.isc : domain.iec + 1, domain.jsc : domain.jec + 1]

        if not convert:
            global_data = global_data.T
            send = send.T

        rbuf_shape = None
        if is_root_pe:
          if convert:
            rbuf_shape = [nx, ny]
          else:
            rbuf_shape = [ny, nx]


        pelist = pyfms.mpp.get_current_pelist(pyfms.mpp.npes())
        gathered = pyfms.mpp.gather(
            send, rbuf_shape=rbuf_shape, domain=domain, pelist=pelist, convert_cf_order=convert
        )

        if pyfms.mpp.pe() == pyfms.mpp.root_pe():
            assert np.all(global_data == gathered)
        else:
            assert gathered is None

    pyfms.fms.end()


def test_gather_1d():

    sbuf_size = 5

    def buffer(ipe):
        return [ipe * 10 + i for i in range(sbuf_size)]

    pyfms.fms.init()

    pe = pyfms.mpp.pe()
    npes = pyfms.mpp.npes()
    is_root_pe = pyfms.mpp.pe() == pyfms.mpp.root_pe()

    send = np.array(buffer(pe), dtype=np.float64)

    if is_root_pe:
      rbuf_size = sbuf_size * npes
    else:
      rbuf_size = None

    receive = pyfms.mpp.gather(np.array(send), rbuf_size=rbuf_size)

    if is_root_pe:
        answers = []
        for ipe in range(npes):
            answers += buffer(ipe)
        np.testing.assert_array_equal(receive, answers)
    else:
        assert receive is None

    pyfms.fms.end()


def test_gatherv_1d():

    def buffer(ipe):
        return [ipe * 10 + i for i in range(ipe + 2)]

    pyfms.fms.init()
    pe = pyfms.mpp.pe()
    is_root_pe = pe == pyfms.mpp.root_pe()

    sbuf = np.array(buffer(pe), dtype=np.float64)

    if is_root_pe:
      rsize = [ipe + 2 for ipe in range(pyfms.mpp.npes())]
    else:
      rsize = None

    receive = pyfms.mpp.gatherv(sbuf, ssize=pe + 2, rsize=rsize)

    if is_root_pe:
        answers = []
        for ipe in range(pyfms.mpp.npes()):
            answers += buffer(ipe)
        np.testing.assert_array_equal(receive, answers)
    else:
        assert receive is None

    pyfms.fms.end()
