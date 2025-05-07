from ctypes import CDLL, POINTER, c_bool, c_int

import numpy as np
from numpy.typing import NDArray

from ..utils.data_handling import (
    set_Cchar,
    setarray_Cbool,
    setarray_Cdouble,
    setarray_Cfloat,
    setarray_Cint32,
    setscalar_Cbool,
    setscalar_Cint32,
)
from .domain import Domain


_libpath: str = None
_lib: type[CDLL] = None

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
WEST: int = None
SOUTH_WEST: int = None


def setlib(libpath: str, lib: type[CDLL]):

    """
    Sets _libpath and _lib module variables associated
    with the loaded cFMS library.  This function is
    to be used internally by the cfms module
    """

    global _libpath, _lib

    _libpath = libpath
    _lib = lib


def constants_init():

    """
    Retrieves and assigns mpp_domain related parameters
    from FMS
    """

    global GLOBAL_DATA_DOMAIN, BGRID_NE, CGRID_NE, DGRID_NE, AGRID
    global FOLD_SOUTH_EDGE, FOLD_WEST_EDGE, FOLD_EAST_EDGE
    global CYCLIC_GLOBAL_DOMAIN
    global NUPDATE, EUPDATE, XUPDATE, YUPDATE
    global NORTH, NORTH_EAST, EAST, SOUTH_EAST
    global CORNER, CENTER, SOUTH, SOUTH_WEST

    def get_constant(variable):
        return int(c_int.in_dll(_lib, variable).value)

    GLOBAL_DATA_DOMAIN = get_constant("GLOBAL_DATA_DOMAIN")
    BGRID_NE = get_constant("BGRID_NE")
    CGRID_NE = get_constant("CGRID_NE")
    DGRID_NE = get_constant("DGRID_NE")
    AGRID = get_constant("AGRID")
    FOLD_SOUTH_EDGE = get_constant("FOLD_SOUTH_EDGE")
    FOLD_WEST_EDGE = get_constant("FOLD_WEST_EDGE")
    FOLD_EAST_EDGE = get_constant("FOLD_EAST_EDGE")
    CYCLIC_GLOBAL_DOMAIN = get_constant("CYCLIC_GLOBAL_DOMAIN")
    NUPDATE = get_constant("NUPDATE")
    EUPDATE = get_constant("EUPDATE")
    XUPDATE = get_constant("XUPDATE")
    YUPDATE = get_constant("YUPDATE")
    NORTH = get_constant("NORTH")
    NORTH_EAST = get_constant("NORTH_EAST")
    EAST = get_constant("EAST")
    SOUTH_EAST = get_constant("SOUTH_EAST")
    CORNER = get_constant("CORNER")
    CENTER = get_constant("CENTER")
    SOUTH = get_constant("SOUTH")
    SOUTH_WEST = get_constant("SOUTH_WEST")
    WEST = get_constant("WEST")
    NORTH_WEST = get_constant("NORTH_WEST")


def get_compute_domain(
    domain_id: int,
    position: int = None,
    tile_count: int = None,
    whalo: int = None,
    shalo: int = None,
) -> dict:

    """
    Queries and returns a dictionary of compute domain indices and
    compute domain size associated with domain_id.  The returned
    dictionary can be passed into the update method in class pyDomain
    to update the pyfms domain object.
    """

    _cfms_get_compute_domain = _lib.cFMS_get_compute_domain

    default_i = 0
    default_b = False

    domain_id_t = c_int
    xbegin_t = c_int
    xend_t = c_int
    ybegin_t = c_int
    yend_t = c_int
    xsize_t = c_int
    xmax_size_t = c_int
    ysize_t = c_int
    ymax_size_t = c_int
    x_is_global_t = c_bool
    y_is_global_t = c_bool
    tile_count_t = c_int
    position_t = c_int
    whalo_t = c_int
    shalo_t = c_int

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
        POINTER(domain_id_t),
        POINTER(xbegin_t),
        POINTER(xend_t),
        POINTER(ybegin_t),
        POINTER(yend_t),
        POINTER(xsize_t),
        POINTER(xmax_size_t),
        POINTER(ysize_t),
        POINTER(ymax_size_t),
        POINTER(x_is_global_t),
        POINTER(y_is_global_t),
        POINTER(tile_count_t),
        POINTER(position_t),
        POINTER(whalo_t),
        POINTER(shalo_t),
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
        isc=xbegin_c.value,
        jsc=ybegin_c.value,
        iec=xend_c.value,
        jec=yend_c.value,
        xsize_c=xsize_c.value,
        ysize_c=ysize_c.value,
        xmax_size_c=xmax_size_c.value,
        ymax_size_c=ymax_size_c.value,
        x_is_global_c=x_is_global_c.value,
        y_is_global_c=y_is_global_c.value,
    )


