from pyfms.py_horiz_interp import horiz_interp


class Interp:
    def __init__(self, interp_id: int):
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
        self.area_frac_dst = horiz_interp.get_area_frac_dst(interp_id)

    def __repr__(self):

        repr_str = f"""
            interp_id: {self.interp_id}
            nxgrid: {self.nxgrid}
            nlon_src: {self.nlon_src}
            nlat_src: {self.nlat_src}
            nlon_dst: {self.nlon_dst}
            nlat_dst: {self.nlat_dst}
            interp_method: {self.interp_method}
            i_src_minmax: [{self.i_src.min()}, {self.i_src.max()}]
            j_src_minmax [{self.j_src.min()}, {self.j_src.max()}]
            i_dst_minmax: [{self.i_dst.min()}, {self.i_dst.max()}]
            j_dst_minmax: [{self.j_dst.min()}, {self.j_dst.max()}]
            area_frac_dst_minmax: [{self.area_frac_dst.min()}, {self.area_frac_dst.max()}]
        """

        return repr_str
