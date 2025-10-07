import numpy as np

import pyfms


def test_gather():

    nx, ny = 32, 64
    global_indices = [0, nx-1, 0, ny-1]
    
    pyfms.fms.init(ndomain=2)

    #define domain
    layout = pyfms.mpp_domains.define_layout(global_indices, pyfms.mpp.npes())
    domain = pyfms.mpp_domains.define_domains(global_indices, layout)

    print('here', pyfms.mpp.npes(), layout, global_indices)
    pyfms.fms.end()
    exit()
    
    #data to send
    pe = pyfms.mpp.pe()
    send = np.array([[i*100 + j for j in range(domain.jsc, domain.jec)] for i in range(domain.isc, domain.iec)], dtype=np.float64)

    pelist = pyfms.mpp.get_current_pelist(pyfms.mpp.npes())
    gathered = pyfms.mpp.gather(domain, send, pelist=pelist)

    pyfms.fms.end()

    answers = np.array([[i*100+j for j in range(ny)] for i in range(nx)], dtype=np.float64)

    if pe == pyfms.mpp.root_pe():
        assert np.all(answers == gathered)
    else:
        assert gathered is None
    