def get_data_domain(
    domain_id: int,
    position: int = None,
    tile_count: int = None,
    whalo: int = None,
    shalo: int = None,
) -> dict:

    """
    Queries and returns a dictionary of data domain indices and
    data domain size associated with domain_id.  The returned
    dictionary can be passed into the update method in class pyDomain
    to update the pyfms domain object.
    """

    _cfms_get_data_domain = _lib.cFMS_get_data_domain

    default_i = 0
    default_b = False

    domain_id_t = c_int
    xbegin_t = c_int
    xend_t = c_int
    ybegin_t = c_int
    yend_t = c_int
    xsize_t = c_int
    xmax_size_t = c_int
    ysize_t = c_int
    ymax_size_t = c_int
    x_is_global_t = c_bool
    y_is_global_t = c_bool
    tile_count_t = c_int
    position_t = c_int
    whalo_t = c_int
    shalo_t = c_int

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
        POINTER(domain_id_t),
        POINTER(xbegin_t),
        POINTER(xend_t),
        POINTER(ybegin_t),
        POINTER(yend_t),
        POINTER(xsize_t),
        POINTER(xmax_size_t),
        POINTER(ysize_t),
        POINTER(ymax_size_t),
        POINTER(x_is_global_t),
        POINTER(y_is_global_t),
        POINTER(tile_count_t),
        POINTER(position_t),
        POINTER(whalo_t),
        POINTER(shalo_t),
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
        isd=xbegin_c.value,
        jsd=ybegin_c.value,
        ied=xend_c.value,
        jed=yend_c.value,
        xsize_d=xsize_c.value,
        ysize_d=ysize_c.value,
        xmax_size_d=xmax_size_c.value,
        ymax_size_d=ymax_size_c.value,
        x_is_global_d=x_is_global_c.value,
        y_is_global_d=y_is_global_c.value,
    )


def define_domains(
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
) -> type(Domain):

    """
    Creates a domain.  Automatically queries the newly formed
    compute and data domains and returns a pyDomain object with
    queried domain information. The returned domain_id
    corresponds to the saved FmsMppDomain2D derived type in cFMS
    """

    _cfms_define_domains = _lib.cFMS_define_domains

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

    _cfms_define_domains.restype = c_int

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

    compute = get_compute_domain(
        domain_id=domain_id, tile_count=tile_count, whalo=whalo, shalo=shalo
    )
    data = get_data_domain(
        domain_id=domain_id, tile_count=tile_count, whalo=whalo, shalo=shalo
    )

    domain = Domain()
    for key in compute:
        setattr(domain, key, compute[key])
    for key in data:
        setattr(domain, key, data[key])
    return domain


def define_io_domain(io_layout: list[int], domain_id: int):

    """
    Defines the io domain for domain with domain_id
    """

    _cfms_define_io_domain = _lib.cFMS_define_io_domain

    io_layout_arr = np.array(io_layout, dtype=np.int32)

    io_layout_p, io_layout_t = setarray_Cint32(io_layout_arr)
    domain_id_c, domain_id_t = setscalar_Cint32(domain_id)

    _cfms_define_io_domain.argtypes = [io_layout_t, domain_id_t]
    _cfms_define_io_domain.restype = None

    _cfms_define_io_domain(io_layout_p, domain_id_c)


