from typing import Any

from pyfms.utils.ctypes_utils import get_constant_double


_libpath = None
_lib = None

PI = None
RAD_TO_DEG = None
DEG_TO_RAD = None
RADIAN = None
RADIUS = None
OMEGA = None
GRAV = None
SECONDS_PER_DAY = None
SECONDS_PER_HOUR = None
SECONDS_PER_MINUTE = None
RADGAS = None
RVGAS = None
HLV = None
HLS = None
KAPPA = None
CP_AIR = None
CP_VAPOR = None
CP_OCEAN = None
DENS_H20 = None
RHOAIR = None
RHO0 = None
RHO0R = None
RHO_CP = None
O2MIXRAT = None
WTMAIR = None
WTMH2O = None
WTMOZONE = None
WTMC = None
WTMCO2 = None
WTMCH4 = None
WTMO2 = None
WTMCFC11 = None
WTMCFC12 = None
WTMN = None
DIFFAC = None
ES0 = None
PSTD = None
PSTD_MKS = None
KELVIN = None
TFREEZE = None
C2DBARS = None
STEFAN = None
AVOGNO = None
VONKARM = None
ALOGMIN = None
EPSLN = None
RADCON = None
RADCON_MKS = None


def _init_constants():

    """
    Initializes all FMS constants
    All constants are initialized as np.float64 kind
    """

    global PI, RAD_TO_DEG, DEG_TO_RAD, RADIAN, RADIUS, OMEGA, GRAV
    global SECONDS_PER_DAY, SECONDS_PER_HOUR, SECONDS_PER_MINUTE
    global RADGAS, RVGAS, HLV, HLS, KAPPA, CP_AIR, CP_VAPOR, CP_OCEAN
    global DENS_H20, RHOAIR, RHO0, RHO0R, RHO_CP, O2MIXRAT, WTMAIR, WTMH2O
    global WTMOZONE, WTMC, WTMCO2, WTMCH4, WTMO2, WTMCFC11, WTMCFC12, WTMN
    global DIFFAC, ES0, PSTD, PSTD_MKS, KELVIN, TFREEZE, C2DBARS, STEFAN, AVOGNO
    global VONKARM, ALOGMIN, EPSLN, RADCON, RADCON_MKS

    PI = get_constant_double(_lib, "PI")
    RAD_TO_DEG = get_constant_double(_lib, "RAD_TO_DEG")
    DEG_TO_RAD = get_constant_double(_lib, "DEG_TO_RAD")
    RADIAN = get_constant_double(_lib, "RADIAN")
    RADIUS = get_constant_double(_lib, "RADIUS")
    OMEGA = get_constant_double(_lib, "OMEGA")
    GRAV = get_constant_double(_lib, "GRAV")
    SECONDS_PER_DAY = get_constant_double(_lib, "SECONDS_PER_DAY")
    SECONDS_PER_HOUR = get_constant_double(_lib, "SECONDS_PER_HOUR")
    SECONDS_PER_MINUTE = get_constant_double(_lib, "SECONDS_PER_MINUTE")
    RADGAS = get_constant_double(_lib, "RDGAS")
    RVGAS = get_constant_double(_lib, "RVGAS")
    HLV = get_constant_double(_lib, "HLV")
    HLS = get_constant_double(_lib, "HLS")
    KAPPA = get_constant_double(_lib, "KAPPA")
    CP_AIR = get_constant_double(_lib, "CP_AIR")
    CP_VAPOR = get_constant_double(_lib, "CP_VAPOR")
    CP_OCEAN = get_constant_double(_lib, "CP_OCEAN")
    DENS_H20 = get_constant_double(_lib, "DENS_H20")
    RHOAIR = get_constant_double(_lib, "RHOAIR")
    RHO0 = get_constant_double(_lib, "RHO0")
    RHO0R = get_constant_double(_lib, "RHO0R")
    RHO_CP = get_constant_double(_lib, "RHO_CP")
    O2MIXRAT = get_constant_double(_lib, "O2MIXRAT")
    WTMAIR = get_constant_double(_lib, "WTMAIR")
    WTMH2O = get_constant_double(_lib, "WTMH2O")
    WTMOZONE = get_constant_double(_lib, "WTMOZONE")
    WTMC = get_constant_double(_lib, "WTMC")
    WTMCO2 = get_constant_double(_lib, "WTMCO2")
    WTMCH4 = get_constant_double(_lib, "WTMCH4")
    WTMO2 = get_constant_double(_lib, "WTMO2")
    WTMCFC11 = get_constant_double(_lib, "WTMCFC11")
    WTMCFC12 = get_constant_double(_lib, "WTMCFC12")
    WTMN = get_constant_double(_lib, "WTMN")
    DIFFAC = get_constant_double(_lib, "DIFFAC")
    ES0 = get_constant_double(_lib, "ES0")
    PSTD = get_constant_double(_lib, "PSTD")
    PSTD_MKS = get_constant_double(_lib, "PSTD_MKS")
    KELVIN = get_constant_double(_lib, "KELVIN")
    TFREEZE = get_constant_double(_lib, "TFREEZE")
    C2DBARS = get_constant_double(_lib, "C2DBARS")
    STEFAN = get_constant_double(_lib, "STEFAN")
    AVOGNO = get_constant_double(_lib, "AVOGNO")
    VONKARM = get_constant_double(_lib, "VONKARM")
    ALOGMIN = get_constant_double(_lib, "ALOGMIN")
    EPSLN = get_constant_double(_lib, "EPSLN")
    RADCON = get_constant_double(_lib, "RADCON")
    RADCON_MKS = get_constant_double(_lib, "RADCON_MKS")


def _init(libpath: str, lib: Any):

    """
    Sets _libpath and _lib module variables associated
    with the loaded cFMS library.  This function is
    to be used internally by the cfms module
    """

    global _libpath, _lib

    _lib = lib
    _libpath = libpath

    _init_constants()
