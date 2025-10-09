from typing import Any

import numpy as np
from numpy.typing import NDArray

from pyfms.py_mpp import _mpp_domains_functions
from pyfms.py_mpp.domain import Domain
from pyfms.utils.ctypes_utils import (
    check_str,
    get_constant_int,
    set_array,
    set_c_bool,
    set_c_int,
    set_c_str,
    set_list,
)


_libpath = None
_lib = None

GLOBAL_DATA_DOMAIN = None
BGRID_NE = None
CGRID_NE = None
DGRID_NE = None
AGRID = None
FOLD_SOUTH_EDGE = None
FOLD_WEST_EDGE = None
FOLD_EAST_EDGE = None
FOLD_NORTH_EDGE = None
CYCLIC_GLOBAL_DOMAIN = None
NUPDATE = None
EUPDATE = None
XUPDATE = None
YUPDATE = None
NORTH = None
NORTH_EAST = None
EAST = None
SOUTH_EAST = None
CORNER = None
CENTER = None
SOUTH = None
WEST = None
SOUTH_WEST = None

_cFMS_get_compute_domain = None
_cFMS_get_data_domain = None
_cFMS_define_domains = None
_cFMS_define_io_domain = None
_cFMS_define_layout = None
_cFMS_define_nest_domains = None
_cFMS_define_cubic_mosaic = None
_cFMS_domain_is_initialized = None
_cFMS_get_domain_name = None
_cFMS_get_layout = None
_cFMS_get_domain_pelist = None
_cFMS_set_compute_domain = None
_cFMS_set_current_domain = None
_cFMS_set_data_domain = None
_cFMS_set_global_domain = None
_cFMS_update_domains_int_2d = None
_cFMS_update_domains_float_2d = None
_cFMS_update_domains_double_2d = None
_cFMS_update_domains_int_3d = None
_cFMS_update_domains_float_3d = None
_cFMS_update_domains_double_3d = None
_cFMS_update_domains_int_4d = None
_cFMS_update_domains_float_4d = None
_cFMS_update_domains_double_4d = None
_cFMS_update_domains_int_5d = None
_cFMS_update_domains_float_5d = None
_cFMS_update_domains_double_5d = None
_cFMS_update_domains = {}
_cFMS_v_update_domains_float_2d = None
_cFMS_v_update_domains_double_2d = None
_cFMS_v_update_domains_float_3d = None
_cFMS_v_update_domains_double_3d = None
_cFMS_v_update_domains_float_4d = None
_cFMS_v_update_domains_double_4d = None
_cFMS_v_update_domains_float_5d = None
_cFMS_v_update_domains_double_5d = None
_cFMS_v_update_domains = {}


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

    arglist = []
    set_c_int(domain_id, arglist)
    xbegin = set_c_int(0, arglist)
    xend = set_c_int(0, arglist)
    ybegin = set_c_int(0, arglist)
    yend = set_c_int(0, arglist)
    xsize = set_c_int(0, arglist)
    xmax_size = set_c_int(0, arglist)
    ysize = set_c_int(0, arglist)
    ymax_size = set_c_int(0, arglist)
    x_is_global = set_c_bool(False, arglist)
    y_is_global = set_c_bool(False, arglist)
    set_c_int(tile_count, arglist)
    set_c_int(position, arglist)
    set_c_int(whalo, arglist)
    set_c_int(shalo, arglist)

    _cFMS_get_compute_domain(*arglist)

    return dict(
        domain_id_c=domain_id,
        isc=xbegin.value,
        jsc=ybegin.value,
        iec=xend.value,
        jec=yend.value,
        xsize_c=xsize.value,
        ysize_c=ysize.value,
        xmax_size_c=xmax_size.value,
        ymax_size_c=ymax_size.value,
        x_is_global_c=x_is_global.value,
        y_is_global_c=y_is_global.value,
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

    arglist = []
    set_c_int(domain_id, arglist)
    xbegin = set_c_int(0, arglist)
    xend = set_c_int(0, arglist)
    ybegin = set_c_int(0, arglist)
    yend = set_c_int(0, arglist)
    xsize = set_c_int(0, arglist)
    xmax_size = set_c_int(0, arglist)
    ysize = set_c_int(0, arglist)
    ymax_size = set_c_int(0, arglist)
    x_is_global = set_c_bool(False, arglist)
    y_is_global = set_c_bool(False, arglist)
    set_c_int(tile_count, arglist)
    set_c_int(position, arglist)
    set_c_int(whalo, arglist)
    set_c_int(shalo, arglist)

    _cFMS_get_data_domain(*arglist)

    return dict(
        domain_id=domain_id,
        isd=xbegin.value,
        jsd=ybegin.value,
        ied=xend.value,
        jed=yend.value,
        xsize_d=xsize.value,
        ysize_d=ysize.value,
        xmax_size_d=xmax_size.value,
        ymax_size_d=ymax_size.value,
        x_is_global_d=x_is_global.value,
        y_is_global_d=y_is_global.value,
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

    arglist = []
    set_list(global_indices, np.int32, arglist)
    set_list(layout, np.int32, arglist)
    set_c_int(1 if pelist is None else len(pelist), arglist)
    set_list(pelist, np.int32, arglist)
    set_c_int(xflags, arglist)
    set_c_int(yflags, arglist)
    set_c_int(xhalo, arglist)
    set_c_int(yhalo, arglist)
    set_list(xextent, np.int32, arglist)
    set_list(yextent, np.int32, arglist)
    set_list(maskmap, np.bool, arglist)
    set_c_str(name, arglist)
    set_c_bool(symmetry, arglist)
    set_list(memory_size, np.int32, arglist)
    set_c_int(whalo, arglist)
    set_c_int(ehalo, arglist)
    set_c_int(shalo, arglist)
    set_c_int(nhalo, arglist)
    set_c_bool(is_mosaic, arglist)
    set_c_int(tile_count, arglist)
    set_c_int(tile_id, arglist)
    set_c_bool(complete, arglist)
    set_c_int(x_cyclic_offset, arglist)
    set_c_int(y_cyclic_offset, arglist)

    domain_id = _cFMS_define_domains(*arglist)

    compute = get_compute_domain(
        domain_id=domain_id, tile_count=tile_count, whalo=whalo, shalo=shalo
    )
    data = get_data_domain(
        domain_id=domain_id, tile_count=tile_count, whalo=whalo, shalo=shalo
    )

    domain = Domain(domain_id=domain_id)
    for key in compute:
        setattr(domain, key, compute[key])
    for key in data:
        setattr(domain, key, data[key])

    domain.isg = global_indices[0]
    domain.ieg = global_indices[1]
    domain.jsg = global_indices[2]
    domain.jeg = global_indices[3]

    return domain


def define_io_domain(io_layout: list[int], domain_id: int):

    """
    Defines the io domain for domain with domain_id
    """

    arglist = []
    set_list(io_layout, np.int32, arglist)
    set_c_int(domain_id, arglist)

    _cFMS_define_io_domain(*arglist)


def define_layout(global_indices: list[int], ndivs: int) -> list:

    """
    Defines the layout associated with a domain decomposition
    """

    arglist = []
    set_list(global_indices, np.int32, arglist)
    set_c_int(ndivs, arglist)
    layout = set_list([0] * 2, np.int32, arglist)

    _cFMS_define_layout(*arglist)

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

    arglist = []
    set_c_int(num_nest, arglist)
    set_c_int(ntiles, arglist)
    set_list(nest_level, np.int32, arglist)
    set_list(tile_fine, np.int32, arglist)
    set_list(tile_coarse, np.int32, arglist)
    set_list(istart_coarse, np.int32, arglist)
    set_list(icount_coarse, np.int32, arglist)
    set_list(jstart_coarse, np.int32, arglist)
    set_list(jcount_coarse, np.int32, arglist)
    set_list(npes_nest_tile, np.int32, arglist)
    set_list(x_refine, np.int32, arglist)
    set_list(y_refine, np.int32, arglist)
    set_c_int(domain_id, arglist)
    set_c_int(extra_halo, arglist)
    set_c_str(name, arglist)

    return _cFMS_define_nest_domains(*arglist)


def define_cubic_mosaic(
    ni: list[int],
    nj: list[int],
    global_indices: list[int],
    layout: list[int],
    ntiles: int,
    halo: int = None,
    use_memsize: bool = None,
) -> int:

    """
    Defines a cubic mosaic domain based on the
    given global indices and layout.
    Returns a domain id corresponding to the
    FmsMPPDomain2D type saved in cFMS.
    """

    arglist = []
    set_list(ni, np.int32, arglist)
    set_list(nj, np.int32, arglist)
    set_list(global_indices, np.int32, arglist)
    set_list(layout, np.int32, arglist)
    set_c_int(ntiles, arglist)
    set_c_int(halo, arglist)
    set_c_bool(use_memsize, arglist)

    return _cFMS_define_cubic_mosaic(*arglist)


def domain_is_initialized(domain_id: int) -> bool:

    """
    Returns True if domain with domain_id has been initialized;
    else, returns False
    """

    arglist = []
    set_c_int(domain_id, arglist)

    return _cFMS_domain_is_initialized(*arglist)


def get_domain_name(domain_id: int) -> str:

    """
    Returns the domain name associated with domain_id
    """

    arglist = []
    name = set_c_str(" ", arglist)
    set_c_int(domain_id, arglist)

    _cFMS_get_domain_name(*arglist)

    return name.value.decode("utf-8")


def get_layout(domain_id: int) -> list[int]:

    """
    Returns the layout associated with domain_id
    """

    arglist = []
    layout = set_list([0] * 2, np.int32, arglist)
    set_c_int(domain_id, arglist)

    _cFMS_get_layout(layout, domain_id)

    return layout.tolist()


def get_domain_pelist(domain_id: int) -> list[int]:

    """
    Returns the pelist associated with domain_id
    """

    npes = get_constant_int(_lib, "cFMS_pelist_npes")

    arglist = []
    pelist = set_list([0] * npes, np.int32, arglist)
    set_c_int(domain_id, arglist)

    _cFMS_get_domain_pelist(*arglist)

    return pelist.tolist()


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

    arglist = []
    set_c_int(domain_id, arglist)
    set_c_int(xbegin, arglist)
    set_c_int(xend, arglist)
    set_c_int(ybegin, arglist)
    set_c_int(yend, arglist)
    set_c_int(xsize, arglist)
    set_c_int(ysize, arglist)
    set_c_bool(x_is_global, arglist)
    set_c_bool(y_is_global, arglist)
    set_c_int(tile_count, arglist)
    set_c_int(whalo, arglist)
    set_c_int(shalo, arglist)

    _cFMS_set_compute_domain(*arglist)


def set_current_domain(domain_id: int):

    """
    Sets current_domain in cFMS to be the domain with domain_id
    This function is to be used internally in pyFMS
    """

    arglist = []
    set_c_int(domain_id, arglist)

    _cFMS_set_current_domain(*arglist)


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

    arglist = []
    set_c_int(domain_id, arglist)
    set_c_int(xbegin, arglist)
    set_c_int(xend, arglist)
    set_c_int(ybegin, arglist)
    set_c_int(yend, arglist)
    set_c_int(xsize, arglist)
    set_c_int(ysize, arglist)
    set_c_bool(x_is_global, arglist)
    set_c_bool(x_is_global, arglist)
    set_c_int(tile_count, arglist)
    set_c_int(whalo, arglist)
    set_c_int(shalo, arglist)

    _cFMS_set_data_domain(*arglist)


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

    arglist = []
    set_c_int(domain_id, arglist)
    set_c_int(xbegin, arglist)
    set_c_int(xend, arglist)
    set_c_int(ybegin, arglist)
    set_c_int(yend, arglist)
    set_c_int(xsize, arglist)
    set_c_int(ysize, arglist)
    set_c_int(tile_count, arglist)
    set_c_int(whalo, arglist)
    set_c_int(shalo, arglist)

    _cFMS_set_global_domain(*arglist)


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
    convert_cf_order: bool = True,
):

    """
    Updates the field values for the halo regions
    in the data domain associated with domain_id
    """

    try:
        cFMS_update_this = _cFMS_update_domains[field.ndim][field.dtype.name]
    except KeyError:
        raise RuntimeError(
            f"mpp_domains.update:"
            "data of dimensions {field.ndim} and/or "
            f"of type {field.dtype}"
        )

    check_str(name, 64, "mpp_domains.update")

    arglist = []
    set_list(field.shape, np.int32, arglist)
    set_array(field, arglist)
    set_c_int(domain_id, arglist)
    set_c_int(flags, arglist)
    set_c_bool(complete, arglist)
    set_c_int(position, arglist)
    set_c_int(whalo, arglist)
    set_c_int(ehalo, arglist)
    set_c_int(shalo, arglist)
    set_c_int(nhalo, arglist)
    set_c_str(name, arglist)
    set_c_int(tile_count, arglist)
    set_c_bool(convert_cf_order, arglist)

    cFMS_update_this(*arglist)


def vector_update_domains(
    fieldx: NDArray,
    fieldy: NDArray,
    domain_id: int = None,
    flags: int = None,
    gridtype: int = None,
    complete: bool = None,
    whalo: int = None,
    ehalo: int = None,
    shalo: int = None,
    nhalo: int = None,
    name: str = None,
    tile_count: int = None,
    convert_cf_order: bool = True,
):
    try:
        cFMS_v_update_this = _cFMS_v_update_domains[fieldx.ndim][fieldx.dtype.name]
    except KeyError:
        raise RuntimeError(
            f"mpp_domains.vector_update:"
            f"data of dimensions {fieldx.ndim} and/or "
            f"of type {fieldx.dtype} "
            "not implemented"
        )
    check_str(name, 64, "mpp_domains.vector_update")

    arglist = []
    set_list(fieldx.shape, np.int32, arglist)
    set_array(fieldx, arglist)
    set_list(fieldy.shape, np.int32, arglist)
    set_array(fieldy, arglist)
    set_c_int(domain_id, arglist)
    set_c_int(flags, arglist)
    set_c_int(gridtype, arglist)
    set_c_bool(complete, arglist)
    set_c_int(whalo, arglist)
    set_c_int(ehalo, arglist)
    set_c_int(shalo, arglist)
    set_c_int(nhalo, arglist)
    set_c_str(name, arglist)
    set_c_int(tile_count, arglist)
    set_c_bool(convert_cf_order, arglist)

    cFMS_v_update_this(*arglist)


def _init_constants():

    """
    Retrieves and assigns mpp_domain related parameters
    from FMS
    """

    global GLOBAL_DATA_DOMAIN, BGRID_NE, CGRID_NE, DGRID_NE, AGRID
    global FOLD_SOUTH_EDGE, FOLD_WEST_EDGE, FOLD_EAST_EDGE, FOLD_NORTH_EDGE
    global CYCLIC_GLOBAL_DOMAIN
    global NUPDATE, EUPDATE, XUPDATE, YUPDATE
    global NORTH, NORTH_EAST, EAST, SOUTH_EAST
    global CORNER, CENTER, SOUTH, SOUTH_WEST

    GLOBAL_DATA_DOMAIN = get_constant_int(_lib, "GLOBAL_DATA_DOMAIN")
    BGRID_NE = get_constant_int(_lib, "BGRID_NE")
    CGRID_NE = get_constant_int(_lib, "CGRID_NE")
    DGRID_NE = get_constant_int(_lib, "DGRID_NE")
    AGRID = get_constant_int(_lib, "AGRID")
    FOLD_SOUTH_EDGE = get_constant_int(_lib, "FOLD_SOUTH_EDGE")
    FOLD_WEST_EDGE = get_constant_int(_lib, "FOLD_WEST_EDGE")
    FOLD_EAST_EDGE = get_constant_int(_lib, "FOLD_EAST_EDGE")
    FOLD_NORTH_EDGE = get_constant_int(_lib, "FOLD_NORTH_EDGE")
    CYCLIC_GLOBAL_DOMAIN = get_constant_int(_lib, "CYCLIC_GLOBAL_DOMAIN")
    NUPDATE = get_constant_int(_lib, "NUPDATE")
    EUPDATE = get_constant_int(_lib, "EUPDATE")
    XUPDATE = get_constant_int(_lib, "XUPDATE")
    YUPDATE = get_constant_int(_lib, "YUPDATE")
    NORTH = get_constant_int(_lib, "NORTH")
    NORTH_EAST = get_constant_int(_lib, "NORTH_EAST")
    EAST = get_constant_int(_lib, "EAST")
    SOUTH_EAST = get_constant_int(_lib, "SOUTH_EAST")
    CORNER = get_constant_int(_lib, "CORNER")
    CENTER = get_constant_int(_lib, "CENTER")
    SOUTH = get_constant_int(_lib, "SOUTH")
    SOUTH_WEST = get_constant_int(_lib, "SOUTH_WEST")
    WEST = get_constant_int(_lib, "WEST")
    NORTH_WEST = get_constant_int(_lib, "NORTH_WEST")


def _init_functions():

    global _cFMS_get_compute_domain
    global _cFMS_get_data_domain
    global _cFMS_define_domains
    global _cFMS_define_io_domain
    global _cFMS_define_layout
    global _cFMS_define_nest_domains
    global _cFMS_define_cubic_mosaic
    global _cFMS_domain_is_initialized
    global _cFMS_get_domain_name
    global _cFMS_get_layout
    global _cFMS_get_domain_pelist
    global _cFMS_set_compute_domain
    global _cFMS_set_current_domain
    global _cFMS_set_data_domain
    global _cFMS_set_global_domain
    global _cFMS_update_domains_int_2d
    global _cFMS_update_domains_float_2d
    global _cFMS_update_domains_double_2d
    global _cFMS_update_domains_int_3d
    global _cFMS_update_domains_float_3d
    global _cFMS_update_domains_double_3d
    global _cFMS_update_domains_int_4d
    global _cFMS_update_domains_float_4d
    global _cFMS_update_domains_double_4d
    global _cFMS_update_domains_int_5d
    global _cFMS_update_domains_float_5d
    global _cFMS_update_domains_double_5d
    global _cFMS_update_domains
    global _cFMS_v_update_domains_float_2d
    global _cFMS_v_update_domains_double_2d
    global _cFMS_v_update_domains_float_3d
    global _cFMS_v_update_domains_double_3d
    global _cFMS_v_update_domains_float_4d
    global _cFMS_v_update_domains_double_4d
    global _cFMS_v_update_domains_float_5d
    global _cFMS_v_update_domains_double_5d
    global _cFMS_v_update_domains

    _cFMS_get_compute_domain = _lib.cFMS_get_compute_domain
    _cFMS_get_data_domain = _lib.cFMS_get_data_domain
    _cFMS_define_domains = _lib.cFMS_define_domains
    _cFMS_define_io_domain = _lib.cFMS_define_io_domain
    _cFMS_define_layout = _lib.cFMS_define_layout
    _cFMS_define_nest_domains = _lib.cFMS_define_nest_domains
    _cFMS_define_cubic_mosaic = _lib.cFMS_define_cubic_mosaic
    _cFMS_domain_is_initialized = _lib.cFMS_domain_is_initialized
    _cFMS_get_domain_name = _lib.cFMS_get_domain_name
    _cFMS_get_layout = _lib.cFMS_get_layout
    _cFMS_get_domain_pelist = _lib.cFMS_get_domain_pelist
    _cFMS_set_compute_domain = _lib.cFMS_set_compute_domain
    _cFMS_set_current_domain = _lib.cFMS_set_current_domain
    _cFMS_set_data_domain = _lib.cFMS_set_data_domain
    _cFMS_set_global_domain = _lib.cFMS_set_global_domain
    _cFMS_update_domains_int_2d = _lib.cFMS_update_domains_int_2d
    _cFMS_update_domains_float_2d = _lib.cFMS_update_domains_float_2d
    _cFMS_update_domains_double_2d = _lib.cFMS_update_domains_double_2d
    _cFMS_update_domains_int_3d = _lib.cFMS_update_domains_int_3d
    _cFMS_update_domains_float_3d = _lib.cFMS_update_domains_float_3d
    _cFMS_update_domains_double_3d = _lib.cFMS_update_domains_double_3d
    _cFMS_update_domains_int_4d = _lib.cFMS_update_domains_int_4d
    _cFMS_update_domains_float_4d = _lib.cFMS_update_domains_float_4d
    _cFMS_update_domains_double_4d = _lib.cFMS_update_domains_double_4d
    _cFMS_update_domains_int_5d = _lib.cFMS_update_domains_int_5d
    _cFMS_update_domains_float_5d = _lib.cFMS_update_domains_float_5d
    _cFMS_update_domains_double_5d = _lib.cFMS_update_domains_double_5d
    _cFMS_v_update_domains_float_2d = _lib.cFMS_v_update_domains_float_2d
    _cFMS_v_update_domains_double_2d = _lib.cFMS_v_update_domains_double_2d
    _cFMS_v_update_domains_float_3d = _lib.cFMS_v_update_domains_float_3d
    _cFMS_v_update_domains_double_3d = _lib.cFMS_v_update_domains_double_3d
    _cFMS_v_update_domains_float_4d = _lib.cFMS_v_update_domains_float_4d
    _cFMS_v_update_domains_double_4d = _lib.cFMS_v_update_domains_double_4d
    _cFMS_v_update_domains_float_5d = _lib.cFMS_v_update_domains_float_5d
    _cFMS_v_update_domains_double_5d = _lib.cFMS_v_update_domains_double_5d

    _mpp_domains_functions.define(_lib)

    _cFMS_update_domains = {
        2: {
            "int": _cFMS_update_domains_int_2d,
            "float32": _cFMS_update_domains_float_2d,
            "float64": _cFMS_update_domains_double_2d,
        },
        3: {
            "int": _cFMS_update_domains_int_3d,
            "float32": _cFMS_update_domains_float_3d,
            "float64": _cFMS_update_domains_double_3d,
        },
        4: {
            "int": _cFMS_update_domains_int_4d,
            "float32": _cFMS_update_domains_float_4d,
            "float64": _cFMS_update_domains_double_4d,
        },
        5: {
            "int": _cFMS_update_domains_int_5d,
            "float32": _cFMS_update_domains_float_5d,
            "float64": _cFMS_update_domains_double_5d,
        },
    }

    _cFMS_v_update_domains = {
        2: {
            "float32": _cFMS_v_update_domains_float_2d,
            "float64": _cFMS_v_update_domains_double_2d,
        },
        3: {
            "float32": _cFMS_v_update_domains_float_3d,
            "float64": _cFMS_v_update_domains_double_3d,
        },
        4: {
            "float32": _cFMS_v_update_domains_float_4d,
            "float64": _cFMS_v_update_domains_double_4d,
        },
        5: {
            "float32": _cFMS_v_update_domains_float_5d,
            "float64": _cFMS_v_update_domains_double_5d,
        },
    }


def _init(libpath: str, lib: Any):

    """
    Sets _libpath and _lib module variables associated
    with the loaded cFMS library.  This function is
    to be used internally by the cfms module
    """

    global _libpath, _lib

    _libpath = libpath
    _lib = lib

    _init_constants()
    _init_functions()
