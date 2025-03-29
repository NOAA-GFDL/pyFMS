import ctypes
from typing import Any

import numpy as np
import numpy.typing as npt

from pyfms.pyfms_utils.data_handling import (
    set_Cchar,
    setscalar_Cint32,
    setscalar_Cfloat,
    setscalar_Cdouble,
    setarray_Cfloat,
    setarray_Cdouble,
    setarray_Cint32,
    setscalar_Cbool,
)


class HorizInterp:
    def __init__(self, cfms: ctypes.CDLL):
        self.cfms = cfms

    def get_maxxgrid(self) -> np.int32:
        self.cfms.get_maxxgrid.restype = np.int32
        return self.cfms.get_maxxgrid()

    def create_xgrid_2dx2d_order1(
        self,
        nlon_src: int,
        nlat_src: int,
        nlon_tgt: int,
        nlat_tgt: int,
        lon_src: npt.NDArray[np.float64],
        lat_src: npt.NDArray[np.float64],
        lon_tgt: npt.NDArray[np.float64],
        lat_tgt: npt.NDArray[np.float64],
        mask_src: npt.NDArray[np.float64],
    ) -> dict:

        ngrid_src = nlon_src * nlat_src
        ngrid_tgt = nlon_tgt * nlat_tgt

        ngrid_src_p1 = (nlon_src + 1) * (nlat_src + 1)
        ngrid_tgt_p1 = (nlon_tgt + 1) * (nlat_tgt + 1)

        maxxgrid = self.get_maxxgrid()

        nlon_src_t = ctypes.c_int
        nlat_src_t = ctypes.c_int
        nlon_tgt_t = ctypes.c_int
        nlat_tgt_t = ctypes.c_int
        maxxgrid_t = ctypes.c_int
        lon_src_ndp = np.ctypeslib.ndpointer(
            dtype=np.float64, shape=(ngrid_src_p1), flags="C_CONTIGUOUS"
        )
        lat_src_ndp = np.ctypeslib.ndpointer(
            dtype=np.float64, shape=(ngrid_src_p1), flags="C_CONTIGUOUS"
        )
        lon_tgt_ndp = np.ctypeslib.ndpointer(
            dtype=np.float64, shape=(ngrid_tgt_p1), flags="C_CONTIGUOUS"
        )
        lat_tgt_ndp = np.ctypeslib.ndpointer(
            dtype=np.float64, shape=(ngrid_tgt_p1), flags="C_CONTIGUOUS"
        )
        mask_src_ndp = np.ctypeslib.ndpointer(
            dtype=np.float64, shape=(ngrid_src_p1), flags="C_CONTIGUOUS"
        )
        i_src_ndp = np.ctypeslib.ndpointer(
            dtype=np.int32, shape=(maxxgrid), flags="C_CONTIGUOUS"
        )
        j_src_ndp = np.ctypeslib.ndpointer(
            dtype=np.int32, shape=(maxxgrid), flags="C_CONTIGUOUS"
        )
        i_tgt_ndp = np.ctypeslib.ndpointer(
            dtype=np.int32, shape=(maxxgrid), flags="C_CONTIGUOUS"
        )
        j_tgt_ndp = np.ctypeslib.ndpointer(
            dtype=np.int32, shape=(maxxgrid), flags="C_CONTIGUOUS"
        )
        xarea_ndp = np.ctypeslib.ndpointer(
            dtype=np.float64, shape=(maxxgrid), flags="C_CONTIGUOUS"
        )

        i_src = np.zeros(maxxgrid, dtype=np.int32)
        j_src = np.zeros(maxxgrid, dtype=np.int32)
        i_tgt = np.zeros(maxxgrid, dtype=np.int32)
        j_tgt = np.zeros(maxxgrid, dtype=np.int32)
        xarea = np.zeros(maxxgrid, dtype=np.float64)

        _create_xgrid = self.cfms.cFMS_create_xgrid_2dx2d_order1

        _create_xgrid.restype = ctypes.c_int
        _create_xgrid.argtypes = [
            ctypes.POINTER(nlon_src_t),
            ctypes.POINTER(nlat_src_t),
            ctypes.POINTER(nlon_tgt_t),
            ctypes.POINTER(nlat_tgt_t),
            lon_src_ndp,
            lat_src_ndp,
            lon_tgt_ndp,
            lat_tgt_ndp,
            mask_src_ndp,
            ctypes.POINTER(maxxgrid_t),
            i_src_ndp,
            j_src_ndp,
            i_tgt_ndp,
            j_tgt_ndp,
            xarea_ndp,
        ]

        nlon_src_c = nlon_src_t(nlon_src)
        nlat_src_c = nlat_src_t(nlat_src)
        nlon_tgt_c = nlon_tgt_t(nlon_tgt)
        nlat_tgt_c = nlat_tgt_t(nlat_tgt)
        maxxgrid_c = maxxgrid_t(maxxgrid)

        nxgrid = _create_xgrid(
            ctypes.byref(nlon_src_c),
            ctypes.byref(nlat_src_c),
            ctypes.byref(nlon_tgt_c),
            ctypes.byref(nlat_tgt_c),
            lon_src,
            lat_src,
            lon_tgt,
            lat_tgt,
            mask_src,
            maxxgrid_c,
            i_src,
            j_src,
            i_tgt,
            j_tgt,
            xarea,
        )

        return {
            "nxgrid": nxgrid,
            "i_src": i_src[:nxgrid],
            "j_src": j_src[:nxgrid],
            "i_tgt": i_tgt[:nxgrid],
            "j_tgt": j_tgt[:nxgrid],
            "xarea": xarea[:nxgrid],
        }

    def horiz_interp_init(self, ninterp: int = None):
        _cfms_horiz_interp_init = self.cfms.cFMS_horiz_interp_init

        ninterp_c, ninterp_t = ctypes.c_int(ninterp), ctypes.POINTER(ctypes.c_int)

        _cfms_horiz_interp_init.argtypes = [ninterp_t]
        _cfms_horiz_interp_init.restype = None

        _cfms_horiz_interp_init(ctypes.byref(ninterp_c))

    def set_current_interp(self, interp_id: int = None):
        _cfms_set_current_interp = self.cfms.cFMS_set_current_interp

        interp_id_c, interp_id_t = ctypes.c_int(interp_id), ctypes.POINTER(ctypes.c_int)

        _cfms_set_current_interp.argtypes = [interp_id_t]
        _cfms_set_current_interp.restype = None

        _cfms_set_current_interp(ctypes.byref(interp_id_c))

    def get_interp(
        self,
        datatype: Any,
        interp_id: int = None,
        nxgrid: int = None,
        ilon: npt.NDArray = None,
        ilon_shape: list[int] = None,
        jlat: npt.NDArray = None,
        jlat_shape: list[int] = None,
        i_lon: npt.NDArray = None,
        i_lon_shape: list[int] = None,
        j_lat: npt.NDArray = None,
        j_lat_shape: list[int] = None,
        found_neighbors: npt.NDArray = None,
        found_neighbors_shape: list[int] = None,
        num_found: npt.NDArray = None,
        num_found_shape: list[int] = None,
        nlon_src: int = None,
        nlat_src: int = None,
        nlon_dst: int = None,
        nlat_dst: int = None,
        interp_method: int = None,
        I_am_initialized: bool = None,
        version: int = None,
        i_src: npt.NDArray = None,
        i_src_shape: int = None,
        j_src: npt.NDArray = None,
        j_src_shape: int = None,
        i_dst: npt.NDArray = None,
        i_dst_shape: int = None,
        j_dst: npt.NDArray = None,
        j_dst_shape: int = None,
        faci: npt.NDArray = None,
        faci_shape: list[int] = None,
        facj: npt.NDArray = None,
        facj_shape: list[int] = None,
        area_src: npt.NDArray = None,
        area_src_shape: list[int] = None,
        area_dst: npt.NDArray = None,
        area_dst_shape: list[int] = None,
        wti: npt.NDArray = None,
        wti_shape: list[int] = None,
        wtj: npt.NDArray = None,
        wtj_shape: list[int] = None,
        src_dist: npt.NDArray = None,
        src_dist_shape: list[int] = None,
        rat_x: npt.NDArray = None,
        rat_x_shape: list[int] = None,
        rat_y: npt.NDArray = None,
        rat_y_shape: list[int] = None,
        lon_in: npt.NDArray = None,
        lon_in_shape: int = None,
        lat_in: npt.NDArray = None,
        lat_in_shape: int = None,
        area_frac_dst: npt.NDArray = None,
        area_frac_dst_shape: int = None,
        mask_in: npt.NDArray = None,
        mask_in_shape: list[int] = None,
        max_src_dist: float = None,
        is_allocated: bool = None,
    ):
        if datatype is np.float64:
            _cfms_get_interp = self.cfms.cFMS_get_interp_cdouble
            faci_t = np.ctypeslib.ndpointer(dtype=np.float64, ndim=2, shape=faci_shape)
            facj_t = np.ctypeslib.ndpointer(dtype=np.float64, ndim=2, shape=facj_shape)
            area_src_t = np.ctypeslib.ndpointer(
                dtype=np.float64, ndim=2, shape=area_src_shape
            )
            area_dst_t = np.ctypeslib.ndpointer(
                dtype=np.float64, ndim=2, shape=area_dst_shape
            )
            wti_t = np.ctypeslib.ndpointer(dtype=np.float64, ndim=3, shape=wti_shape)
            wtj_t = np.ctypeslib.ndpointer(dtype=np.float64, ndim=3, shape=wtj_shape)
            src_dist_t = np.ctypeslib.ndpointer(
                dtype=np.float64, ndim=3, shape=src_dist_shape
            )
            rat_x_t = np.ctypeslib.ndpointer(
                dtype=np.float64, ndim=2, shape=rat_x_shape
            )

    def horiz_interp_new(
            self,
            lon_in: npt.NDArray,
            lon_in_shape: npt.NDArray,
            lat_in: npt.NDArray,
            lat_in_shape: npt.NDArray,
            lon_out: npt.NDArray,
            lon_out_shape: npt.NDArray,
            lat_out: npt.NDArray,
            lat_out_shape: npt.NDArray,
            interp_method: str = None,
            verbose: int = None,
            num_nbrs: int = None,
            max_dist: float = None,
            src_modulo: bool = None,
            mask_in: npt.NDArray = None,
            mask_in_shape: npt.NDArray = None,
            mask_out: npt.NDArray = None,
            mask_out_shape: npt.NDArray = None,
            is_latlon_in: bool = None,
            is_latlon_out: bool = None,
            interp_id: int = None,
    ):
        if interp_method is not None:
            interp_method = interp_method[:128]

        # if statement regarding dim is preemptive for introduction of 1d methods
        if lon_in.dtype == np.float64:
            if lon_in.ndim == 2:
                _cfms_horiz_interp_new = self.cfms.cFMS_horiz_interp_new_2d_cdouble
                lon_in_p, lon_in_t = setarray_Cdouble(lon_in)
                lat_in_p, lat_in_t = setarray_Cdouble(lat_in)
                lon_out_p, lon_out_t = setarray_Cdouble(lon_out)
                lat_out_p, lat_out_t = setarray_Cdouble(lat_out)
                mask_in_p, mask_in_t = setarray_Cdouble(mask_in)
                mask_out_p, mask_out_t = setarray_Cdouble(mask_out)
                max_dist_c, max_dist_t = setscalar_Cdouble(max_dist)   
        if lon_in.dtype == np.float32:
            if lon_in.ndim == 2:
                _cfms_horiz_interp_new = self.cfms.cFMS_horiz_interp_new_2d_cfloat
                lon_in_p, lon_in_t = setarray_Cfloat(lon_in)
                lat_in_p, lat_in_t = setarray_Cfloat(lat_in)
                lon_out_p, lon_out_t = setarray_Cfloat(lon_out)
                lat_out_p, lat_out_t = setarray_Cfloat(lat_out)
                mask_in_p, mask_in_t = setarray_Cfloat(mask_in)
                mask_out_p, mask_out_t = setarray_Cfloat(mask_out)
                max_dist_c, max_dist_t = setscalar_Cfloat(max_dist) 
                
        lon_in_shape_p, lon_in_shape_t = setarray_Cint32(lon_in_shape)
        lat_in_shape_p, lat_in_shape_t = setarray_Cint32(lat_in_shape)
        lon_out_shape_p, lon_out_shape_t = setarray_Cint32(lon_out_shape)
        lat_out_shape_p, lat_out_shape_t = setarray_Cint32(lat_out_shape)
        interp_method_c, interp_method_t = set_Cchar(interp_method)
        verbose_c, verbose_t = setscalar_Cint32(verbose)
        num_nbrs_c, num_nbrs_t = setscalar_Cint32(num_nbrs)
        src_modulo_c, src_modulo_t = setscalar_Cbool(src_modulo)
        mask_in_shape_p, mask_in_shape_t = setarray_Cint32(mask_in_shape)
        mask_out_shape_p, mask_out_shape_t = setarray_Cint32(mask_out_shape)
        is_latlon_in_c, is_latlon_in_t = setscalar_Cbool(is_latlon_in)
        is_latlon_out_c, is_latlon_out_t = setscalar_Cbool(is_latlon_out)
        interp_id_c, interp_id_t = setscalar_Cint32(interp_id)
        
        _cfms_horiz_interp_new.argtypes = [
            lon_in_t,
            lon_in_shape_t,
            lat_in_t,
            lat_in_shape_t,
            lon_out_t,
            lon_out_shape_t,
            lat_out_t,
            lat_out_shape_t,
            interp_method_t,
            verbose_t,
            num_nbrs_t,
            max_dist_t,
            src_modulo_t,
            mask_in_t,
            mask_in_shape_t,
            mask_out_t,
            mask_out_shape_t,
            is_latlon_in_t,
            is_latlon_out_t,
            interp_id_t,
        ]

        _cfms_horiz_interp_new.restype = ctypes.c_int32

        return _cfms_horiz_interp_new(
            lon_in_p,
            lon_in_shape_p,
            lat_in_p,
            lat_in_shape_p,
            lon_out_p,
            lon_out_shape_p,
            lat_out_p,
            lat_out_shape_p,
            interp_method_c,
            verbose_c,
            num_nbrs_c,
            max_dist_c,
            src_modulo_c,
            mask_in_p,
            mask_in_shape_p,
            mask_out_p,
            mask_out_shape_p,
            is_latlon_in_c,
            is_latlon_out_c,
            interp_id_c,
        )


