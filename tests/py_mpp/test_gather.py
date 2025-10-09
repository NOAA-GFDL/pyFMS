import numpy as np

import pyfms


def test_gather():

    pyfms.fms.init(ndomain=2)

    for convert in [True, False]:

        nx, ny = 12, 24
        global_indices = [0, nx - 1, 0, ny - 1]

        # define domain
        layout = pyfms.mpp_domains.define_layout(global_indices, pyfms.mpp.npes())
        domain = pyfms.mpp_domains.define_domains(global_indices, layout)

        # data to send
        global_data = np.array(
            [[i * 100 + j for j in range(ny)] for i in range(nx)], dtype=np.float64
        )
        send = global_data[domain.isc : domain.iec + 1, domain.jsc : domain.jec + 1]

        if not convert:
            global_data = global_data.T
            send = send.T

        pelist = pyfms.mpp.get_current_pelist(pyfms.mpp.npes())
        gathered = pyfms.mpp.gather(
            domain, send, pelist=pelist, convert_cf_order=convert
        )

        if pyfms.mpp.pe() == pyfms.mpp.root_pe():
            assert np.all(global_data == gathered)
        else:
            assert gathered is None

    pyfms.fms.end()
