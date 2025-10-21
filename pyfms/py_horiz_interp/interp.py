from pyfms.py_horiz_interp import horiz_interp


class ConserveInterp:
    def __init__(self, interp_id: int, weights_as_fregrid: bool = False):
        # set only for conservative
        self.interp_id = interp_id
        self.nxgrid = horiz_interp.get_nxgrid(interp_id)
        self.i_src = horiz_interp.get_i_src(interp_id)
        self.j_src = horiz_interp.get_j_src(interp_id)
        self.i_dst = horiz_interp.get_i_dst(interp_id)
        self.j_dst = horiz_interp.get_j_dst(interp_id)
        self.nlon_src = horiz_interp.get_nlon_src(interp_id)
        self.nlat_src = horiz_interp.get_nlat_src(interp_id)
        self.nlon_dst = horiz_interp.get_nlon_dst(interp_id)
        self.nlat_dst = horiz_interp.get_nlat_dst(interp_id)
        self.interp_method = horiz_interp.get_interp_method(interp_id)
        self.get_area_frac_dst = horiz_interp.get_area_frac_dst(interp_id)

        self.xgrid_area = None
        if weights_as_fregrid:
            self.xgrid_area = horiz_interp.get_xgrid_area(interp_id)
