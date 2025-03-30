import ctypes
from typing import Optional

import numpy as np
from numpy.typing import NDArray

from ..pyfms_utils.data_handling import (
    set_Cchar,
    set_multipointer,
    setarray_Cdouble,
    setarray_Cfloat,
    setarray_Cint32,
    setscalar_Cbool,
    setscalar_Cint32,
)


class pyDomainData:
    def __init__(
        self,
        xbegin=0,
        xend=0,
        ybegin=0,
        yend=0,
        xsize=0,
        xmax_size=0,
        ysize=0,
        ymax_size=0,
        x_is_global=False,
        y_is_global=False,
        tile_count=0,
    ):
        self.xbegin = ctypes.c_int(xbegin)
        self.xend = ctypes.c_int(xend)
        self.ybegin = ctypes.c_int(ybegin)
        self.yend = ctypes.c_int(yend)
        self.xsize = ctypes.c_int(xsize)
        self.xmax_size = ctypes.c_int(xmax_size)
        self.ysize = ctypes.c_int(ysize)
        self.ymax_size = ctypes.c_int(ymax_size)
        self.x_is_global = ctypes.c_bool(x_is_global)
        self.y_is_global = ctypes.c_bool(y_is_global)
        self.tile_count = ctypes.c_int(tile_count)


