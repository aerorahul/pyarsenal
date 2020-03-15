# coding: utf-8 -*-

'''
WRF.py contains WRF related functions:
    wrf_proj(filename)
    proj_set(proj)
    latlon_to_ij(lat,lon,proj)
    ij_to_latlon(i,j,proj)
'''

__all__ = ['ddx', 'ddy', 'vorticity',
           'wrf_proj', 'proj_set',
           'ij_to_latlon', 'latlon_to_ij',
           'find_max_value', 'find_min_value', 'find_min_max']

import math as _math
import numpy as _np
from netCDF4 import Dataset as _Dataset

pid = _math.pi / 180.0
R_earth = 6370.0 * 1.0e3


def ddx(fldin, dx=1):
    # _np.shape(fldin) == [ny,nx]
    return _np.gradient(fldin)[-1] / dx


def ddy(fldin, dy=1):
    # _np.shape(fldin) == [ny,nx]
    return _np.gradient(fldin)[-2] / dy


def vorticity(u, v, dx, dy, mfac):
    # _np.shape(u)    == [ny,nx]
    # _np.shape(v)    == [ny,nx]
    # _np.shape(dx)   == scalar
    # _np.shape(dy)   == scalar
    # _np.shape(mfac) == [ny,nx]
    return (ddx(v, dx=dx) - ddy(u, dy=dy)) / mfac


def wrf_proj(filename):

    proj = type('WRF_PROJECTION', (), {})

    nc = _Dataset(filename, 'r')

    proj.code = int(nc.MAP_PROJ)
    proj.nx = len(nc.dimensions['west_east'])
    proj.ny = len(nc.dimensions['south_north'])
    if ('bottom_top' in nc.dimensions):
        proj.nz = len(nc.dimensions['bottom_top'])
    proj.dx = float(nc.DX)
    proj.dy = float(nc.DY)
    proj.cenlat = float(nc.CEN_LAT)
    proj.cenlon = float(nc.CEN_LON)
    proj.stdlat1 = float(nc.TRUELAT1)
    proj.stdlat2 = float(nc.TRUELAT2)
    proj.stdlon = float(nc.STAND_LON)

    if 'XLAT' in nc.variables:
        proj.xlat = _np.squeeze(nc.variables["XLAT"][:])
        tmp = _np.squeeze(nc.variables["XLONG"][:])
        proj.xlon = (tmp < 0.0) * 360.0 + tmp
    elif 'XLAT_M' in nc.variables:
        proj.xlat = _np.squeeze(nc.variables["XLAT_M"][:])
        tmp = _np.squeeze(nc.variables["XLONG_M"][:])
        proj.xlon = (tmp < 0.0) * 360.0 + tmp

    proj.lat1 = proj.xlat[0, 0]
    proj.lon1 = proj.xlon[0, 0]

    nc.close()

    if (proj.code == 1):
        proj.projection = 'lcc'
        proj.lat_0 = proj.cenlat
        proj.lon_0 = proj.cenlon
        proj.lat_1 = proj.stdlat1
        proj.lat_2 = proj.stdlat2
        proj.width = proj.dx * proj.nx
        proj.height = proj.dy * proj.ny

    elif (proj.code == 3):
        proj.projection = 'merc'
        proj.llcrnrlon = _np.min(proj.xlon) - 0.1
        proj.llcrnrlat = _np.min(proj.xlat) - 0.1
        proj.urcrnrlon = _np.max(proj.xlon) + 0.1
        proj.urcrnrlat = _np.max(proj.xlat) + 0.1

    else:
        str = 'Error message from : wrf_proj\n' + \
            '   wrf_proj is unable to handle projection code "%d"\n' % (proj.code) +\
            '   valid options are: \n' +\
            '   1 | 3 for lcc | merc'
        raise Exception(str)

    proj.resolution = 'i'
    proj.meridians = _np.arange(-180, 180, 30)
    proj.meridians_labels = [0, 0, 0, 1]
    proj.parallels = _np.arange(-90, 90, 15)
    proj.parallels_labels = [0, 1, 0, 0]
    proj.box_lat = _np.concatenate((proj.xlat[0, :],
                                    _np.transpose(proj.xlat[:, -1]),
                                    _np.flipud(proj.xlat[-1, :]),
                                    _np.flipud(proj.xlat[:, 0])), axis=0)
    proj.box_lon = _np.concatenate((proj.xlon[0, :],
                                    _np.transpose(proj.xlon[:, -1]),
                                    _np.flipud(proj.xlon[-1, :]),
                                    _np.flipud(proj.xlon[:, 0])), axis=0)

    proj = proj_set(proj)

    return proj


