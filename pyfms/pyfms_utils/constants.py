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

    def __init__(self, cFMS: ctypes.CDLL = None):
        self.cFMS = cFMS
        self.PI = self.get_constant("PI")
        self.RAD_TO_DEG = self.get_constant("RAD_TO_DEG")
        self.DEG_TO_RAD = self.get_constant("DEG_TO_RAD")
        self.RADIAN = self.get_constant("RADIAN")
        self.RADIUS = self.get_constant("RADIUS")
        self.OMEGA = self.get_constant("OMEGA")
        self.GRAV = self.get_constant("GRAV")
        self.SECONDS_PER_DAY = self.get_constant("SECONDS_PER_DAY")
        self.SECONDS_PER_HOUR = self.get_constant("SECONDS_PER_HOUR")
        self.SECONDS_PER_MINUTE = self.get_constant("SECONDS_PER_MINUTE")
        self.RADGAS = self.get_constant("RDGAS")
        self.RVGAS = self.get_constant("RVGAS")
        self.HLV = self.get_constant("HLV")
        self.HLS = self.get_constant("HLS")
        self.KAPPA = self.get_constant("KAPPA")
        self.CP_AIR = self.get_constant("CP_AIR")
        self.CP_VAPOR = self.get_constant("CP_VAPOR")
        self.CP_OCEAN = self.get_constant("CP_OCEAN")
        self.DENS_H20 = self.get_constant("DENS_H20")
        self.RHOAIR = self.get_constant("RHOAIR")
        self.RHO0 = self.get_constant("RHO0")
        self.RHO0R = self.get_constant("RHO0R")
        self.RHO_CP = self.get_constant("RHO_CP")
        self.O2MIXRAT = self.get_constant("O2MIXRAT")
        self.WTMAIR = self.get_constant("WTMAIR")
        self.WTMH2O = self.get_constant("WTMH2O")
        self.WTMOZONE = self.get_constant("WTMOZONE")
        self.WTMC = self.get_constant("WTMC")
        self.WTMCO2 = self.get_constant("WTMCO2")
        self.WTMCH4 = self.get_constant("WTMCH4")
        self.WTMO2 = self.get_constant("WTMO2")
        self.WTMCFC11 = self.get_constant("WTMCFC11")
        self.WTMCFC12 = self.get_constant("WTMCFC12")
        self.WTMN = self.get_constant("WTMN")
        self.DIFFAC = self.get_constant("DIFFAC")
        self.ES0 = self.get_constant("ES0")
        self.PSTD = self.get_constant("PSTD")
        self.PSTD_MKS = self.get_constant("PSTD_MKS")
        self.KELVIN = self.get_constant("KELVIN")
        self.TFREEZE = self.get_constant("TFREEZE")
        self.C2DBARS = self.get_constant("C2DBARS")
        self.STEFAN = self.get_constant("STEFAN")
        self.AVOGNO = self.get_constant("AVOGNO")
        self.VONKARM = self.get_constant("VONKARM")
        self.ALOGMIN = self.get_constant("ALOGMIN")
        self.EPSLN = self.get_constant("EPSLN")
        self.RADCON = self.get_constant("RADCON")
        self.RADCON_MKS = self.get_constant("RADCON_MKS")

    def get_constant(self, variable):
        return np.float64(ctypes.c_double.in_dll(self.cFMS, variable).value)
