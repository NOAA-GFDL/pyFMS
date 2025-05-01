import ctypes

import numpy as np


class constants:

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

    __libpath: str = None
    __lib: type[ctypes.CDLL] = None

    @classmethod
    def setlib(cls, libpath: str, lib: type[ctypes.CDLL]):
        cls.__libpath = libpath
        cls.__lib = lib

    @classmethod
    def lib(cls):
        return cls.__lib

    @classmethod
    def libpath(cls) -> str:
        return cls.__libpath

    @classmethod
    def init(cls):
        def get_constant(variable):
            return np.float64(ctypes.c_double.in_dll(cls.lib(), variable).value)

        cls.PI = get_constant("PI")
        cls.RAD_TO_DEG = get_constant("RAD_TO_DEG")
        cls.DEG_TO_RAD = get_constant("DEG_TO_RAD")
        cls.RADIAN = get_constant("RADIAN")
        cls.RADIUS = get_constant("RADIUS")
        cls.OMEGA = get_constant("OMEGA")
        cls.GRAV = get_constant("GRAV")
        cls.SECONDS_PER_DAY = get_constant("SECONDS_PER_DAY")
        cls.SECONDS_PER_HOUR = get_constant("SECONDS_PER_HOUR")
        cls.SECONDS_PER_MINUTE = get_constant("SECONDS_PER_MINUTE")
        cls.RADGAS = get_constant("RDGAS")
        cls.RVGAS = get_constant("RVGAS")
        cls.HLV = get_constant("HLV")
        cls.HLS = get_constant("HLS")
        cls.KAPPA = get_constant("KAPPA")
        cls.CP_AIR = get_constant("CP_AIR")
        cls.CP_VAPOR = get_constant("CP_VAPOR")
        cls.CP_OCEAN = get_constant("CP_OCEAN")
        cls.DENS_H20 = get_constant("DENS_H20")
        cls.RHOAIR = get_constant("RHOAIR")
        cls.RHO0 = get_constant("RHO0")
        cls.RHO0R = get_constant("RHO0R")
        cls.RHO_CP = get_constant("RHO_CP")
        cls.O2MIXRAT = get_constant("O2MIXRAT")
        cls.WTMAIR = get_constant("WTMAIR")
        cls.WTMH2O = get_constant("WTMH2O")
        cls.WTMOZONE = get_constant("WTMOZONE")
        cls.WTMC = get_constant("WTMC")
        cls.WTMCO2 = get_constant("WTMCO2")
        cls.WTMCH4 = get_constant("WTMCH4")
        cls.WTMO2 = get_constant("WTMO2")
        cls.WTMCFC11 = get_constant("WTMCFC11")
        cls.WTMCFC12 = get_constant("WTMCFC12")
        cls.WTMN = get_constant("WTMN")
        cls.DIFFAC = get_constant("DIFFAC")
        cls.ES0 = get_constant("ES0")
        cls.PSTD = get_constant("PSTD")
        cls.PSTD_MKS = get_constant("PSTD_MKS")
        cls.KELVIN = get_constant("KELVIN")
        cls.TFREEZE = get_constant("TFREEZE")
        cls.C2DBARS = get_constant("C2DBARS")
        cls.STEFAN = get_constant("STEFAN")
        cls.AVOGNO = get_constant("AVOGNO")
        cls.VONKARM = get_constant("VONKARM")
        cls.ALOGMIN = get_constant("ALOGMIN")
        cls.EPSLN = get_constant("EPSLN")
        cls.RADCON = get_constant("RADCON")
        cls.RADCON_MKS = get_constant("RADCON_MKS")
