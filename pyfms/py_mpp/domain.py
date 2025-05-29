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
        self.domain_id = domain_id  # domain_id
        self.isc = isc  # xbegin in compute domain
        self.jsc = jsc  # ybeing in compute domain
        self.iec = iec  # xend in compute domain
        self.jec = jec  # yend in compute domain
        self.isd = isd  # xbegin in data_domain
        self.jsd = jsd  # ybegin in data_domain
        self.ied = ied  # xend in data_domain
        self.jed = jed  # yend in data_domain
        self.xsize_c = xsize_c  # xsize in compute domain
        self.ysize_c = ysize_c  # ysize in compute domain
        self.xmax_size_c = xmax_size_c  # xmax_size in compute domain
        self.ymax_size_c = ymax_size_c  # ymax_size in compute domain
        self.x_is_global_c = x_is_global_c  # x_is_global for compute domain
        self.y_is_global_c = y_is_global_c  # y_is_global for compute_domain
        self.xsize_d = xsize_d  # xsize in data domain
        self.ysize_d = ysize_d  # ysize in data_domain
        self.xmax_size_d = xmax_size_d  # xmax_size in data domain
        self.ymax_size_d = ymax_size_d  # ymax_size in data domain
        self.x_is_global_d = x_is_global_d  # x_is_global in data domain
        self.y_is_global_d = y_is_global_d  # y_is_global in data domain

    def update(self, domain_dict: dict):
        for key in domain_dict:
            setattr(self, key, domain_dict[key])
        return self
