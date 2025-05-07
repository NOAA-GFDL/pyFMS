class Domain:
    """
    Carries useful information about the domain
    such as array indices corresponding to each domain.
    pyfms.mpp_domains.define() will return an instance of pyDomain.
    Instance variables can be updated with the update method
    by providing the dictionaries returned from
    pyfms.mpp_domains.get_compute_domain and
    pyfms.mpp_domains.get_data_domain
    """

    def __init__(
        self,
        domain_id: int = None,
        isc: int = None,
        jsc: int = None,
        iec: int = None,
        jec: int = None,
        isd: int = None,
        jsd: int = None,
        ied: int = None,
        jed: int = None,
        xsize_c: int = None,
        ysize_c: int = None,
        xmax_size_c: int = None,
        ymax_size_c: int = None,
        x_is_global_c: int = None,
        y_is_global_c: int = None,
        xsize_d: int = None,
        ysize_d: int = None,
        xmax_size_d: int = None,
        ymax_size_d: int = None,
        x_is_global_d: bool = None,
        y_is_global_d: bool = None,
    ):
        self.domain_id = domain_id
        self.isc = isc
        self.jsc = jsc
        self.iec = iec
        self.jec = jec
        self.isd = isd
        self.jsd = jsd
        self.ied = ied
        self.jed = jed
        self.xsize_c = xsize_c
        self.ysize_c = ysize_c
        self.xmax_size_c = xmax_size_c
        self.ymax_size_c = ymax_size_c
        self.x_is_global_c = x_is_global_c
        self.y_is_global_c = y_is_global_c
        self.xsize_d = xsize_d
        self.ysize_d = ysize_d
        self.xmax_size_d = xmax_size_d
        self.ymax_size_d = ymax_size_d
        self.x_is_global_d = x_is_global_d
        self.y_is_global_d = y_is_global_d

    def update(self, domain_dict: dict):
        for key in domain_dict:
            setattr(self, key, domain_dict[key])
        return self