def proj_set(proj):
    # translated from proj_set.m
    # proj.code == 1 is tested, rest are not

    if (proj.stdlat1 < 0.0):
        proj.hemi = -1
    else:
        proj.hemi = 1

    proj.rebydx = R_earth / proj.dx

    if (proj.code == 0):  # latitude longitude

        if (proj.lon1 < 0.0):
            proj.lon1 = proj.lon1 + 360.0

    elif (proj.code == 1):  # lambert conformal

        stdlat1 = _np.min((proj.stdlat1, proj.stdlat2))
        stdlat2 = _np.max((proj.stdlat1, proj.stdlat2))
        proj.stdlat1 = _np.min((stdlat1, stdlat2))
        proj.stdlat2 = _np.max((stdlat1, stdlat2))

        if (_np.abs(proj.stdlat1 - proj.stdlat2) > 0.1):
            proj.cone = (_math.log(_math.cos(stdlat1 * pid)) - _math.log(_math.cos(stdlat2 * pid))) / (
                _math.log(_math.tan((90.0 - _np.abs(stdlat1)) * pid * 0.5)) -
                _math.log(_math.tan((90.0 - _np.abs(stdlat2)) * pid * 0.5)))
        else:
            proj.cone = _math.sin(_np.abs(stdlat1) * pid)

        dlon1 = proj.lon1 - proj.stdlon
        if (dlon1 > 180.0):
            dlon1 = dlon - 360.0
        if (dlon1 < -180.0):
            dlon1 = dlon + 360.0

        tl1r = _math.cos(proj.stdlat1 * pid)
        proj.rsw = proj.rebydx * (tl1r / proj.cone) * (
            _math.tan((90.0 * proj.hemi - proj.lat1) * pid / 2) /
            _math.tan((90.0 * proj.hemi - proj.stdlat1) * pid / 2)) ** (proj.cone)

        argmnt = proj.cone * (dlon1 * pid)
        proj.polei = 1.0 - proj.hemi * proj.rsw * _math.sin(argmnt)
        proj.polej = 1.0 + proj.rsw * _math.cos(argmnt)

    elif (proj.code == 2):  # polar stereographic

        reflon = proj.stdlon + 90.0
        proj.cone = 1.0

        s_top = 1.0 + proj.hemi * _math.sin(proj.stdlat1 * pid)
        ala1 = proj.lat1 * pid
        proj.rsw = proj.rebydx * \
            _math.cos(ala1) * s_top / (1.0 + proj.hemi * _math.sin(ala1))

        alo1 = (proj.lon1 - reflon) * pid
        proj.polei = 1.0 - proj.rsw * _math.cos(alo1)
        proj.polej = 1.0 - proj.hemi * proj.rsw * _math.sin(alo1)

    elif (proj.code == 3):  # mercator

        clain = _math.cos(proj.stdlat1 * pid)
        proj.dlon = proj.dx / (R_earth * clain)

        proj.rsw = 0.0
        if (proj.lat1 != 0.0):
            proj.rsw = (_math.log(
                _math.tan(0.5 * ((proj.lat1 + 90.0) * pid)))) / proj.dlon

    else:
        raise Exception('unknown proj.code for proj_set')

    return proj


def latlon_to_ij(lat, lon, proj):
    # translated from latlon_to_ij.m
    # proj.code == 1 is tested, rest are not

    if (proj.code == 0):  # latitude-longitude grid

        if (lon < 0.0):
            lon360 = lon + 360.0
        else:
            lon360 = lon.copy()

        deltalon = lon360 - proj.lon1
        deltalat = lat - proj.lat1
        ir = deltalon / proj.dx + 1.0
        jr = deltalat / proj.dy + 1.0

    elif (proj.code == 1):  # lambert conformal

        dlon = lon - proj.stdlon
        if (dlon > 180.0):
            dlon = dlon - 360.0
        if (dlon < -180.0):
            dlon = dlon + 360.0

        tl1r = _math.cos(proj.stdlat1 * pid)

        rm = proj.rebydx * tl1r / proj.cone * (
            _math.tan((90.0 * proj.hemi - lat) * pid / 2.0) /
            _math.tan((90.0 * proj.hemi - proj.stdlat1) * pid / 2.0)
        ) ** proj.cone

        argmnt = proj.cone * dlon * pid
        ir = proj.polei + proj.hemi * rm * _math.sin(argmnt)
        jr = proj.polej - rm * _math.cos(argmnt)

        if (proj.hemi == -1):
            ir = 2.0 - ir
            jr = 2.0 - jr

    elif (proj.code == 2):  # polar stereographic

        reflon = proj.stdlon + 90.0
        s_top = 1.0 + proj.hemi * _math.sin(proj.stdlat1 * pid)
        ala = lat * pid
        rm = proj.rebydx * _math.cos(ala) * s_top / \
            (1.0 + proj.hemi * _math.sin(ala))
        alo = (lon - reflon) * pid
        ir = proj.polei + rm * _math.cos(alo)
        jr = proj.polej + proj.hemi * rm * _math.sin(alo)

    elif (proj.code == 3):  # mercator

        dlon = lon - proj.lon1
        if (dlon > 180.0):
            dlon = dlon - 360.0
        if (dlon < -180.0):
            dlon = dlon + 360.0
        ir = 1.0 + (dlon / (proj.dlon / pid))
        jr = 1.0 + (_math.log(_math.tan(0.5 * ((lat + 90.0) * pid)))
                    ) / proj.dlon - proj.rsw

    else:
        raise Exception('unknown proj.code for proj_set')

    # acknowledge the fact that in python indexing starts at 0
    ir = int(_np.round(ir)) - 1
    # acknowledge the fact that in python indexing starts at 0
    jr = int(_np.round(jr)) - 1

    return [ir, jr]


