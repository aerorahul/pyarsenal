#!/usr/bin/env python

###############################################################
# < next few lines under version control, D O  N O T  E D I T >
# $Date$
# $Revision$
# $Author$
# $Id$
###############################################################

'''
meteor.py contains commonly used meteorological related functions
At some point, one should start using Unidata MetPy module instead
'''

import numpy as _np

__author__ = "Rahul Mahajan"
__email__ = "rahul.mahajan@nasa.gov"
__copyright__ = "Copyright 2016, NOAA / NCEP / EMC"
__license__ = "GPL"
__status__ = "Prototype"
__version__ = "0.1"

__all__ = ['atmos_const', 'meteor']


class atmos_const(object):

    def __init__(self):
        ''' Initialize commonly used atmospheric constants '''
        # Ideal gas constant for dry air
        self.Rd = 287.06
        # Ideal gas constant for moist air
        self.Rv = 461.6
        # Heat capacity of air at constant pressure (J/kg/K)
        self.Cp = 1004.67
        # Heat capacity of air at constant volume (J/kg/K)
        self.Cv = self.Cp - self.Rd
        # Latent heat of vaporization of water (J/kg)
        self.L = 2.26e6
        self.kappa = self.Rd / self.Cp
        # Heat capacity ratio
        self.gamma = self.Cp / self.Cv
        # Acceleration due to gravity (m/s2)
        self.g = 9.81
        # Base temperature for standard atmosphere
        self.Talt = 288.15
        # Freezing point of water (K)
        self.Tfrez = 273.15
        # Reference pressure (hPa)
        self.Pr = 1000.0
        # Base pressure for standard atmosphere (Pa)
        self.Po = 101325.0
        # Saturation vapor pressure at freezing (hPa)
        self.eo = 6.112
        # Standard lapse rate in (K/m)
        self.lapsesta = 6.5 / 1000.0

        # Seconds per day (secs)
        self.secsperday = 24 * 60 * 60
        # Degrees to Radians
        self.deg2rad = _np.pi / 180.0
        # Radians to Degrees
        self.rad2deg = 180.0 / _np.pi

        # Solar constant (W/m2)
        self.solar_const = 1368.0
        # Radius of Earth (m)
        self.R_earth = 6370000.0
        # Rotation rate of the Earth (/s)
        self.omega_earth = (2.0 * _np.pi) / self.secsperday


