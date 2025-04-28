import ctypes

import numpy as np
from numpy.typing import NDArray

from ..pyfms_utils.data_handling import (
    set_Cchar,
    setarray_Cbool,
    setarray_Cdouble,
    setarray_Cfloat,
    setarray_Cint32,
    setscalar_Cbool,
    setscalar_Cint32,
)

class mpp_domains:

    GLOBAL_DATA_DOMAIN: int = None
    BGRID_NE: int = None
    CGRID_NE: int = None
    DGRID_NE: int = None
    AGRID: int = None
    FOLD_SOUTH_EDGE: int = None
    FOLD_WEST_EDGE: int = None
    FOLD_EAST_EDGE: int = None
    CYCLIC_GLOBAL_DOMAIN: int = None
    NUPDATE: int = None
    EUPDATE: int = None
    XUPDATE: int = None
    YUPDATE: int = None
    NORTH: int = None
    NORTH_EAST: int = None
    EAST: int = None
    SOUTH_EAST: int = None
    CORNER: int = None
    CENTER: int = None
    SOUTH: int = None
    SOUTH_WEST: int = None

    def __init__(self, cFMS: ctypes.CDLL = None):
        self.cFMS = cFMS
        self.GLOBAL_DATA_DOMAIN = ctypes.c_int.in_dll(
            self.cFMS, "GLOBAL_DATA_DOMAIN"
        ).value
        self.BGRID_NE = ctypes.c_int.in_dll(self.cFMS, "BGRID_NE").value
        self.CGRID_NE = ctypes.c_int.in_dll(self.cFMS, "CGRID_NE").value
        self.DGRID_NE = ctypes.c_int.in_dll(self.cFMS, "DGRID_NE").value
        self.AGRID = ctypes.c_int.in_dll(self.cFMS, "AGRID").value
        self.FOLD_SOUTH_EDGE = ctypes.c_int.in_dll(self.cFMS, "FOLD_SOUTH_EDGE").value
        self.FOLD_WEST_EDGE = ctypes.c_int.in_dll(self.cFMS, "FOLD_WEST_EDGE").value
        self.FOLD_EAST_EDGE = ctypes.c_int.in_dll(self.cFMS, "FOLD_EAST_EDGE").value
        self.CYCLIC_GLOBAL_DOMAIN = ctypes.c_int.in_dll(
            self.cFMS, "CYCLIC_GLOBAL_DOMAIN"
        ).value
        self.NUPDATE = ctypes.c_int.in_dll(self.cFMS, "NUPDATE").value
        self.EUPDATE = ctypes.c_int.in_dll(self.cFMS, "EUPDATE").value
        self.XUPDATE = ctypes.c_int.in_dll(self.cFMS, "XUPDATE").value
        self.YUPDATE = ctypes.c_int.in_dll(self.cFMS, "YUPDATE").value
        self.NORTH = ctypes.c_int.in_dll(self.cFMS, "NORTH").value
        self.NORTH_EAST = ctypes.c_int.in_dll(self.cFMS, "NORTH_EAST").value
        self.EAST = ctypes.c_int.in_dll(self.cFMS, "EAST").value
        self.SOUTH_EAST = ctypes.c_int.in_dll(self.cFMS, "SOUTH_EAST").value
        self.CORNER = ctypes.c_int.in_dll(self.cFMS, "CORNER").value
        self.CENTER = ctypes.c_int.in_dll(self.cFMS, "CENTER").value
        self.SOUTH = ctypes.c_int.in_dll(self.cFMS, "SOUTH").value
        self.SOUTH_WEST = ctypes.c_int.in_dll(self.cFMS, "SOUTH_WEST").value
        self.WEST = ctypes.c_int.in_dll(self.cFMS, "WEST").value
        self.NORTH_WEST = ctypes.c_int.in_dll(self.cFMS, "NORTH_WEST").value

    """
    Subroutine: define_domains

    This method will pass its arguments to set the values for a domain

    Returns: In the Fortan source, global_indices, tile_count, and
    tile_id will be updated. The NumPy array passed for the
    global_indices argument will be updated automatically, the objects
    passed for the tile_count and tile_id arguments should also be set
    to the result of the method to update their values.
    """

    def define_domains(
        self,
        global_indices: list[int],
        layout: list[int],
        pelist: list[int] = None,
        xflags: int = None,
        yflags: int = None,
        xhalo: int = None,
        yhalo: int = None,
        xextent: list[int] = None,
        yextent: list[int] = None,
        maskmap: list[list[np.bool_]] = None,
        name: str = None,
        symmetry: bool = None,
        memory_size: list[int] = None,
        whalo: int = None,
        ehalo: int = None,
        shalo: int = None,
        nhalo: int = None,
        is_mosaic: bool = None,
        tile_count: int = None,
        tile_id: int = None,
        complete: bool = None,
        x_cyclic_offset: int = None,
        y_cyclic_offset: int = None,
    ) -> pyDomain:

        _cfms_define_domains = self.cFMS.cFMS_define_domains

        global_indices_arr = np.array(global_indices, dtype=np.int32)
        layout_arr = np.array(layout, dtype=np.int32)
        xextent_arr = np.array(xextent, dtype=np.int32) if xextent is not None else None
        yextent_arr = np.array(yextent, dtype=np.int32) if yextent is not None else None
        maskmap_arr = np.array(maskmap, dtype=np.bool_) if maskmap is not None else None
        memory_size_arr = (
            np.array(memory_size, dtype=np.int32) if memory_size is not None else None
        )

        if pelist is not None:
            pelist_arr = np.array(pelist, dtype=np.int32)
            npelist = len(pelist)
        else:
            pelist_arr = None
            npelist = 1

        global_indices_p, global_indices_t = setarray_Cint32(global_indices_arr)
        layout_p, layout_t = setarray_Cint32(layout_arr)
        npelist_c, npelist_t = setscalar_Cint32(npelist)
        pelist_p, pelist_t = setarray_Cint32(pelist_arr)
        xflags_c, xflags_t = setscalar_Cint32(xflags)
        yflags_c, yflags_t = setscalar_Cint32(yflags)
        xhalo_c, xhalo_t = setscalar_Cint32(xhalo)
        yhalo_c, yhalo_t = setscalar_Cint32(yhalo)
        xextent_p, xextent_t = setarray_Cint32(xextent_arr)
        yextent_p, yextent_t = setarray_Cint32(yextent_arr)
        maskmap_p, maskmap_t = setarray_Cbool(maskmap_arr)
        name_c, name_t = set_Cchar(name)
        symmetry_c, symmetry_t = setscalar_Cbool(symmetry)
        memory_size_p, memory_size_t = setarray_Cint32(memory_size_arr)
        whalo_c, whalo_t = setscalar_Cint32(whalo)
        ehalo_c, ehalo_t = setscalar_Cint32(ehalo)
        shalo_c, shalo_t = setscalar_Cint32(shalo)
        nhalo_c, nhalo_t = setscalar_Cint32(nhalo)
        is_mosaic_c, is_mosaic_t = setscalar_Cbool(is_mosaic)
        tile_count_c, tile_count_t = setscalar_Cint32(tile_count)
        tile_id_c, tile_id_t = setscalar_Cint32(tile_id)
        complete_c, complete_t = setscalar_Cbool(complete)
        x_cyclic_offset_c, x_cyclic_offset_t = setscalar_Cint32(x_cyclic_offset)
        y_cyclic_offset_c, y_cyclic_offset_t = setscalar_Cint32(y_cyclic_offset)

        _cfms_define_domains.argtypes = [
            global_indices_t,
            layout_t,
            npelist_t,
            pelist_t,
            xflags_t,
            yflags_t,
            xhalo_t,
            yhalo_t,
            xextent_t,
            yextent_t,
            maskmap_t,
            name_t,
            symmetry_t,
            memory_size_t,
            whalo_t,
            ehalo_t,
            shalo_t,
            nhalo_t,
            is_mosaic_t,
            tile_count_t,
            tile_id_t,
            complete_t,
            x_cyclic_offset_t,
            y_cyclic_offset_t,
        ]

        _cfms_define_domains.restype = ctypes.c_int

        domain_id = _cfms_define_domains(
            global_indices_p,
            layout_p,
            npelist_c,
            pelist_p,
            xflags_c,
            yflags_c,
            xhalo_c,
            yhalo_c,
            xextent_p,
            yextent_p,
            maskmap_p,
            name_c,
            symmetry_c,
            memory_size_p,
            whalo_c,
            ehalo_c,
            shalo_c,
            nhalo_c,
            is_mosaic_c,
            tile_count_c,
            tile_id_c,
            complete_c,
            x_cyclic_offset_c,
            y_cyclic_offset_c,
        )

        return pyDomain(domain_id=domain_id, layout=layout, tile=tile_id)

    """
    Subroutine: define_io_domains

    Arguments of this method will define data for I/O domain

    Returns: No return
    """

    def define_io_domain(self, io_layout: list[int], domain_id: int):
        _cfms_define_io_domain = self.cFMS.cFMS_define_io_domain

        io_layout_arr = np.array(io_layout, dtype=np.int32)

        io_layout_p, io_layout_t = setarray_Cint32(io_layout_arr)
        domain_id_c, domain_id_t = setscalar_Cint32(domain_id)

        _cfms_define_io_domain.argtypes = [io_layout_t, domain_id_t]
        _cfms_define_io_domain.restype = None

        _cfms_define_io_domain(io_layout_p, domain_id_c)

    """
    Subroutine: define_layout

    Arguments passed to this method will define the layout to be used

    Returns: A NDArray containing the layout
    """

    def define_layout(
        self,
        global_indices: list[int],
        ndivs: int,
    ) -> list:

        layout = np.empty(shape=2, dtype=np.int32, order="C")

        global_indices_arr = np.array(global_indices, dtype=np.int32)

        _cfms_define_layout = self.cFMS.cFMS_define_layout

        global_indices_p, global_indices_t = setarray_Cint32(global_indices_arr)
        ndivs_c, ndivs_t = setscalar_Cint32(ndivs)
        layout_p, layout_t = setarray_Cint32(layout)

        _cfms_define_layout.argtypes = [global_indices_t, ndivs_t, layout_t]
        _cfms_define_layout.restype = None

        _cfms_define_layout(global_indices_p, ndivs_c, layout_p)

        return layout.tolist()

    """
    Subroutine: define_nest_domains

    Arguments passed to this method will define data for nest domains

    Returns: No return
    """

    def define_nest_domains(
        self,
        num_nest: int,
        ntiles: int,
        nest_level: list[int],
        tile_fine: list[int],
        tile_coarse: list[int],
        istart_coarse: list[int],
        icount_coarse: list[int],
        jstart_coarse: list[int],
        jcount_coarse: list[int],
        npes_nest_tile: list[int],
        x_refine: list[int],
        y_refine: list[int],
        domain_id: int,
        extra_halo: int = None,
        name: str = None,
    ) -> int:
        _cfms_define_nest_domain = self.cFMS.cFMS_define_nest_domains

        nest_level_arr = np.array(nest_level, dtype=np.int32)
        tile_fine_arr = np.array(tile_fine, dtype=np.int32)
        tile_coarse_arr = np.array(tile_coarse, dtype=np.int32)
        istart_coarse_arr = np.array(istart_coarse, dtype=np.int32)
        jstart_coarse_arr = np.array(jstart_coarse, dtype=np.int32)
        icount_coarse_arr = np.array(icount_coarse, dtype=np.int32)
        jcount_coarse_arr = np.array(jcount_coarse, dtype=np.int32)
        npes_nest_tile_arr = np.array(npes_nest_tile, dtype=np.int32)
        x_refine_arr = np.array(x_refine, dtype=np.int32)
        y_refine_arr = np.array(y_refine, dtype=np.int32)

        num_nest_p, num_nest_t = setscalar_Cint32(num_nest)
        ntiles_c, ntiles_t = setscalar_Cint32(ntiles)
        nest_level_p, nest_level_t = setarray_Cint32(nest_level_arr)
        tile_fine_p, tile_fine_t = setarray_Cint32(tile_fine_arr)
        tile_coarse_p, tile_coarse_t = setarray_Cint32(tile_coarse_arr)
        istart_coarse_p, istart_coarse_t = setarray_Cint32(istart_coarse_arr)
        icount_coarse_p, icount_coarse_t = setarray_Cint32(icount_coarse_arr)
        jstart_coarse_p, jstart_coarse_t = setarray_Cint32(jstart_coarse_arr)
        jcount_coarse_p, jcount_coarse_t = setarray_Cint32(jcount_coarse_arr)
        npes_nest_tile_p, npes_nest_tile_t = setarray_Cint32(npes_nest_tile_arr)
        x_refine_p, x_refine_t = setarray_Cint32(x_refine_arr)
        y_refine_p, y_refine_t = setarray_Cint32(y_refine_arr)
        domain_id_c, domain_id_t = setscalar_Cint32(domain_id)
        extra_halo_c, extra_halo_t = setscalar_Cint32(extra_halo)
        name_p, name_t = set_Cchar(name)

        _cfms_define_nest_domain.argtypes = [
            num_nest_t,
            ntiles_t,
            nest_level_t,
            tile_fine_t,
            tile_coarse_t,
            istart_coarse_t,
            icount_coarse_t,
            jstart_coarse_t,
            jcount_coarse_t,
            npes_nest_tile_t,
            x_refine_t,
            y_refine_t,
            domain_id_t,
            extra_halo_t,
            name_t,
        ]
        _cfms_define_nest_domain.restype = ctypes.c_int

        return _cfms_define_nest_domain(
            num_nest_p,
            ntiles_c,
            nest_level_p,
            tile_fine_p,
            tile_coarse_p,
            istart_coarse_p,
            icount_coarse_p,
            jstart_coarse_p,
            jcount_coarse_p,
            npes_nest_tile_p,
            x_refine_p,
            y_refine_p,
            domain_id_c,
            extra_halo_c,
            name_p,
        )

    """
    Function: domain_is_initialized

    Method will return a boolean value representing the state of domain
    initialization

    Returns: Boolean
    """

    def domain_is_initialized(self, domain_id: int) -> bool:
        _cfms_domain_is_initialized = self.cFMS.cFMS_domain_is_initialized

        domain_id_c, domain_id_t = setscalar_Cint32(domain_id)

        _cfms_domain_is_initialized.argtypes = [domain_id_t]
        _cfms_domain_is_initialized.restype = ctypes.c_bool

        return _cfms_domain_is_initialized(domain_id_c)

    """
    Subroutine: get_compute_domain

    Arguments passed to function will generate and update data for a
    compute domain

    Returns: In the Fortran source, when passed in xbegin, xend, ybegin, yend,
    xsize, xmax_size, ysize, ymax_size, x_is_global, y_is_global, and
    tile_count are updated. To obtain access to the updated value the flag
    associated with the desired variable should be set to true.
    This method will return a dictionary containing values for those arguments
    which were passed, overwriting the passed value.
    """

    def get_compute_domain(
        self,
        domain_id: int,
        position: int = None,
        tile_count: int = None,
        whalo: int = None,
        shalo: int = None,
    ) -> dict:

        _cfms_get_compute_domain = self.cFMS.cFMS_get_compute_domain

        default_i = 0
        default_b = False

        domain_id_t = ctypes.c_int
        xbegin_t = ctypes.c_int
        xend_t = ctypes.c_int
        ybegin_t = ctypes.c_int
        yend_t = ctypes.c_int
        xsize_t = ctypes.c_int
        xmax_size_t = ctypes.c_int
        ysize_t = ctypes.c_int
        ymax_size_t = ctypes.c_int
        x_is_global_t = ctypes.c_bool
        y_is_global_t = ctypes.c_bool
        tile_count_t = ctypes.c_int
        position_t = ctypes.c_int
        whalo_t = ctypes.c_int
        shalo_t = ctypes.c_int

        xbegin_c = xbegin_t(default_i)
        xend_c = xend_t(default_i)
        ybegin_c = ybegin_t(default_i)
        yend_c = yend_t(default_i)
        xsize_c = xsize_t(default_i)
        xmax_size_c = xmax_size_t(default_i)
        ysize_c = ysize_t(default_i)
        ymax_size_c = ymax_size_t(default_i)
        x_is_global_c = x_is_global_t(default_b)
        y_is_global_c = y_is_global_t(default_b)
        domain_id_c = domain_id_t(domain_id) if domain_id is not None else None
        tile_count_c = tile_count_t(tile_count) if tile_count is not None else None
        position_c = position_t(position) if position is not None else None
        whalo_c = whalo_t(whalo) if whalo is not None else None
        shalo_c = shalo_t(shalo) if shalo is not None else None

        _cfms_get_compute_domain.argtypes = [
            ctypes.POINTER(domain_id_t),
            ctypes.POINTER(xbegin_t),
            ctypes.POINTER(xend_t),
            ctypes.POINTER(ybegin_t),
            ctypes.POINTER(yend_t),
            ctypes.POINTER(xsize_t),
            ctypes.POINTER(xmax_size_t),
            ctypes.POINTER(ysize_t),
            ctypes.POINTER(ymax_size_t),
            ctypes.POINTER(x_is_global_t),
            ctypes.POINTER(y_is_global_t),
            ctypes.POINTER(tile_count_t),
            ctypes.POINTER(position_t),
            ctypes.POINTER(whalo_t),
            ctypes.POINTER(shalo_t),
        ]

        _cfms_get_compute_domain.restype = None

        _cfms_get_compute_domain(
            domain_id_c,
            xbegin_c,
            xend_c,
            ybegin_c,
            yend_c,
            xsize_c,
            xmax_size_c,
            ysize_c,
            ymax_size_c,
            x_is_global_c,
            y_is_global_c,
            tile_count_c,
            position_c,
            whalo_c,
            shalo_c,
        )

        return dict(
            domain_id=domain_id_c.value,
            xbegin=xbegin_c.value,
            ybegin=ybegin_c.value,
            xend=xend_c.value,
            yend=yend_c.value,
            xsize=xsize_c.value,
            ysize=ysize_c.value,
            xmax_size=xmax_size_c.value,
            ymax_size=ymax_size_c.value,
            x_is_global=x_is_global_c.value,
            y_is_global=y_is_global_c.value,
        )

    """
    Subroutine: get_data_domain

    Arguments passed to function will generate and update data for a
    data domain

    Returns: In the Fortran source, when passed in xbegin, xend, ybegin, yend,
    xsize, xmax_size, ysize, ymax_size, x_is_global, y_is_global, and
    tile_count are updated. To obtain access to the updated value the flag
    associated with the desired variable should be set to true.
    This method will return a dictionary containing values for those arguments
    which were passed, overwriting the passed value.
    """

    def get_data_domain(
        self,
        domain_id: int,
        position: int = None,
        tile_count: int = None,
        whalo: int = None,
        shalo: int = None,
    ) -> dict:
        _cfms_get_data_domain = self.cFMS.cFMS_get_data_domain

        default_i = 0
        default_b = False

        domain_id_t = ctypes.c_int
        xbegin_t = ctypes.c_int
        xend_t = ctypes.c_int
        ybegin_t = ctypes.c_int
        yend_t = ctypes.c_int
        xsize_t = ctypes.c_int
        xmax_size_t = ctypes.c_int
        ysize_t = ctypes.c_int
        ymax_size_t = ctypes.c_int
        x_is_global_t = ctypes.c_bool
        y_is_global_t = ctypes.c_bool
        tile_count_t = ctypes.c_int
        position_t = ctypes.c_int
        whalo_t = ctypes.c_int
        shalo_t = ctypes.c_int

        xbegin_c = xbegin_t(default_i)
        xend_c = xend_t(default_i)
        ybegin_c = ybegin_t(default_i)
        yend_c = yend_t(default_i)
        xsize_c = xsize_t(default_i)
        xmax_size_c = xmax_size_t(default_i)
        ysize_c = ysize_t(default_i)
        ymax_size_c = ymax_size_t(default_i)
        x_is_global_c = x_is_global_t(default_b)
        y_is_global_c = y_is_global_t(default_b)
        domain_id_c = domain_id_t(domain_id) if domain_id is not None else None
        tile_count_c = tile_count_t(tile_count) if tile_count is not None else None
        position_c = position_t(position) if position is not None else None
        whalo_c = whalo_t(whalo) if whalo is not None else None
        shalo_c = shalo_t(shalo) if shalo is not None else None

        _cfms_get_data_domain.argtypes = [
            ctypes.POINTER(domain_id_t),
            ctypes.POINTER(xbegin_t),
            ctypes.POINTER(xend_t),
            ctypes.POINTER(ybegin_t),
            ctypes.POINTER(yend_t),
            ctypes.POINTER(xsize_t),
            ctypes.POINTER(xmax_size_t),
            ctypes.POINTER(ysize_t),
            ctypes.POINTER(ymax_size_t),
            ctypes.POINTER(x_is_global_t),
            ctypes.POINTER(y_is_global_t),
            ctypes.POINTER(tile_count_t),
            ctypes.POINTER(position_t),
            ctypes.POINTER(whalo_t),
            ctypes.POINTER(shalo_t),
        ]

        _cfms_get_data_domain.restype = None

        _cfms_get_data_domain(
            domain_id_c,
            xbegin_c,
            xend_c,
            ybegin_c,
            yend_c,
            xsize_c,
            xmax_size_c,
            ysize_c,
            ymax_size_c,
            x_is_global_c,
            y_is_global_c,
            tile_count_c,
            position_c,
            whalo_c,
            shalo_c,
        )

        return dict(
            domain_id=domain_id_c.value,
            xbegin=xbegin_c.value,
            ybegin=ybegin_c.value,
            xend=xend_c.value,
            yend=yend_c.value,
            xsize=xsize_c.value,
            ysize=ysize_c.value,
            xmax_size=xmax_size_c.value,
            ymax_size=ymax_size_c.value,
            x_is_global=x_is_global_c.value,
            y_is_global=y_is_global_c.value,
        )

    """
    Subroutine: get_domain_name

    The passed domain_name string object will be updated with the domain name
    respective to the arguments passed

    Returns: In Fortran source, domain_name is updated. The Python object passed as
    the argument for domain_name should be set to the result of the call to update
    its value as well.
    """

    def get_domain_name(self, domain_id: int) -> str:
        _cfms_get_domain_name = self.cFMS.cFMS_get_domain_name

        domain_name = ""

        domain_name_c, domain_name_t = set_Cchar(domain_name)
        domain_id_c, domain_id_t = setscalar_Cint32(domain_id)

        _cfms_get_domain_name.argtypes = [domain_name_t, domain_id_t]
        _cfms_get_domain_name.restype = None

        _cfms_get_domain_name(domain_name_c, domain_id_c)

        return domain_name_c.value.decode("utf-8")

    """
    Subroutine: get_layout

    Updates layout NumPy array to contain layout data

    Returns: NDArray with layout info
    """

    def get_layout(self, domain_id: int) -> list[int]:

        layout = np.empty(shape=2, dtype=np.int32, order="C")

        _cfms_get_layout = self.cFMS.cFMS_get_layout

        layout_p, layout_t = setarray_Cint32(layout)
        domain_id_c, domain_id_t = setscalar_Cint32(domain_id)

        _cfms_get_layout.argtypes = [layout_t, domain_id_t]
        _cfms_get_layout.restype = None

        _cfms_get_layout(layout_p, domain_id_c)

        return layout_p.tolist()

    """
    Subroutine: get_domain_pelist

    Returns: NDArray containing pelist
    """

    def get_domain_pelist(self, domain_id: int) -> list[int]:

        npes = ctypes.c_int.in_dll(self.cFMS, "cFMS_pelist_npes")
        pelist = np.empty(shape=npes.value, dtype=np.int32, order="C")

        _cfms_get_domain_pelist = self.cFMS.cFMS_get_domain_pelist

        pelist_p, pelist_t = setarray_Cint32(pelist)
        domain_id_c, domain_id_t = setscalar_Cint32(domain_id)

        _cfms_get_domain_pelist.argtypes = [pelist_t, domain_id_t]
        _cfms_get_domain_pelist.restype = None

        _cfms_get_domain_pelist(pelist_p, domain_id_c)

        return pelist_p.tolist()

    """
    Subroutine: set_compute_domain

    Passed arguments will set data for compute domain

    Returns: In Fortran source, xbegin, xend, ybegin, yend, xsize,
    ysize, x_is_global, y_is_global, and tile_count are updated.
    Python objects passed as arguments should be set to the result
    of the call.
    Returns: In the Fortran source, when passed in xbegin, xend, ybegin, yend,
    xsize, ysize, x_is_global, y_is_global, and tile_count are updated. To
    obtain access to their values, an integer Python object should be passed
    in as an argument for the desired variable.
    This method will return a dictionary containing values for those arguments
    which were passed, overwriting the passed value.
    """

    def set_compute_domain(
        self,
        domain_id: int,
        xbegin: int = None,
        xend: int = None,
        ybegin: int = None,
        yend: int = None,
        xsize: int = None,
        ysize: int = None,
        x_is_global: bool = None,
        y_is_global: bool = None,
        tile_count: int = None,
        whalo: int = None,
        shalo: int = None,
    ):
        _cfms_set_compute_domain = self.cFMS.cFMS_set_compute_domain

        domain_id_c, domain_id_t = setscalar_Cint32(domain_id)
        xbegin_c, xbegin_t = setscalar_Cint32(xbegin)
        xend_c, xend_t = setscalar_Cint32(xend)
        ybegin_c, ybegin_t = setscalar_Cint32(ybegin)
        yend_c, yend_t = setscalar_Cint32(yend)
        xsize_c, xsize_t = setscalar_Cint32(xsize)
        ysize_c, ysize_t = setscalar_Cint32(ysize)
        x_is_global_c, x_is_global_t = setscalar_Cbool(x_is_global)
        y_is_global_c, y_is_global_t = setscalar_Cbool(y_is_global)
        tile_count_c, tile_count_t = setscalar_Cint32(tile_count)
        whalo_c, whalo_t = setscalar_Cint32(whalo)
        shalo_c, shalo_t = setscalar_Cint32(shalo)

        _cfms_set_compute_domain.argtypes = [
            domain_id_t,
            xbegin_t,
            xend_t,
            ybegin_t,
            yend_t,
            xsize_t,
            ysize_t,
            x_is_global_t,
            y_is_global_t,
            tile_count_t,
            whalo_t,
            shalo_t,
        ]
        _cfms_set_compute_domain.restype = None

        _cfms_set_compute_domain(
            domain_id_c,
            xbegin_c,
            xend_c,
            ybegin_c,
            yend_c,
            xsize_c,
            ysize_c,
            x_is_global_c,
            y_is_global_c,
            tile_count_c,
            whalo_c,
            shalo_c,
        )

    """
    Subroutine: set_current_domain

    Sets domain to current_domain, updating the id of the current_domain
    to domain_id
    """

    def set_current_domain(self, domain_id: int):
        _cfms_set_current_domain = self.cFMS.cFMS_set_current_domain

        domain_id_c, domain_id_t = setscalar_Cint32(domain_id)

        _cfms_set_current_domain.argtypes = [domain_id_t]
        _cfms_set_current_domain.restype = None

        _cfms_set_current_domain(domain_id_c)

    """
    Subroutine: set_current_nest_domain

    Sets nest_domain to current_nest_domain, and updates id of current_nest_domain
    to nest_domain_id
    """

    def set_current_nest_domain(self, nest_domain_id: int):
        _cfms_set_current_nest_domain = self.cFMS.cFMS_set_current_nest_domain

        nest_domain_id_c, nest_domain_id_t = setscalar_Cint32(nest_domain_id)

        _cfms_set_current_nest_domain.argtypes = [nest_domain_id_t]
        _cfms_set_current_nest_domain.restype = None

        _cfms_set_current_nest_domain(nest_domain_id_c)

    """
    Subroutine: set_data_domain

    Passed arguments will set data for data domain

    Returns: In the Fortran source, when passed in xbegin, xend, ybegin, yend,
    xsize, ysize, x_is_global, y_is_global, and tile_count are updated. To
    obtain access to their values, an integer Python object should be passed
    in as an argument for the desired variable.
    This method will return a dictionary containing values for those arguments
    which were passed, overwriting the passed value.
    """

    def set_data_domain(
        self,
        domain_id: int,
        xbegin: int = None,
        xend: int = None,
        ybegin: int = None,
        yend: int = None,
        xsize: int = None,
        ysize: int = None,
        x_is_global: bool = None,
        y_is_global: bool = None,
        tile_count: int = None,
        whalo: int = None,
        shalo: int = None,
    ):
        _cfms_set_data_domain = self.cFMS.cFMS_set_data_domain

        domain_id_c, domain_id_t = setscalar_Cint32(domain_id)
        xbegin_c, xbegin_t = setscalar_Cint32(xbegin)
        xend_c, xend_t = setscalar_Cint32(xend)
        ybegin_c, ybegin_t = setscalar_Cint32(ybegin)
        yend_c, yend_t = setscalar_Cint32(yend)
        xsize_c, xsize_t = setscalar_Cint32(xsize)
        ysize_c, ysize_t = setscalar_Cint32(ysize)
        x_is_global_c, x_is_global_t = setscalar_Cbool(x_is_global)
        y_is_global_c, y_is_global_t = setscalar_Cbool(y_is_global)
        tile_count_c, tile_count_t = setscalar_Cint32(tile_count)
        whalo_c, whalo_t = setscalar_Cint32(whalo)
        shalo_c, shalo_t = setscalar_Cint32(shalo)

        _cfms_set_data_domain.argtypes = [
            domain_id_t,
            xbegin_t,
            xend_t,
            ybegin_t,
            yend_t,
            xsize_t,
            ysize_t,
            x_is_global_t,
            y_is_global_t,
            tile_count_t,
            whalo_t,
            shalo_t,
        ]
        _cfms_set_data_domain.restype = None

        _cfms_set_data_domain(
            domain_id_c,
            xbegin_c,
            xend_c,
            ybegin_c,
            yend_c,
            xsize_c,
            ysize_c,
            x_is_global_c,
            y_is_global_c,
            tile_count_c,
            whalo_c,
            shalo_c,
        )

    """
    Subroutine: set_global_domain

    Passed arguments will set data for data domain

    Returns: In Fortran source, xbegin, xend, ybegin, yend, xsize,
    ysize, and tile_count are updated.
    Python objects passed as arguments should be set to the result
    of the call.
    Returns: In the Fortran source, when passed in xbegin, xend, ybegin, yend,
    xsize, ysize, and tile_count are updated. To obtain access to their values,
    an integer Python object should be passed in as an argument for the
    desired variable.
    This method will return a dictionary containing values for those arguments
    which were passed, overwriting the passed value.
    """

    def set_global_domain(
        self,
        domain_id: int,
        xbegin: int = None,
        xend: int = None,
        ybegin: int = None,
        yend: int = None,
        xsize: int = None,
        ysize: int = None,
        tile_count: int = None,
        whalo: int = None,
        shalo: int = None,
    ):
        _cfms_set_global_domain = self.cFMS.cFMS_set_global_domain

        domain_id_c, domain_id_t = setscalar_Cint32(domain_id)
        xbegin_c, xbegin_t = setscalar_Cint32(xbegin)
        xend_c, xend_t = setscalar_Cint32(xend)
        ybegin_c, ybegin_t = setscalar_Cint32(ybegin)
        yend_c, yend_t = setscalar_Cint32(yend)
        xsize_c, xsize_t = setscalar_Cint32(xsize)
        ysize_c, ysize_t = setscalar_Cint32(ysize)
        tile_count_c, tile_count_t = setscalar_Cint32(tile_count)
        whalo_c, whalo_t = setscalar_Cint32(whalo)
        shalo_c, shalo_t = setscalar_Cint32(shalo)

        _cfms_set_global_domain.argtypes = [
            domain_id_t,
            xbegin_t,
            xend_t,
            ybegin_t,
            yend_t,
            xsize_t,
            ysize_t,
            tile_count_t,
            whalo_t,
            shalo_t,
        ]
        _cfms_set_global_domain.restype = None

        _cfms_set_global_domain(
            domain_id_c,
            xbegin_c,
            xend_c,
            ybegin_c,
            yend_c,
            xsize_c,
            ysize_c,
            tile_count_c,
            whalo_c,
            shalo_c,
        )

    def update_domains(
        self,
        field: NDArray,
        domain_id: int = None,
        flags: int = None,
        complete: bool = None,
        position: int = None,
        whalo: int = None,
        ehalo: int = None,
        shalo: int = None,
        nhalo: int = None,
        name: str = None,
        tile_count: int = None,
    ):
        if name is not None:
            name = name[:64]

        if field.ndim == 2:
            if field.dtype == np.float64:
                _cfms_update_domains = self.cFMS.cFMS_update_domains_double_2d
                field_p, field_t = setarray_Cdouble(field)
            elif field.dtype == np.float32:
                _cfms_update_domains = self.cFMS.cFMS_update_domains_float_2d
                field_p, field_t = setarray_Cfloat(field)
            elif field.dtype == np.int32:
                _cfms_update_domains = self.cFMS.cFMS_update_domains_int_2d
                field_p, field_t = setarray_Cfloat(field)
            else:
                raise RuntimeError(
                    f"udate_domains input field datatype {field.dtype} unsupported"
                )
        elif field.ndim == 3:
            if field.dtype == np.float64:
                _cfms_update_domains = self.cFMS.cFMS_update_domains_double_3d
                field_p, field_t = setarray_Cdouble(field)
            elif field.dtype == np.float32:
                _cfms_update_domains = self.cFMS.cFMS_update_domains_float_3d
                field_p, field_t = setarray_Cfloat(field)
            elif field.dtype == np.int32:
                _cfms_update_domains = self.cFMS.cFMS_update_domains_int_3d
                field_p, field_t = setarray_Cfloat(field)
            else:
                raise RuntimeError(
                    f"udate_domains input field datatype {field.dtype} unsupported"
                )
        elif field.ndim == 4:
            if field.dtype == np.float64:
                _cfms_update_domains = self.cFMS.cFMS_update_domains_double_4d
                field_p, field_t = setarray_Cdouble(field)
            elif field.dtype == np.float32:
                _cfms_update_domains = self.cFMS.cFMS_update_domains_float_4d
                field_p, field_t = setarray_Cfloat(field)
            elif field.dtype == np.int32:
                _cfms_update_domains = self.cFMS.cFMS_update_domains_int_4d
                field_p, field_t = setarray_Cfloat(field)
            else:
                raise RuntimeError(
                    f"udate_domains input field datatype {field.dtype} unsupported"
                )
        elif field.ndim == 5:
            if field.dtype == np.float64:
                _cfms_update_domains = self.cFMS.cFMS_update_domains_double_5d
                field_p, field_t = setarray_Cdouble(field)
            elif field.dtype == np.float32:
                _cfms_update_domains = self.cFMS.cFMS_update_domains_float_5d
                field_p, field_t = setarray_Cfloat(field)
            elif field.dtype == np.int32:
                _cfms_update_domains = self.cFMS.cFMS_update_domains_int_5d
                field_p, field_t = setarray_Cfloat(field)
            else:
                raise RuntimeError(
                    f"udate_domains input field datatype {field.dtype} unsupported"
                )
        else:
            raise RuntimeError(
                f"update_domains field dimension {field.ndim}d unsupported"
            )

        field_shape = np.array(field.shape, dtype=np.int32)
        field_shape_p, field_shape_t = setarray_Cint32(field_shape)
        domain_id_c, domain_id_t = setscalar_Cint32(domain_id)
        flags_c, flags_t = setscalar_Cint32(flags)
        complete_c, complete_t = setscalar_Cbool(complete)
        position_c, position_t = setscalar_Cint32(position)
        whalo_c, whalo_t = setscalar_Cint32(whalo)
        ehalo_c, ehalo_t = setscalar_Cint32(ehalo)
        shalo_c, shalo_t = setscalar_Cint32(shalo)
        nhalo_c, nhalo_t = setscalar_Cint32(nhalo)
        name_c, name_t = set_Cchar(name)
        tile_count_c, tile_count_t = setscalar_Cint32(tile_count)

        _cfms_update_domains.argtypes = [
            field_shape_t,
            field_t,
            domain_id_t,
            flags_t,
            complete_t,
            position_t,
            whalo_t,
            ehalo_t,
            shalo_t,
            nhalo_t,
            name_t,
            tile_count_t,
        ]
        _cfms_update_domains.restype = None

        _cfms_update_domains(
            field_shape_p,
            field_p,
            domain_id_c,
            flags_c,
            complete_c,
            position_c,
            whalo_c,
            ehalo_c,
            shalo_c,
            nhalo_c,
            name_c,
            tile_count_c,
        )
