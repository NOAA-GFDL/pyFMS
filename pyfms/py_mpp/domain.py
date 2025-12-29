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
        isg: int = None,
        ieg: int = None,
        jsg: int = None,
        jeg: int = None,
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
        xsize_g: int = None,
        ysize_g: int = None,
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
        self.isg = isg  # xbegin in global domain
        self.ieg = ieg  # xend in global domain
        self.jsg = jsg  # ybegin in global domain
        self.jeg = jeg  # yend in global domain
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
        self.xsize_g = xsize_g  # size of the global domain in x direction
        self.ysize_g = ysize_g  # size of the global domain in the y direction
        self.x_is_global_d = x_is_global_d  # x_is_global in data domain
        self.y_is_global_d = y_is_global_d  # y_is_global in data domain

    def update(self, domain_dict: dict):
        for key in domain_dict:
            setattr(self, key, domain_dict[key])
        return self

    def __repr__(self):

        repr_str = f"""
            domain_id: {self.domain_id}\n
            ** compute domain **
            (isc, jsc): ({self.isc}, {self.jsc})
            (iec, jec): ({self.iec}, {self.jec})
            (xsize_c, ysize_c): ({self.xsize_c}, {self.ysize_c})
            (xmax_size_c, ymax_size_c): ({self.xmax_size_c}, {self.ymax_size_c})
            (x_is_global_c, y_is_global_c): ({self.x_is_global_c}, {self.y_is_global_c})\n
            ** data domain **
            (isd, jsd) = ({self.isd}, {self.jsd})
            (ied, jed) = ({self.ied}, {self.jed})
            (xsize_d, ysize_d): ({self.xsize_d}, {self.ysize_d})
            (xmax_size_d, ymax_size_d): ({self.xmax_size_d}, {self.ymax_size_d})
            (x_is_global_d, y_is_global_d): ({self.x_is_global_d}, {self.y_is_global_d})\n
            ** global domain **
            (isg, jsg) = ({self.isg}, {self.jsg})
            (ieg, jeg) = ({self.ieg}, {self.jeg})
            (xsize_g, ysize_g) = ({self.xsize_g}, {self.ysize_g})
            (xmax_size_g, ymax_size_g): ({self.xmax_size_d}, {self.ymax_size_d})
            (x_is_global_d, y_is_global_d): ({self.x_is_global_d}, {self.y_is_global_d})
        """

        return repr_str