class meteor(object):
    '''
    Define a class that contains most commonly used meteorological functions
    '''

    def __init__(self):
        self.atmos_const = atmos_const()
        pass

    def altimeter(self, pin, hin):
        ''' altimeter given pressure and altitude '''

        pexp = (self.atmos_const.Rd * self.atmos_const.lapseta) / \
            self.atmos_const.g
        invpexp = 1.0 / pexp
        alt = pin * (1.0 + ((self.atmos_const.Po / pin) ** pexp) *
                     (self.atmos_const.lapsesta * hin / self.atmos_const.Talt)) ** invpexp

        return alt

    def alt_to_psfc(self, alt, hin):
        ''' reduce the altitude to surface pressure '''

        pexp = (self.atmos_const.Rd * self.atmos_const.lapseta) / \
            self.atmos_const.g
        invpexp = 1.0 / pexp
        psfc = (alt ** pexp -
                (self.atmos_const.Po ** pexp) *
                (self.atmos_const.lapsesta *
                 hin /
                 self.atmos_const.Talt)) ** invpexp

        return psfc

    def clausius_clapeyron(self, tin):
        ''' saturated vapor pressure or Clausius-Clapeyron '''

        esat = self.atmos_const.eo * \
            _np.exp((self.atmos_const.L / self.atmos_const.Rv)
                    * (1.0 / self.atmos_const.Tfrez - 1.0 / tin))

        return esat

    def sat_vapor_pressure(self, tin):
        ''' saturated vapor pressure '''

        esat = self.clausius_clapeyron(tin)

        return esat

    def sat_mixrat(self, es, pin):
        ''' saturated mixing ratio '''

        ws = 0.622 * (es / (pin - es))

        return ws

    def mixrat_to_tdew(self, qvap, pres):
        ''' mixing ratio to dew-point temperature '''

        evap = qvap * pres * self.atmos_const.Rv / self.atmos_const.Rd
        tdew = 1.0 / ((1.0 / self.atmos_const.Tfrez) - (self.atmos_const.Rv /
                                                        self.atmos_const.L) * _np.emath.log(evap / self.atmos_const.eo))

        return tdew

    def dry_static_energy(self, tin, zin):
        ''' dry static energy '''

        dse = self.atmos_const.Cp * tin + self.atmos_const.g * zin

        return dse

    def moist_static_energy(self, tin, zin, qin):
        ''' moist static energy '''

        mse = self.dry_static_energy(tin, zin) + self.atmos_const.L * qin

        return mse

    def earth_dist(self, xlat1, xlon1, xlat2, xlon2):
        ''' distance between two points on a sphere (Earth) '''

        pid = _np.pi / 180.0
        e_dist = self.atmos_const.R_earth * _np.arccos(_np.sin(xlat1 * pid) * _np.sin(
            xlat2 * pid) + _np.cos(xlat1 * pid) * _np.cos(xlat2 * pid) * _np.cos((xlon2 - xlon1) * pid))

        return e_dist

    def advection(self, uwnd, vwnd, fld, dx, dy, mfac=None):
        ''' simple advection of a field '''

        dfdx, dfdy = self.gradient_2d(fld, dx, dy, mfac=mfac)
        adv = -(uwnd * dfdx) - (vwnd * dfdy)

        return adv

    def gradient_2d(self, indat, x, y, mfac=None):
        ''' horizontal gradient of a field '''

        if (mfac is None):
            gradx = self.ddx(indat, x)
            grady = self.ddy(indat, y)
        else:
            gradx = self.ddx(indat, x / mfac)
            grady = self.ddy(indat, y / mfac)

        return (gradx, grady)

    def ddx(self, fldin, xin):
        ''' d(field) / dx '''

        iy, ix = _np.shape(fldin)
        xpt = _np.arange(1, ix - 1)
        fldout = _np.zeros((iy, ix))

        fldout[:, xpt] = (fldin[:, xpt + 1] - fldin[:, xpt - 1]) / \
            (xin[:, xpt + 1] - xin[:, xpt - 1])
        fldout[:,  0] = (fldin[:,    1] - fldin[:,    0]) / \
            (xin[:, 1] - xin[:, 0])
        fldout[:, -1] = (fldin[:,   -1] - fldin[:,   -2]) / \
            (xin[:, -1] - xin[:, -2])

        return fldout

    def ddy(self, fldin, yin):
        ''' d(field) / dy '''

        iy, ix = _np.shape(fldin)
        ypt = _np.arange(1, iy - 1)
        fldout = _np.zeros((iy, ix))

        fldout[ypt, :] = (fldin[ypt + 1, :] - fldin[ypt - 1, :]
                          ) / (yin[ypt + 1, :] - yin[ypt - 1, :])
        fldout[0, :] = (fldin[1, :] - fldin[0, :]) / (yin[1, :] - yin[0, :])
        fldout[-1, :] = (fldin[-1, :] - fldin[-2, :]) / \
            (yin[-1, :] - yin[-2, :])

        return fldout

    def ddp(self, fldin, presin):
        ''' d(field) / dpressure '''

        iz, iy, ix = _np.shape(fldin)
        zpt = _np.arange(1, iz - 1)
        fldout = _np.zeros((iz, iy, ix))

        fldout[zpt, :, :] = (fldin[zpt + 1, :, :] - fldin[zpt - 1, :, :]) / \
            (presin[zpt + 1, :, :] - presin[zpt - 1, :, :])
        fldout[0, :, :] = (fldin[1, :, :] - fldin[0, :, :]) / \
            (presin[1, :, :] - presin[0, :, :])
        fldout[-1, :, :] = (fldin[-1, :, :] - fldin[-2, :, :]) / \
            (presin[-1, :, :] - presin[-2, :, :])

        return fldout