def ij_to_latlon(i, j, proj):
    # translated from ij_to_latlon.m
    # proj.code == 1 is tested, rest are not

    i = i + 1  # acknowledge the fact that in python indexing starts at 0
    j = j + 1  # acknowledge the fact that in python indexing starts at 0

    if (proj.code == 0):  # latitude-longitude grid
        raise Exception('latitude-longitude is not set, yet')

    elif (proj.code == 1):  # lambert conformal

        chi1 = (90.0 - proj.hemi * proj.stdlat1) * pid
        chi2 = (90.0 - proj.hemi * proj.stdlat2) * pid

        if (proj.hemi == -1):
            inew = -i + 2.0
            jnew = -j + 2.0
        else:
            inew = i + 0.0
            jnew = j + 0.0

        xx = inew - proj.polei
        yy = proj.polej - jnew
        r2 = xx**2 + yy**2
        r = _np.sqrt(r2) / proj.rebydx

        if (r2 == 0.0):
            lat = proj.hemi * 90.0
            lon = proj.stdlon
        else:
            lon = proj.stdlon + \
                _math.atan2(proj.hemi * xx, yy) / proj.cone / pid
            lon = _np.mod(lon + 360.0, 360.0)

            if (chi1 == chi2):
                chi = 2.0 * \
                    _math.atan(((r / _math.tan(chi1)) ** (1.0 / proj.cone)) * _math.tan(chi1 * 0.5))
            else:
                chi = 2.0 * _math.atan(((r * proj.cone / _math.sin(chi1))
                                        ** (1.0 / proj.cone)) * _math.tan(chi1 * 0.5))

            lat = (90.0 - chi / pid) * proj.hemi

        if (lon > 180.0):
            lon = lon - 360.0
        if (lon < -180.0):
            lon = lon + 360.0

    elif (proj.code == 2):  # polar stereographic

        reflon = proj.stdlon + 90.0
        scale_top = 1.0 + proj.hemi + _math.sin(proj.truelat1 * pid)

        xx = i - proj.polei
        yy = (j - proj.polej) * proj.hemi
        r2 = xx**2 + yy**2

        if (r2 == 0.0):
            lat = proj.hemi * 90.0
            lon = reflon
        else:
            gi2 = (proj.rebydx * scale_top) ** 2.0
            lat = proj.hemi * _math.asin((gi2 - r2) / (gi2 + r2)) / pid
            arccos = _math.acos(xx / _np.sqrt(r2))
            if (yy > 0.0):
                lon = reflon + arccos / pid
            else:
                lon = reflon - arccos / pid

        if (lon > 180.0):
            lon = lon - 360.0
        if (lon < -180.0):
            lon = lon + 360.0

    elif (proj.code == 3):  # mercator

        lat = 2.0 * _math.atan(_math.exp(proj.dlon *
                                         (proj.rsw + j - 1.0))) / pid - 90.0
        lon = (i - 1.0) * proj.dlon / pid + proj.lon1
        if (lon > 180.0):
            lon = lon - 360.0
        if (lon < -180.0):
            lon = lon + 360.0

    else:
        raise Exception('unknown proj.code')

    return [lon, lat]


def find_min_value(fldin, glat, glon, proj, radius=10):

    [ir, jr] = latlon_to_ij(glat, glon, proj)
    xrange = _np.arange(_np.max((ir - radius, 0)),
                        _np.min((ir + radius, proj.nx)), 1)
    yrange = _np.arange(_np.max((jr - radius, 0)),
                        _np.min((jr + radius, proj.ny)), 1)

    minval = 1.0e36
    for y in yrange:
        for x in xrange:
            if (fldin[y, x] < minval):
                iout = x
                jout = y
                minval = fldin[y, x]

    return [iout, jout, minval]


def find_max_value(fldin, glat, glon, proj, radius=10):

    [ir, jr] = latlon_to_ij(glat, glon, proj)
    xrange = _np.arange(_np.max((ir - radius, 0)),
                        _np.min((ir + radius, proj.nx)), 1)
    yrange = _np.arange(_np.max((jr - radius, 0)),
                        _np.min((jr + radius, proj.ny)), 1)

    maxval = -1.0e36
    for y in yrange:
        for x in xrange:
            if (fldin[y, x] > maxval):
                iout = x
                jout = y
                maxval = fldin[y, x]

    return [iout, jout, maxval]


def find_min_max(fldin, glat, glon, proj, radius=10, minima=True):

    if (minima):
        [iout, jout, val] = find_min_value(
            fldin, glat, glon, proj, radius=radius)
    else:
        [iout, jout, val] = find_max_value(
            fldin, glat, glon, proj, radius=radius)

    return [iout, jout, val]