class pyFMS_mpp_domains:
    def __init__(self, cFMS: ctypes.CDLL = None):
        self.cFMS = cFMS

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
        global_indices: NDArray,
        layout: NDArray,
        domain_id: Optional[int] = None,
        pelist: Optional[NDArray] = None,
        xflags: Optional[int] = None,
        yflags: Optional[int] = None,
        xhalo: Optional[int] = None,
        yhalo: Optional[int] = None,
        xextent: Optional[NDArray] = None,
        yextent: Optional[NDArray] = None,
        maskmap: Optional[NDArray[np.bool_]] = None,
        name: Optional[str] = None,
        symmetry: Optional[bool] = None,
        memory_size: Optional[NDArray] = None,
        whalo: Optional[int] = None,
        ehalo: Optional[int] = None,
        shalo: Optional[int] = None,
        nhalo: Optional[int] = None,
        is_mosaic: Optional[bool] = None,
        tile_count: Optional[int] = None,
        tile_id: Optional[int] = None,
        complete: Optional[bool] = None,
        x_cyclic_offset: Optional[int] = None,
        y_cyclic_offset: Optional[int] = None,
    ):

        _cfms_define_domains = self.cFMS.cFMS_define_domains

        global_indices_p, global_indices_t = setarray_Cint32(global_indices)
        layout_p, layout_t = setarray_Cint32(layout)
        domain_id_c, domain_id_t = setscalar_Cint32(domain_id)
        pelist_p, pelist_t = setarray_Cint32(pelist)
        xflags_c, xflags_t = setscalar_Cint32(xflags)
        yflags_c, yflags_t = setscalar_Cint32(yflags)
        xhalo_c, xhalo_t = setscalar_Cint32(xhalo)
        yhalo_c, yhalo_t = setscalar_Cint32(yhalo)
        xextent_p, xextent_t = setarray_Cint32(xextent)
        yextent_p, yextent_t = setarray_Cint32(yextent)
        maskmap_p, maskmap_t = set_multipointer(arg=maskmap, num_ptr=2)
        name_c, name_t = set_Cchar(name)
        symmetry_c, symmetry_t = setscalar_Cbool(symmetry)
        memory_size_p, memory_size_t = setarray_Cint32(memory_size)
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
            domain_id_t,
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

        _cfms_define_domains.restype = None

        _cfms_define_domains(
            global_indices_p,
            layout_p,
            domain_id_c,
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

    """
    Subroutine: define_io_domains

    Arguments of this method will define data for I/O domain

    Returns: No return
    """

    def define_io_domain(self, io_layout: NDArray, domain_id: Optional[int] = None):
        _cfms_define_io_domain = self.cFMS.cFMS_define_io_domain

        io_layout_p, io_layout_t = setarray_Cint32(io_layout)
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
        global_indices: NDArray,
        ndivs: int,
    ) -> NDArray:

        layout = np.empty(shape=2, dtype=np.int32, order="C")

        _cfms_define_layout = self.cFMS.cFMS_define_layout

        global_indices_p, global_indices_t = setarray_Cint32(global_indices)
        ndivs_c, ndivs_t = setscalar_Cint32(ndivs)
        layout_p, layout_t = setarray_Cint32(layout)

        _cfms_define_layout.argtypes = [global_indices_t, ndivs_t, layout_t]
        _cfms_define_layout.restype = None

        _cfms_define_layout(global_indices_p, ndivs_c, layout_p)

        return layout

    """
    Subroutine: define_nest_domains

    Arguments passed to this method will define data for nest domains

    Returns: No return
    """

    def define_nest_domains(
        self,
        num_nest: int,
        ntiles: int,
        nest_level: NDArray,
        tile_fine: NDArray,
        tile_coarse: NDArray,
        istart_coarse: NDArray,
        icount_coarse: NDArray,
        jstart_coarse: NDArray,
        jcount_coarse: NDArray,
        npes_nest_tile: NDArray,
        x_refine: NDArray,
        y_refine: NDArray,
        nest_domain_id: Optional[int] = None,
        domain_id: Optional[int] = None,
        extra_halo: Optional[int] = None,
        name: Optional[str] = None,
    ):
        _cfms_define_nest_domain = self.cFMS.cFMS_define_nest_domains

        num_nest_p, num_nest_t = setscalar_Cint32(num_nest)
        ntiles_c, ntiles_t = setscalar_Cint32(ntiles)
        nest_level_p, nest_level_t = setarray_Cint32(nest_level)
        tile_fine_p, tile_fine_t = setarray_Cint32(tile_fine)
        tile_coarse_p, tile_coarse_t = setarray_Cint32(tile_coarse)
        istart_coarse_p, istart_coarse_t = setarray_Cint32(istart_coarse)
        icount_coarse_p, icount_coarse_t = setarray_Cint32(icount_coarse)
        jstart_coarse_p, jstart_coarse_t = setarray_Cint32(jstart_coarse)
        jcount_coarse_p, jcount_coarse_t = setarray_Cint32(jcount_coarse)
        npes_nest_tile_p, npes_nest_tile_t = setarray_Cint32(npes_nest_tile)
        x_refine_p, x_refine_t = setarray_Cint32(x_refine)
        y_refine_p, y_refine_t = setarray_Cint32(y_refine)
        nest_domain_id_c, nest_domain_id_t = setscalar_Cint32(nest_domain_id)
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
            nest_domain_id_t,
            domain_id_t,
            extra_halo_t,
            name_t,
        ]
        _cfms_define_nest_domain.restype = None

        _cfms_define_nest_domain(
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
            nest_domain_id_c,
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

    def domain_is_initialized(self, domain_id: Optional[int] = None) -> bool:
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
        domain_data: pyDomainData,
        domain_id: Optional[int] = None,
        position: Optional[int] = None,
        whalo: Optional[int] = None,
        shalo: Optional[int] = None,
    ):

        _cfms_get_compute_domain = self.cFMS.cFMS_get_compute_domain

        domain_id_c, domain_id_t = setscalar_Cint32(domain_id)
        xbegin_c, xbegin_t = setscalar_Cint32(domain_data.xbegin)
        xend_c, xend_t = setscalar_Cint32(domain_data.xend)
        ybegin_c, ybegin_t = setscalar_Cint32(domain_data.ybegin)
        yend_c, yend_t = setscalar_Cint32(domain_data.yend)
        xsize_c, xsize_t = setscalar_Cint32(domain_data.xsize)
        xmax_size_c, xmax_size_t = setscalar_Cint32(domain_data.xmax_size)
        ysize_c, ysize_t = setscalar_Cint32(domain_data.ysize)
        ymax_size_c, ymax_size_t = setscalar_Cint32(domain_data.ymax_size)
        x_is_global_c, x_is_global_t = setscalar_Cbool(domain_data.x_is_global)
        y_is_global_c, y_is_global_t = setscalar_Cbool(domain_data.y_is_global)
        tile_count_c, tile_count_t = setscalar_Cint32(domain_data.tile_count)
        position_c, position_t = setscalar_Cint32(position)
        whalo_c, whalo_t = setscalar_Cint32(whalo)
        shalo_c, shalo_t = setscalar_Cint32(shalo)

        _cfms_get_compute_domain.argtypes = [
            domain_id_t,
            xbegin_t,
            xend_t,
            ybegin_t,
            yend_t,
            xsize_t,
            xmax_size_t,
            ysize_t,
            ymax_size_t,
            x_is_global_t,
            y_is_global_t,
            tile_count_t,
            position_t,
            whalo_t,
            shalo_t,
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

    def get_compute_domain2(
        self,
        domain_id: int | None = None,
        position: int | None = None,
        tile_count: int | None = None,
        whalo: int | None = None,
        shalo: int | None = None,
    ):

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
        position_c = position_t(position) if tile_count is not None else None
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
        domain_data: pyDomainData,
        domain_id: Optional[int] = None,
        position: Optional[int] = None,
        whalo: Optional[int] = None,
        shalo: Optional[int] = None,
    ):
        _cfms_get_data_domain = self.cFMS.cFMS_get_data_domain

        domain_id_c, domain_id_t = setscalar_Cint32(domain_id)
        xbegin_c, xbegin_t = setscalar_Cint32(domain_data.xbegin)
        xend_c, xend_t = setscalar_Cint32(domain_data.xend)
        ybegin_c, ybegin_t = setscalar_Cint32(domain_data.ybegin)
        yend_c, yend_t = setscalar_Cint32(domain_data.yend)
        xsize_c, xsize_t = setscalar_Cint32(domain_data.xsize)
        xmax_size_c, xmax_size_t = setscalar_Cint32(domain_data.xmax_size)
        ysize_c, ysize_t = setscalar_Cint32(domain_data.ysize)
        ymax_size_c, ymax_size_t = setscalar_Cint32(domain_data.ymax_size)
        x_is_global_c, x_is_global_t = setscalar_Cbool(domain_data.x_is_global)
        y_is_global_c, y_is_global_t = setscalar_Cbool(domain_data.y_is_global)
        tile_count_c, tile_count_t = setscalar_Cint32(domain_data.tile_count)
        position_c, position_t = setscalar_Cint32(position)
        whalo_c, whalo_t = setscalar_Cint32(whalo)
        shalo_c, shalo_t = setscalar_Cint32(shalo)

        _cfms_get_data_domain.argtypes = [
            domain_id_t,
            xbegin_t,
            xend_t,
            ybegin_t,
            yend_t,
            xsize_t,
            xmax_size_t,
            ysize_t,
            ymax_size_t,
            x_is_global_t,
            y_is_global_t,
            tile_count_t,
            position_t,
            whalo_t,
            shalo_t,
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

    """
    Subroutine: get_domain_name

    The passed domain_name string object will be updated with the domain name
    respective to the arguments passed

    Returns: In Fortran source, domain_name is updated. The Python object passed as
    the argument for domain_name should be set to the result of the call to update
    its value as well.
    """

    def get_domain_name(self, domain_id: Optional[int] = None) -> str:
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

    def get_layout(self, domain_id: Optional[int] = None) -> NDArray:

        layout = np.empty(shape=2, dtype=np.int32, order="C")

        _cfms_get_layout = self.cFMS.cFMS_get_layout

        layout_p, layout_t = setarray_Cint32(layout)
        domain_id_c, domain_id_t = setscalar_Cint32(domain_id)

        _cfms_get_layout.argtypes = [layout_t, domain_id_t]
        _cfms_get_layout.restype = None

        _cfms_get_layout(layout_p, domain_id_c)

        return layout

    """
    Subroutine: get_domain_pelist

    Returns: NDArray containing pelist
    """

    def get_domain_pelist(self, domain_id: Optional[int]) -> NDArray:

        npes = ctypes.c_int.in_dll(self.cFMS, "cFMS_pelist_npes")
        pelist = np.empty(shape=npes.value, dtype=np.int32, order="C")

        _cfms_get_domain_pelist = self.cFMS.cFMS_get_domain_pelist

        pelist_p, pelist_t = setarray_Cint32(pelist)
        domain_id_c, domain_id_t = setscalar_Cint32(domain_id)

        _cfms_get_domain_pelist.argtypes = [pelist_t, domain_id_t]
        _cfms_get_domain_pelist.restype = None

        _cfms_get_domain_pelist(pelist_p, domain_id_c)

        return pelist

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
        xbegin: Optional[int] = None,
        xend: Optional[int] = None,
        ybegin: Optional[int] = None,
        yend: Optional[int] = None,
        xsize: Optional[int] = None,
        ysize: Optional[int] = None,
        x_is_global: Optional[bool] = None,
        y_is_global: Optional[bool] = None,
        tile_count: Optional[int] = None,
        domain_id: Optional[int] = None,
        whalo: Optional[int] = None,
        shalo: Optional[int] = None,
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

    def set_current_domain(self, domain_id: Optional[int] = None):
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

    def set_current_nest_domain(self, nest_domain_id: Optional[int] = None):
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
        xbegin: Optional[int] = None,
        xend: Optional[int] = None,
        ybegin: Optional[int] = None,
        yend: Optional[int] = None,
        xsize: Optional[int] = None,
        ysize: Optional[int] = None,
        x_is_global: Optional[bool] = None,
        y_is_global: Optional[bool] = None,
        tile_count: Optional[int] = None,
        domain_id: Optional[int] = None,
        whalo: Optional[int] = None,
        shalo: Optional[int] = None,
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
        xbegin: Optional[int] = None,
        xend: Optional[int] = None,
        ybegin: Optional[int] = None,
        yend: Optional[int] = None,
        xsize: Optional[int] = None,
        ysize: Optional[int] = None,
        tile_count: Optional[int] = None,
        domain_id: Optional[int] = None,
        whalo: Optional[int] = None,
        shalo: Optional[int] = None,
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

    def update_domains_double_2d(
        self,
        field_shape: NDArray,
        field: NDArray,
        domain_id: Optional[int],
        flags: Optional[int],
        complete: Optional[bool],
        position: Optional[int],
        whalo: Optional[int],
        ehalo: Optional[int],
        shalo: Optional[int],
        nhalo: Optional[int],
        name: Optional[str],
        tile_count: Optional[int],
    ):
        _cfms_update_domains_double_2d = self.clibFMS.cFMS_update_domains_double_2d

        field_shape_p, field_shape_t = setarray_Cint32(field_shape)
        field_p, field_t = setarray_Cdouble(field)
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

        _cfms_update_domains_double_2d.argtypes = [
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
        _cfms_update_domains_double_2d.restype = None

        _cfms_update_domains_double_2d(
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

    def update_domains_double_3d(
        self,
        field_shape: NDArray,
        field: NDArray,
        domain_id: Optional[int],
        flags: Optional[int],
        complete: Optional[bool],
        position: Optional[int],
        whalo: Optional[int],
        ehalo: Optional[int],
        shalo: Optional[int],
        nhalo: Optional[int],
        name: Optional[str],
        tile_count: Optional[int],
    ):
        _cfms_update_domains_double_3d = self.clibFMS.cFMS_update_domains_double_3d

        field_shape_p, field_shape_t = setarray_Cint32(field_shape)
        field_p, field_t = setarray_Cdouble(field)
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

        _cfms_update_domains_double_3d.argtypes = [
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
        _cfms_update_domains_double_3d.restype = None

        _cfms_update_domains_double_3d(
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

    def update_domains_double_4d(
        self,
        field_shape: NDArray,
        field: NDArray,
        domain_id: Optional[int],
        flags: Optional[int],
        complete: Optional[bool],
        position: Optional[int],
        whalo: Optional[int],
        ehalo: Optional[int],
        shalo: Optional[int],
        nhalo: Optional[int],
        name: Optional[str],
        tile_count: Optional[int],
    ):
        _cfms_update_domains_double_4d = self.clibFMS.cFMS_update_domains_double_4d

        field_shape_p, field_shape_t = setarray_Cint32(field_shape)
        field_p, field_t = setarray_Cdouble(field)
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

        _cfms_update_domains_double_4d.argtypes = [
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
        _cfms_update_domains_double_4d.restype = None

        _cfms_update_domains_double_4d(
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

    def update_domains_double_5d(
        self,
        field_shape: NDArray,
        field: NDArray,
        domain_id: Optional[int],
        flags: Optional[int],
        complete: Optional[bool],
        position: Optional[int],
        whalo: Optional[int],
        ehalo: Optional[int],
        shalo: Optional[int],
        nhalo: Optional[int],
        name: Optional[str],
        tile_count: Optional[int],
    ):
        _cfms_update_domains_double_5d = self.clibFMS.cFMS_update_domains_double_5d

        field_shape_p, field_shape_t = setarray_Cint32(field_shape)
        field_p, field_t = setarray_Cdouble(field)
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

        _cfms_update_domains_double_5d.argtypes = [
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
        _cfms_update_domains_double_5d.restype = None

        _cfms_update_domains_double_5d(
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

    def update_domains_float_2d(
        self,
        field_shape: NDArray,
        field: NDArray,
        domain_id: Optional[int],
        flags: Optional[int],
        complete: Optional[bool],
        position: Optional[int],
        whalo: Optional[int],
        ehalo: Optional[int],
        shalo: Optional[int],
        nhalo: Optional[int],
        name: Optional[str],
        tile_count: Optional[int],
    ):
        _cfms_update_domains_float_2d = self.clibFMS.cFMS_update_domains_float2d

        field_shape_p, field_shape_t = setarray_Cint32(field_shape)
        field_p, field_t = setarray_Cfloat(field)
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

        _cfms_update_domains_float_2d.argtypes = [
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
        _cfms_update_domains_float_2d.restype = None

        _cfms_update_domains_float_2d(
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

    def update_domains_float_3d(
        self,
        field_shape: NDArray,
        field: NDArray,
        domain_id: Optional[int],
        flags: Optional[int],
        complete: Optional[bool],
        position: Optional[int],
        whalo: Optional[int],
        ehalo: Optional[int],
        shalo: Optional[int],
        nhalo: Optional[int],
        name: Optional[str],
        tile_count: Optional[int],
    ):
        _cfms_update_domains_float_3d = self.clibFMS.cFMS_update_domains_float_3d

        field_shape_p, field_shape_t = setarray_Cint32(field_shape)
        field_p, field_t = setarray_Cfloat(field)
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

        _cfms_update_domains_float_3d.argtypes = [
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
        _cfms_update_domains_float_3d.restype = None

        _cfms_update_domains_float_3d(
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

    def update_domains_float_4d(
        self,
        field_shape: NDArray,
        field: NDArray,
        domain_id: Optional[int],
        flags: Optional[int],
        complete: Optional[bool],
        position: Optional[int],
        whalo: Optional[int],
        ehalo: Optional[int],
        shalo: Optional[int],
        nhalo: Optional[int],
        name: Optional[str],
        tile_count: Optional[int],
    ):
        _cfms_update_domains_float_4d = self.clibFMS.cFMS_update_domains_float_4d

        field_shape_p, field_shape_t = setarray_Cint32(field_shape)
        field_p, field_t = setarray_Cfloat(field)
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

        _cfms_update_domains_float_4d.argtypes = [
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
        _cfms_update_domains_float_4d.restype = None

        _cfms_update_domains_float_4d(
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

    def update_domains_float_5d(
        self,
        field_shape: NDArray,
        field: NDArray,
        domain_id: Optional[int],
        flags: Optional[int],
        complete: Optional[bool],
        position: Optional[int],
        whalo: Optional[int],
        ehalo: Optional[int],
        shalo: Optional[int],
        nhalo: Optional[int],
        name: Optional[str],
        tile_count: Optional[int],
    ):
        _cfms_update_domains_float_5d = self.clibFMS.cFMS_update_domains_float_5d

        field_shape_p, field_shape_t = setarray_Cint32(field_shape)
        field_p, field_t = setarray_Cfloat(field)
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

        _cfms_update_domains_float_5d.argtypes = [
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
        _cfms_update_domains_float_5d.restype = None

        _cfms_update_domains_float_5d(
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

    def update_domains_int_2d(
        self,
        field_shape: NDArray,
        field: NDArray,
        domain_id: Optional[int],
        flags: Optional[int],
        complete: Optional[bool],
        position: Optional[int],
        whalo: Optional[int],
        ehalo: Optional[int],
        shalo: Optional[int],
        nhalo: Optional[int],
        name: Optional[str],
        tile_count: Optional[int],
    ):
        _cfms_update_domains_int_2d = self.clibFMS.cFMS_update_domains_int_2d

        field_shape_p, field_shape_t = setarray_Cint32(field_shape)
        field_p, field_t = setarray_Cint32(field)
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

        _cfms_update_domains_int_2d.argtypes = [
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
        _cfms_update_domains_int_2d.restype = None

        _cfms_update_domains_int_2d(
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

    def update_domains_int_3d(
        self,
        field_shape: NDArray,
        field: NDArray,
        domain_id: Optional[int],
        flags: Optional[int],
        complete: Optional[bool],
        position: Optional[int],
        whalo: Optional[int],
        ehalo: Optional[int],
        shalo: Optional[int],
        nhalo: Optional[int],
        name: Optional[str],
        tile_count: Optional[int],
    ):
        _cfms_update_domains_int_3d = self.clibFMS.cFMS_update_domains_int_3d

        field_shape_p, field_shape_t = setarray_Cint32(field_shape)
        field_p, field_t = setarray_Cint32(field)
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

        _cfms_update_domains_int_3d.argtypes = [
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
        _cfms_update_domains_int_3d.restype = None

        _cfms_update_domains_int_3d(
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

    def update_domains_int_4d(
        self,
        field_shape: NDArray,
        field: NDArray,
        domain_id: Optional[int],
        flags: Optional[int],
        complete: Optional[bool],
        position: Optional[int],
        whalo: Optional[int],
        ehalo: Optional[int],
        shalo: Optional[int],
        nhalo: Optional[int],
        name: Optional[str],
        tile_count: Optional[int],
    ):
        _cfms_update_domains_int_4d = self.clibFMS.cFMS_update_domains_int_4d

        field_shape_p, field_shape_t = setarray_Cint32(field_shape)
        field_p, field_t = setarray_Cint32(field)
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

        _cfms_update_domains_int_4d.argtypes = [
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
        _cfms_update_domains_int_4d.restype = None

        _cfms_update_domains_int_4d(
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

    def update_domains_int_5d(
        self,
        field_shape: NDArray,
        field: NDArray,
        domain_id: Optional[int],
        flags: Optional[int],
        complete: Optional[bool],
        position: Optional[int],
        whalo: Optional[int],
        ehalo: Optional[int],
        shalo: Optional[int],
        nhalo: Optional[int],
        name: Optional[str],
        tile_count: Optional[int],
    ):
        _cfms_update_domains_int_5d = self.clibFMS.cFMS_update_domains_int_5d

        field_shape_p, field_shape_t = setarray_Cint32(field_shape)
        field_p, field_t = setarray_Cint32(field)
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

        _cfms_update_domains_int_5d.argtypes = [
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
        _cfms_update_domains_int_5d.restype = None

        _cfms_update_domains_int_5d(
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


class pyDomain:
    def __init__(
        self,
        mpp_domains_obj: pyFMS_mpp_domains,
        global_indices: NDArray,
        layout: NDArray,
        domain_id: Optional[int] = None,
        pelist: Optional[NDArray] = None,
        xflags: Optional[int] = None,
        yflags: Optional[int] = None,
        xhalo: Optional[int] = None,
        yhalo: Optional[int] = None,
        xextent: Optional[NDArray] = None,
        yextent: Optional[NDArray] = None,
        maskmap: Optional[NDArray[np.bool_]] = None,
        name: Optional[str] = None,
        symmetry: Optional[bool] = None,
        memory_size: Optional[NDArray] = None,
        whalo: Optional[int] = None,
        ehalo: Optional[int] = None,
        shalo: Optional[int] = None,
        nhalo: Optional[int] = None,
        is_mosaic: Optional[bool] = None,
        tile_count: Optional[int] = None,
        tile_id: Optional[int] = None,
        complete: Optional[bool] = None,
        x_cyclic_offset: Optional[int] = None,
        y_cyclic_offset: Optional[int] = None,
    ):
        self.mpp_domains_obj = mpp_domains_obj
        self.global_indices = global_indices
        self.layout = layout
        self.domain_id = domain_id
        self.pelist = pelist
        self.xflags = xflags
        self.yflags = yflags
        self.xhalo = xhalo
        self.yhalo = yhalo
        self.xextent = xextent
        self.yextent = yextent
        self.maskmap = maskmap
        self.name = name
        self.symmetry = symmetry
        self.memory_size = memory_size
        self.whalo = whalo
        self.ehalo = ehalo
        self.shalo = shalo
        self.nhalo = nhalo
        self.is_mosaic = is_mosaic
        self.tile_count = tile_count
        self.tile_id = tile_id
        self.complete = complete
        self.x_cyclic_offset = x_cyclic_offset
        self.y_cyclic_offset = y_cyclic_offset
        self.compute_domain = pyDomainData()
        self.data_domain = pyDomainData()

        self.mpp_domains_obj.define_domains(
            global_indices=self.global_indices,
            layout=self.layout,
            domain_id=self.domain_id,
            pelist=self.pelist,
            xflags=self.xflags,
            yflags=self.yflags,
            xhalo=self.xhalo,
            yhalo=self.yhalo,
            xextent=self.xextent,
            yextent=self.yextent,
            maskmap=self.maskmap,
            name=self.name,
            symmetry=self.symmetry,
            memory_size=self.memory_size,
            whalo=self.whalo,
            ehalo=self.ehalo,
            shalo=self.shalo,
            nhalo=self.nhalo,
            is_mosaic=self.is_mosaic,
            tile_count=self.tile_count,
            tile_id=self.tile_id,
            complete=self.complete,
            x_cyclic_offset=self.x_cyclic_offset,
            y_cyclic_offset=self.y_cyclic_offset,
        )
        self.mpp_domains_obj.get_compute_domain(
            domain_data=self.compute_domain,
            domain_id=self.domain_id,
            whalo=self.whalo,
            shalo=self.shalo,
        )
        self.mpp_domains_obj.get_data_domain(
            domain_data=self.data_domain,
            domain_id=self.domain_id,
            whalo=self.whalo,
            shalo=self.shalo,
        )

    def set_compute_domain(
        self,
        xbegin: Optional[int] = None,
        xend: Optional[int] = None,
        ybegin: Optional[int] = None,
        yend: Optional[int] = None,
        xsize: Optional[int] = None,
        ysize: Optional[int] = None,
        x_is_global: Optional[bool] = None,
        y_is_global: Optional[bool] = None,
        tile_count: Optional[int] = None,
        domain_id: Optional[int] = None,
        whalo: Optional[int] = None,
        shalo: Optional[int] = None,
    ):
        self.mpp_domains_obj.set_compute_domain(
            xbegin=xbegin,
            xend=xend,
            ybegin=ybegin,
            yend=yend,
            xsize=xsize,
            ysize=ysize,
            x_is_global=x_is_global,
            y_is_global=y_is_global,
            tile_count=tile_count,
            domain_id=domain_id,
            whalo=whalo,
            shalo=shalo,
        )

        self.mpp_domains_obj.get_compute_domain(
            domain_data=self.compute_domain,
            domain_id=self.domain_id,
            whalo=self.whalo,
            shalo=self.shalo,
        )

    def set_data_domain(
        self,
        xbegin: Optional[int] = None,
        xend: Optional[int] = None,
        ybegin: Optional[int] = None,
        yend: Optional[int] = None,
        xsize: Optional[int] = None,
        ysize: Optional[int] = None,
        x_is_global: Optional[bool] = None,
        y_is_global: Optional[bool] = None,
        tile_count: Optional[int] = None,
        domain_id: Optional[int] = None,
        whalo: Optional[int] = None,
        shalo: Optional[int] = None,
    ):
        self.mpp_domains_obj.set_data_domain(
            xbegin=xbegin,
            xend=xend,
            ybegin=ybegin,
            yend=yend,
            xsize=xsize,
            ysize=ysize,
            x_is_global=x_is_global,
            y_is_global=y_is_global,
            tile_count=tile_count,
            domain_id=domain_id,
            whalo=whalo,
            shalo=shalo,
        )

        self.mpp_domains_obj.get_data_domain(
            domain_data=self.data_domain,
            domain_id=self.domain_id,
            whalo=self.whalo,
            shalo=self.shalo,
        )

    def set_global_domain(
        self,
        xbegin: Optional[int] = None,
        xend: Optional[int] = None,
        ybegin: Optional[int] = None,
        yend: Optional[int] = None,
        xsize: Optional[int] = None,
        ysize: Optional[int] = None,
        tile_count: Optional[int] = None,
        domain_id: Optional[int] = None,
        whalo: Optional[int] = None,
        shalo: Optional[int] = None,
    ):
        self.mpp_domains_obj.set_global_domain(
            xbegin=xbegin,
            xend=xend,
            ybegin=ybegin,
            yend=yend,
            xsize=xsize,
            ysize=ysize,
            tile_count=tile_count,
            domain_id=domain_id,
            whalo=whalo,
            shalo=shalo,
        )


class pyNestDomain:
    def __init__(
        self,
        mpp_domains_obj: pyFMS_mpp_domains,
        num_nest: int,
        ntiles: int,
        nest_level: NDArray,
        tile_fine: NDArray,
        tile_coarse: NDArray,
        istart_coarse: NDArray,
        icount_coarse: NDArray,
        jstart_coarse: NDArray,
        jcount_coarse: NDArray,
        npes_nest_tile: NDArray,
        x_refine: NDArray,
        y_refine: NDArray,
        nest_domain_id: Optional[int] = None,
        domain_id: Optional[int] = None,
        extra_halo: Optional[int] = None,
        name: Optional[str] = None,
    ):
        self.mpp_domains_obj = mpp_domains_obj
        self.num_nest = num_nest
        self.ntiles = ntiles
        self.nest_level = nest_level
        self.tile_fine = tile_fine
        self.tile_coarse = tile_coarse
        self.istart_coarse = istart_coarse
        self.icount_coarse = icount_coarse
        self.jstart_coarse = jstart_coarse
        self.jcount_coarse = jcount_coarse
        self.npes_nest_tile = npes_nest_tile
        self.x_refine = x_refine
        self.y_refine = y_refine
        self.nest_domain_id = nest_domain_id
        self.domain_id = domain_id
        self.extra_halo = extra_halo
        self.name = name

        self.mpp_domains_obj.define_nest_domains(
            num_nest=self.num_nest,
            ntiles=self.ntiles,
            nest_level=self.nest_level,
            tile_fine=self.tile_fine,
            tile_coarse=self.tile_coarse,
            istart_coarse=self.istart_coarse,
            icount_coarse=self.icount_coarse,
            jstart_coarse=self.jstart_coarse,
            jcount_coarse=self.jcount_coarse,
            npes_nest_tile=self.npes_nest_tile,
            x_refine=self.x_refine,
            y_refine=self.y_refine,
            nest_domain_id=self.nest_domain_id,
            domain_id=self.domain_id,
            extra_halo=self.extra_halo,
            name=self.name,
        )
