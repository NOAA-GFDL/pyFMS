from ctypes import CDLL, c_double

import numpy as np


_libpath: str = None
_lib: type[CDLL] = None

PI: np.float64 = None
RAD_TO_DEG: np.float64 = None
DEG_TO_RAD: np.float64 = None
RADIAN: np.float64 = None
RADIUS: np.float64 = None
OMEGA: np.float64 = None
GRAV: np.float64 = None
SECONDS_PER_DAY: np.float64 = None
SECONDS_PER_HOUR: np.float64 = None
SECONDS_PER_MINUTE: np.float64 = None
RADGAS: np.float64 = None
RVGAS: np.float64 = None
HLV: np.float64 = None
HLS: np.float64 = None
KAPPA: np.float64 = None
CP_AIR: np.float64 = None
CP_VAPOR: np.float64 = None
CP_OCEAN: np.float64 = None
DENS_H20: np.float64 = None
RHOAIR: np.float64 = None
RHO0: np.float64 = None
RHO0R: np.float64 = None
RHO_CP: np.float64 = None
O2MIXRAT: np.float64 = None
WTMAIR: np.float64 = None
WTMH2O: np.float64 = None
WTMOZONE: np.float64 = None
WTMC: np.float64 = None
WTMCO2: np.float64 = None
WTMCH4: np.float64 = None
WTMO2: np.float64 = None
WTMCFC11: np.float64 = None
WTMCFC12: np.float64 = None
WTMN: np.float64 = None
DIFFAC: np.float64 = None
ES0: np.float64 = None
PSTD: np.float64 = None
PSTD_MKS: np.float64 = None
KELVIN: np.float64 = None
TFREEZE: np.float64 = None
C2DBARS: np.float64 = None
STEFAN: np.float64 = None
AVOGNO: np.float64 = None
VONKARM: np.float64 = None
ALOGMIN: np.float64 = None
EPSLN: np.float64 = None
RADCON: np.float64 = None
RADCON_MKS: np.float64 = None


def setlib(libpath: str, lib: type[CDLL]):

    """
    Sets _libpath and _lib module variables associated
    with the loaded cFMS library.  This function is
    to be used internally by the cfms module
    """

    global _libpath, _lib

    _lib = lib
    _libpath = libpath


def constants_init():

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

    def get_constant(variable):
        return np.float64(c_double.in_dll(_lib, variable).value)

    PI = get_constant("PI")
    RAD_TO_DEG = get_constant("RAD_TO_DEG")
    DEG_TO_RAD = get_constant("DEG_TO_RAD")
    RADIAN = get_constant("RADIAN")
    RADIUS = get_constant("RADIUS")
    OMEGA = get_constant("OMEGA")
    GRAV = get_constant("GRAV")
    SECONDS_PER_DAY = get_constant("SECONDS_PER_DAY")
    SECONDS_PER_HOUR = get_constant("SECONDS_PER_HOUR")
    SECONDS_PER_MINUTE = get_constant("SECONDS_PER_MINUTE")
    RADGAS = get_constant("RDGAS")
    RVGAS = get_constant("RVGAS")
    HLV = get_constant("HLV")
    HLS = get_constant("HLS")
    KAPPA = get_constant("KAPPA")
    CP_AIR = get_constant("CP_AIR")
    CP_VAPOR = get_constant("CP_VAPOR")
    CP_OCEAN = get_constant("CP_OCEAN")
    DENS_H20 = get_constant("DENS_H20")
    RHOAIR = get_constant("RHOAIR")
    RHO0 = get_constant("RHO0")
    RHO0R = get_constant("RHO0R")
    RHO_CP = get_constant("RHO_CP")
    O2MIXRAT = get_constant("O2MIXRAT")
    WTMAIR = get_constant("WTMAIR")
    WTMH2O = get_constant("WTMH2O")
    WTMOZONE = get_constant("WTMOZONE")
    WTMC = get_constant("WTMC")
    WTMCO2 = get_constant("WTMCO2")
    WTMCH4 = get_constant("WTMCH4")
    WTMO2 = get_constant("WTMO2")
    WTMCFC11 = get_constant("WTMCFC11")
    WTMCFC12 = get_constant("WTMCFC12")
    WTMN = get_constant("WTMN")
    DIFFAC = get_constant("DIFFAC")
    ES0 = get_constant("ES0")
    PSTD = get_constant("PSTD")
    PSTD_MKS = get_constant("PSTD_MKS")
    KELVIN = get_constant("KELVIN")
    TFREEZE = get_constant("TFREEZE")
    C2DBARS = get_constant("C2DBARS")
    STEFAN = get_constant("STEFAN")
    AVOGNO = get_constant("AVOGNO")
    VONKARM = get_constant("VONKARM")
    ALOGMIN = get_constant("ALOGMIN")
    EPSLN = get_constant("EPSLN")
    RADCON = get_constant("RADCON")
    RADCON_MKS = get_constant("RADCON_MKS")