def define_layout(global_indices: list[int], ndivs: int) -> list:

    """
    Defines the layout associated with a domain decomposition
    """

    layout = np.empty(shape=2, dtype=np.int32, order="C")

    global_indices_arr = np.array(global_indices, dtype=np.int32)

    _cfms_define_layout = _lib.cFMS_define_layout

    global_indices_p, global_indices_t = setarray_Cint32(global_indices_arr)
    ndivs_c, ndivs_t = setscalar_Cint32(ndivs)
    layout_p, layout_t = setarray_Cint32(layout)

    _cfms_define_layout.argtypes = [global_indices_t, ndivs_t, layout_t]
    _cfms_define_layout.restype = None

    _cfms_define_layout(global_indices_p, ndivs_c, layout_p)

    return layout.tolist()


def define_nest_domains(
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

    """
    Defines the nest domain where the the parent domain has domain_id
    Returns a nest_domain_id corresponding to the FmsMppDomainsNestDomain
    type saved in cFMS
    """

    _cfms_define_nest_domain = _lib.cFMS_define_nest_domains

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
    _cfms_define_nest_domain.restype = c_int

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


def domain_is_initialized(domain_id: int) -> bool:

    """
    Returns True if domain with domain_id has been initialized;
    else, returns False
    """

    _cfms_domain_is_initialized = _lib.cFMS_domain_is_initialized

    domain_id_c, domain_id_t = setscalar_Cint32(domain_id)

    _cfms_domain_is_initialized.argtypes = [domain_id_t]
    _cfms_domain_is_initialized.restype = c_bool

    return _cfms_domain_is_initialized(domain_id_c)


def get_domain_name(domain_id: int) -> str:

    """
    Returns the domain name associated with domain_id
    """

    _cfms_get_domain_name = _lib.cFMS_get_domain_name

    domain_name = ""

    domain_name_c, domain_name_t = set_Cchar(domain_name)
    domain_id_c, domain_id_t = setscalar_Cint32(domain_id)

    _cfms_get_domain_name.argtypes = [domain_name_t, domain_id_t]
    _cfms_get_domain_name.restype = None

    _cfms_get_domain_name(domain_name_c, domain_id_c)

    return domain_name_c.value.decode("utf-8")


def get_layout(domain_id: int) -> list[int]:

    """
    Returns the layout associated with domain_id
    """

    layout = np.empty(shape=2, dtype=np.int32, order="C")

    _cfms_get_layout = _lib.cFMS_get_layout

    layout_p, layout_t = setarray_Cint32(layout)
    domain_id_c, domain_id_t = setscalar_Cint32(domain_id)

    _cfms_get_layout.argtypes = [layout_t, domain_id_t]
    _cfms_get_layout.restype = None

    _cfms_get_layout(layout_p, domain_id_c)

    return layout_p.tolist()


def get_domain_pelist(domain_id: int) -> list[int]:

    """
    Returns the pelist associated with domain_id
    """

    npes = c_int.in_dll(_lib, "cFMS_pelist_npes")
    pelist = np.empty(shape=npes.value, dtype=np.int32, order="C")

    _cfms_get_domain_pelist = _lib.cFMS_get_domain_pelist

    pelist_p, pelist_t = setarray_Cint32(pelist)
    domain_id_c, domain_id_t = setscalar_Cint32(domain_id)

    _cfms_get_domain_pelist.argtypes = [pelist_t, domain_id_t]
    _cfms_get_domain_pelist.restype = None

    _cfms_get_domain_pelist(pelist_p, domain_id_c)

    return pelist_p.tolist()


def set_compute_domain(
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

    """
    Overrides the default compute domain set with define_domains
    for domain_id.
    This function does not update the pyDomain object that was
    created from define_domains.  Users will need to call
    get_compute domain and the update method in pyDomain
    to update the pyDomain object
    """

    _cfms_set_compute_domain = _lib.cFMS_set_compute_domain

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


def set_current_domain(domain_id: int):

    """
    Sets current_domain in cFMS to be the domain with domain_id
    This function is to be used internally in pyFMS
    """

    cfms_set_current_domain = _lib.cFMS_set_current_domain

    domain_id_c, domain_id_t = setscalar_Cint32(domain_id)

    cfms_set_current_domain.argtypes = [domain_id_t]
    cfms_set_current_domain.restype = None

    cfms_set_current_domain(domain_id_c)


def set_current_nest_domain(nest_domain_id: int):

    """
    Sets current_nest_domain in cFMS to be the nest domain with nest_domain_id
    This function is to be used internally in pyFMS
    """

    cfms_set_current_nest_domain = _lib.cFMS_set_current_nest_domain

    nest_domain_id_c, nest_domain_id_t = setscalar_Cint32(nest_domain_id)

    cfms_set_current_nest_domain.argtypes = [nest_domain_id_t]
    cfms_set_current_nest_domain.restype = None

    cfms_set_current_nest_domain(nest_domain_id_c)


def set_data_domain(
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

    """
    Overrides the default data domain set with define_domains
    for domain_id
    This function does not update the pyDomain object that was
    created from define_domains.  Users will need to call
    get_data domain and the update method in pyDomain
    to update the pyDomain object
    """

    _cfms_set_data_domain = _lib.cFMS_set_data_domain

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


def set_global_domain(
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

    """
    Overrides the default global domain set with define_domains
    for domain_id
    """

    _cfms_set_global_domain = _lib.cFMS_set_global_domain

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

    """
    Updates the field values for the halo regions
    in the data domain associated with domain_id
    """

    if name is not None:
        name = name[:64]

    if field.ndim == 2:
        if field.dtype == np.float64:
            _cfms_update_domains = _lib.cFMS_update_domains_double_2d
            field_p, field_t = setarray_Cdouble(field)
        elif field.dtype == np.float32:
            _cfms_update_domains = _lib.cFMS_update_domains_float_2d
            field_p, field_t = setarray_Cfloat(field)
        elif field.dtype == np.int32:
            _cfms_update_domains = _lib.cFMS_update_domains_int_2d
            field_p, field_t = setarray_Cfloat(field)
        else:
            raise RuntimeError(
                f"udate_domains input field datatype {field.dtype} unsupported"
            )
    elif field.ndim == 3:
        if field.dtype == np.float64:
            _cfms_update_domains = _lib.cFMS_update_domains_double_3d
            field_p, field_t = setarray_Cdouble(field)
        elif field.dtype == np.float32:
            _cfms_update_domains = _lib.cFMS_update_domains_float_3d
            field_p, field_t = setarray_Cfloat(field)
        elif field.dtype == np.int32:
            _cfms_update_domains = _lib.cFMS_update_domains_int_3d
            field_p, field_t = setarray_Cfloat(field)
        else:
            raise RuntimeError(
                f"udate_domains input field datatype {field.dtype} unsupported"
            )
    elif field.ndim == 4:
        if field.dtype == np.float64:
            _cfms_update_domains = _lib.cFMS_update_domains_double_4d
            field_p, field_t = setarray_Cdouble(field)
        elif field.dtype == np.float32:
            _cfms_update_domains = _lib.cFMS_update_domains_float_4d
            field_p, field_t = setarray_Cfloat(field)
        elif field.dtype == np.int32:
            _cfms_update_domains = _lib.cFMS_update_domains_int_4d
            field_p, field_t = setarray_Cfloat(field)
        else:
            raise RuntimeError(
                f"udate_domains input field datatype {field.dtype} unsupported"
            )
    elif field.ndim == 5:
        if field.dtype == np.float64:
            _cfms_update_domains = _lib.cFMS_update_domains_double_5d
            field_p, field_t = setarray_Cdouble(field)
        elif field.dtype == np.float32:
            _cfms_update_domains = _lib.cFMS_update_domains_float_5d
            field_p, field_t = setarray_Cfloat(field)
        elif field.dtype == np.int32:
            _cfms_update_domains = _lib.cFMS_update_domains_int_5d
            field_p, field_t = setarray_Cfloat(field)
        else:
            raise RuntimeError(
                f"udate_domains input field datatype {field.dtype} unsupported"
            )
    else:
        raise RuntimeError(f"update_domains field dimension {field.ndim}d unsupported")

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
