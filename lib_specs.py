#!/usr/bin/env python

'''
lib_specs.py contains region and variable specifications
'''

import numpy as _np

__all__ = ['region_specs', 'var_specs', 'field_specs']


class _Container(object):
    '''
    Define an empty container class
    '''

    def __init__(self):
        '''
        Create an empty container class
        '''
        pass


def region_specs(region='global'):
    '''
    region_specs(region='global')
    '''
    region = region.lower()
    if region in ['nh', 'nhemp']:
        regionName = 'Northern Hemisphere'
    elif region in ['tr', 'tropics']:
        regionName = 'Tropics'
    elif region in ['sh', 'shemp']:
        regionName = 'Southern Hemisphere'
    elif region in ['gl', 'global']:
        regionName = 'Global'
    else:
        raise RuntimeError('region_specs: unknown region, %s' % region)
    return regionName


def var_specs(var='temp'):
    '''
    var_specs(var='temp')
    '''
    var = var.lower()
    if var in ['uwind']:
        var_sname = 'u'
        var_unit = 'm/s'
        var_name = 'U Wind'
    elif var in ['vwind']:
        var_sname = 'v'
        var_unit = 'm/s'
        var_name = 'V Wind'
    elif var in ['wind']:
        var_sname = 'wind'
        var_unit = 'K'
        var_name = 'Vector Wind'
    elif var in ['temp']:
        var_sname = 't'
        var_unit = 'K'
        var_name = 'Temp.'
    elif var in ['q']:
        var_sname = 'q'
        var_unit = 'g/kg'
        var_name = 'Sp. Hum.'
    elif var in ['cw', 'cwmr']:
        var_sname = 'cw'
        var_unit = 'g/kg'
        var_name = 'Cloud Water'
    elif var in ['rh']:
        var_sname = 'rh'
        var_unit = '%'
        var_name = 'Rel. Hum.'
    else:
        raise InputError('var_specs: unknown variable, %s' % var)
    return var_name, var_sname, var_unit


def field_specs(vnam):
    '''
    field_specs.py creates a structure with specific
    parameters for a desired field
    vnam   - name of field to get structure for
    strout - output structure that contains parameters
    '''

    strout = _Container()
    strout.vnam = vnam

    if vnam == 'EMPTY':
        strout.name = 'empty name'
        strout.name_short = 'empty'
        strout.level = 'unknown level'
        strout.cntrs = _np.arange(0.0, 1.1, 0.1)
        strout.clab = strout.cntrs[::4]
        strout.inc = _np.arange(0.0, 1.1, 0.1)
        strout.ilab = strout.inc[::4]
        strout.spr = _np.arange(0.0, 1.1, 0.1)
        strout.slab = strout.spr[::4]
        strout.units = ''
        strout.lev_int = '-999999'

    elif (vnam in ['SLP']):
        strout.name = 'sea-level pressure'
        strout.name_short = 'slp'
        strout.level = 'surface'
        strout.cntrs = _np.arange(900, 1041, 4)
        strout.clab = strout.cntrs[::4]
        strout.inc = _np.arange(0.0, 4.25, 0.25)
        strout.ilab = strout.inc[::4]
        strout.spr = _np.arange(0.0, 4.25, 0.25)
        strout.slab = strout.spr[::4]
        strout.smax = 10.0
        strout.units = '$hPa$'
        strout.lev_int = -1

    elif (vnam in ['ALT']):
        strout.name = 'altimeter'
        strout.name_short = 'alt'
        strout.level = 'surface'
        strout.cntrs = _np.arange(900, 1051, 4)
        strout.clab = strout.cntrs[::4]
        strout.inc = _np.arange(0.0, 11.0, 1.0)
        strout.ilab = strout.inc[::4]
        strout.spr = _np.arange(0.0, 11.0, 1.0)
        strout.slab = strout.spr[::4]
        strout.units = '$hPa$'
        strout.lev_int = -1

    elif (vnam in ['T2']):
        strout.name = 'temperature'
        strout.name_short = 'temp_2m'
        strout.level = '2 meters'
        strout.cntrs = _np.arange(-60, 51, 2)
        strout.clab = strout.cntrs[::4]
        strout.inc = _np.arange(0.0, 3.25, 0.25)
        strout.ilab = strout.inc[::4]
        strout.spr = _np.arange(0.0, 3.25, 0.25)
        strout.slab = strout.spr[::4]
        strout.units = '$K$'
        strout.lev_int = -1

    elif (vnam in ['Q2']):
        strout.name = 'moisture'
        strout.name_short = 'sphu_2m'
        strout.level = '2 meters'
        strout.cntrs = _np.arange(-60, 51, 3)
        strout.clab = strout.cntrs[::4]
        strout.inc = _np.arange(0.0, 5.5, 0.5)
        strout.ilab = strout.inc[::4]
        strout.spr = _np.arange(0.0, 5.5, 0.5)
        strout.slab = strout.spr[::4]
        strout.units = '$K$'
        strout.lev_int = -1

    elif (vnam in ['U10', 'V10']):
        strout.name = '%s-wind' % vnam[0].lower()
        strout.name_short = 'wnd'
        strout.level = '10 m'
        strout.cntrs = _np.arange(-80, 81, 5)
        strout.clab = strout.cntrs[::4]
        strout.inc = _np.arange(0.0, 11.0, 1.0)
        strout.ilab = strout.inc[::4]
        strout.spr = _np.arange(0.0, 11.0, 1.0)
        strout.slab = strout.spr[::4]
        strout.units = '$ms^{-1}$'
        strout.lev_int = -1

    elif (vnam in ['Y10']):
        strout.name = 'wind'
        strout.name_short = 'wnd'
        strout.level = '10 m'
        strout.cntrs = _np.arange(0, 81, 2)
        strout.clab = strout.cntrs[::4]
        strout.inc = _np.arange(0.0, 11.0, 1.0)
        strout.ilab = strout.inc[::4]
        strout.spr = _np.arange(0.0, 11.0, 1.0)
        strout.slab = strout.spr[::4]
        strout.units = '$ms^{-1}$'
        strout.lev_int = -1

    elif (vnam in ['H925', 'H850', 'H800', 'H700', 'H600', 'H500', 'H300']):
        strout.name = 'height'
        strout.name_short = 'hght'
        strout.level = '%s hPa' % vnam[1:]
        strout.inc = _np.arange(0.0, 41.0, 2.0)
        strout.ilab = strout.inc[::2]
        strout.spr = _np.arange(0.0, 41.0, 2.0)
        strout.slab = strout.spr[::2]
        strout.units = '$m$'
        strout.lev_int = int(vnam[1:])
        if (strout.lev_int == 925):
            strout.cntrs = _np.arange(400, 2001, 50)
            strout.clab = strout.cntrs[::4]
        elif (strout.lev_int == 850):
            strout.cntrs = _np.arange(600, 2501, 50)
            strout.clab = strout.cntrs[::4]
        elif (strout.lev_int == 800):
            strout.cntrs = _np.arange(800, 2801, 50)
            strout.clab = strout.cntrs[::4]
        elif (strout.lev_int == 700):
            strout.cntrs = _np.arange(2500, 3501, 50)
            strout.clab = strout.cntrs[::4]
        elif (strout.lev_int == 600):
            strout.cntrs = _np.arange(3000, 4501, 50)
            strout.clab = strout.cntrs[::4]
        elif (strout.lev_int == 500):
            strout.cntrs = _np.arange(4800, 8001, 50)
            strout.clab = strout.cntrs[::4]
        elif (strout.lev_int == 300):
            strout.cntrs = _np.arange(8000, 10001, 50)
            strout.clab = strout.cntrs[::4]

    elif (vnam in ['T925', 'T850', 'T800', 'T700', 'T600', 'T500', 'T300']):
        strout.name = 'temperature'
        strout.name_short = 'temp'
        strout.level = '%s hPa' % vnam[1:]
        strout.inc = _np.arange(0.0, 5.25, 0.25)
        strout.ilab = strout.inc[::4]
        strout.spr = _np.arange(0.0, 5.25, 0.25)
        strout.slab = strout.spr[::4]
        strout.units = '$K$'
        strout.lev_int = int(vnam[1:])
        if (strout.lev_int == 925):
            strout.cntrs = _np.arange(-30, 31, 5)
            strout.clab = strout.cntrs[::4]
        elif (strout.lev_int == 850):
            strout.cntrs = _np.arange(-40, 41, 5)
            strout.clab = strout.cntrs[::4]
        elif (strout.lev_int == 800):
            strout.cntrs = _np.arange(-40, 41, 5)
            strout.clab = strout.cntrs[::4]
        elif (strout.lev_int == 700):
            strout.cntrs = _np.arange(-40, 41, 5)
            strout.clab = strout.cntrs[::4]
        elif (strout.lev_int == 600):
            strout.cntrs = _np.arange(-100, 41, 5)
            strout.clab = strout.cntrs[::4]
        elif (strout.lev_int == 500):
            strout.cntrs = _np.arange(-100, 41, 5)
            strout.clab = strout.cntrs[::4]
        elif (strout.lev_int == 300):
            strout.cntrs = _np.arange(-100, 41, 5)
            strout.clab = strout.cntrs[::4]

    elif (vnam in ['U925', 'U850', 'U800', 'U700', 'U600', 'U500', 'U300',
                   'V925', 'V850', 'V800', 'V700', 'V600', 'V500', 'V300']):
        strout.name = '%s-wind' % vnam[0].lower()
        strout.name_short = '%s' % vnam[0].lower()
        strout.level = '%s hPa' % vnam[1:]
        strout.cntrs = _np.arange(-100, 101, 5)
        strout.clab = strout.cntrs[::4]
        strout.inc = _np.arange(0.0, 11.0, 1.0)
        strout.ilab = strout.inc[::4]
        strout.spr = _np.arange(0.0, 11.0, 1.0)
        strout.slab = strout.spr[::4]
        strout.units = '$ms^{-1}$'
        strout.lev_int = int(vnam[1:])

    elif (vnam in ['Y925', 'Y850', 'Y800', 'Y700', 'Y600', 'Y500', 'Y300']):
        strout.name = 'wind'
        strout.name_short = 'wnd'
        strout.level = '%s hPa' % vnam[1:]
        strout.cntrs = _np.arange(0, 101, 5)
        strout.clab = strout.cntrs[::4]
        strout.inc = _np.arange(0.0, 11.0, 1.0)
        strout.ilab = strout.inc[::4]
        strout.spr = _np.arange(0.0, 11.0, 1.0)
        strout.slab = strout.spr[::4]
        strout.units = '$ms^{-1}$'
        strout.lev_int = int(vnam[1:])

    elif (vnam in ['VORT925', 'VORT850', 'VORT800',
                   'VORT700', 'VORT600', 'VORT500', 'VORT300',
                   'CIRC925', 'CIRC850', 'CIRC800',
                   'CIRC700', 'CIRC600', 'CIRC500', 'CIRC300']):
        if (vnam[0:4] == 'VORT'):
            strout.name = 'vorticity'
        elif (vnam[0:4] == 'CIRC'):
            strout.name = 'circulation'
        strout.name_short = '%s' % vnam[0:4].lower()
        strout.level = '%s hPa' % vnam[-3:]
        strout.cntrs = _np.arange(-10, 11, 1)
        strout.clab = strout.cntrs[::2]
        strout.inc = _np.arange(-5.0, 5.25, 0.25)
        strout.ilab = strout.inc[::4]
        strout.spr = _np.arange(0.0, 2.25, 0.25)
        strout.slab = strout.spr[::4]
        strout.units = 'x$10^{-5} s^{-1}$'
        strout.lev_int = int(vnam[-3:])

    elif (vnam in ['QV925', 'QV850', 'QV700',
                   'QV500', 'QV300',
                   'QVAPOR925', 'QVAPOR850',
                   'QVAPOR700', 'QVAPOR500', 'QVAPOR300']):
        strout.name = 'mix. ratio'
        strout.name_short = 'qvap'
        strout.level = '%s hPa' % vnam[-3:]
        strout.cntrs = _np.arange(1e-3, 1e-3, 10e-3)
        strout.clab = strout.cntrs[::4]
        strout.inc = _np.arange(0.0, 4e-3, 5e-4)
        strout.ilab = strout.inc[::4]
        strout.spr = _np.arange(0.0, 4e-3, 5e-4)
        strout.slab = strout.spr[::4]
        strout.units = '$gkg^{-1}$'
        strout.lev_int = int(vnam[-3:])

    elif (vnam in ['QC925', 'QC850', 'QC700',
                   'QC500', 'QC300',
                   'QCLOUD925', 'QCLOUD850', 'QCLOUD700',
                   'QCLOUD500', 'QCLOUD300']):
        strout.name = 'cloud mix. ratio'
        strout.name_short = 'qcld'
        strout.level = '%s hPa' % vnam[-3:]
        strout.cntrs = _np.arange(1e-3, 1e-3, 10e-3)
        strout.clab = strout.cntrs[::4]
        strout.inc = _np.arange(0.0, 4e-3, 5e-4)
        strout.ilab = strout.inc[::4]
        strout.spr = _np.arange(0.0, 4e-3, 5e-4)
        strout.slab = strout.spr[::4]
        strout.units = '$gkg^{-1}$'
        strout.lev_int = int(vnam[-3:])

    elif (vnam in ['RH925', 'RH850', 'RH700', 'RH500', 'RH300']):
        strout.name = 'relative humidity'
        strout.name_short = 'rh'
        strout.level = '%s hPa' % vnam[2:]
        strout.cntrs = _np.arange(0, 101, 10)
        strout.clab = strout.cntrs[::4]
        strout.inc = _np.arange(0.0, 35.0, 5.0)
        strout.ilab = strout.inc[::4]
        strout.spr = _np.arange(0.0, 35.0, 5.0)
        strout.slab = strout.spr[::4]
        strout.units = '$%%$'
        strout.lev_int = int(vnam[2:])

    elif (vnam in ['RAIN', 'RAINNC', 'PRECIP']):
        strout.name = 'precip.'
        strout.name_short = 'pcp'
        strout.level = ''
        strout.cntrs = _np.arange(0, 51, 2)
        strout.clab = strout.cntrs[::4]
        strout.inc = _np.arange(0.0, 25.0, 5.0)
        strout.ilab = strout.inc[::4]
        strout.spr = _np.arange(0.0, 25.0, 5.0)
        strout.slab = strout.spr[::4]
        strout.units = '$mm$'
        strout.lev_int = -1

    elif (vnam == 'AICE'):
        strout.name = 'ice-area'
        strout.name_short = 'aice'
        strout.cntrs = _np.array(
            [0.01, 0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.99])
        strout.clab = list(strout.cntrs[:])
        strout.ylab = 'm$^2$'
        strout.units = 'm$^2$'
        strout.level = 'surface'
        strout.level_int = '-1'

    elif (vnam == 'HICE'):
        strout.name = 'ice-volume'
        strout.name_short = 'hice'
        strout.cntrs = _np.array(
            [0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0])
        strout.clab = list(strout.cntrs[:])
        strout.ylab = 'm$^3$'
        strout.units = 'm$^3$'
        strout.level = 'surface'
        strout.level_int = '-1'

    elif (vnam == 'T'):
        strout.name = 'sea-surface temperature'
        strout.name_short = 'ts'
        strout.cntrs = _np.arange(275, 317.5, 2.5)
        strout.clab = list(strout.cntrs[::2])
        strout.ylab = 'K'
        strout.units = 'K'
        strout.level = 'surface'
        strout.level_int = '-1'

    elif (vnam == 'S'):
        strout.name = 'sea-surface salinity'
        strout.name_short = 'ts'
        strout.cntrs = _np.arange(30, 40.25, 0.25)
        strout.clab = list(strout.cntrs[::4])
        strout.ylab = 'PSU'
        strout.units = 'PSU'
        strout.level = 'surface'
        strout.level_int = '-1'

    elif (vnam == 'TS'):
        strout.name = 'sea-surface temperature'
        strout.name_short = 'ts'
        strout.cntrs = _np.arange(275, 317.5, 2.5)
        strout.clab = list(strout.cntrs[::2])
        strout.ylab = 'K'
        strout.units = 'K'
        strout.level = 'surface'
        strout.level_int = '-1'

    elif (vnam == 'SS'):
        strout.name = 'sea-surface salinity'
        strout.name_short = 'ts'
        strout.cntrs = _np.arange(30, 40.25, 0.25)
        strout.clab = list(strout.cntrs[::4])
        strout.ylab = 'PSU'
        strout.units = 'PSU'
        strout.level = 'surface'
        strout.level_int = '-1'

    elif (vnam == 'DH'):
        strout.name = 'layer-thickness'
        strout.name_short = 'dh'
        strout.cntrs = _np.array([5.0,
                                  10.0,
                                  20.0,
                                  30.0,
                                  40.0,
                                  50.0,
                                  75.0,
                                  100.0,
                                  200.0,
                                  300.0,
                                  400.0,
                                  500.0,
                                  600.0,
                                  700.0,
                                  800.0,
                                  900.0,
                                  1000.0,
                                  1500.0,
                                  2000.0,
                                  2500.0])
        strout.clab = list(strout.cntrs[:])
        strout.ylab = 'm'
        strout.units = 'm'
        strout.level = 'surface'
        strout.level_int = '-1'

    elif (vnam == 'NITRATE'):
        strout.name = 'nitrate'
        strout.name_short = 'rno'
        strout.cntrs = _np.array([0.1,
                                  0.25,
                                  0.5,
                                  0.75,
                                  1.0,
                                  1.5,
                                  2.0,
                                  3.0,
                                  4.0,
                                  5.0,
                                  7.5,
                                  10.0,
                                  25.0,
                                  50.0,
                                  75.0,
                                  100.0])
        strout.clab = list(strout.cntrs[:])
        strout.ylab = '$\mu$M'
        strout.units = '$\mu$M'
        strout.level = ''
        strout.level_int = ''

    elif (vnam == 'CHLORO'):
        strout.name = 'chlorophytes'
        strout.name_short = 'chl'
        strout.cntrs = _np.array([0.01,
                                  0.05,
                                  0.1,
                                  0.15,
                                  0.2,
                                  0.25,
                                  0.3,
                                  0.35,
                                  0.4,
                                  0.45,
                                  0.5,
                                  0.6,
                                  0.7,
                                  0.8,
                                  0.9,
                                  1,
                                  1.5,
                                  3,
                                  5,
                                  7.5,
                                  10])
        strout.cntrs = _np.array([0.01,
                                  0.05,
                                  0.1,
                                  0.15,
                                  0.2,
                                  0.25,
                                  0.3,
                                  0.35,
                                  0.4,
                                  0.45,
                                  0.5,
                                  0.6,
                                  0.7,
                                  0.8,
                                  0.9,
                                  1])
        strout.clab = list(strout.cntrs[:])
        strout.ylab = 'mg/m$^3$'
        strout.units = 'mg/m$^3$'
        strout.level = ''
        strout.level_int = ''

    elif (vnam == 'SILICA'):
        strout.name = 'silica'
        strout.name_short = 'sil'
        strout.cntrs = _np.array([0.1,
                                  0.25,
                                  0.5,
                                  0.75,
                                  1.0,
                                  1.5,
                                  2.0,
                                  3.0,
                                  4.0,
                                  5.0,
                                  7.5,
                                  10.0,
                                  25.0,
                                  50.0,
                                  75.0,
                                  100.0])
        strout.clab = list(strout.cntrs[:])
        strout.ylab = '$\mu$M'
        strout.units = '$\mu$M'
        strout.level = ''
        strout.level_int = ''

    elif (vnam == 'DIC'):
        strout.name = 'dissolved inorganic carbon'
        strout.name_short = 'dic'
        strout.cntrs = _np.arange(1800, 2425, 25)
        strout.clab = list(strout.cntrs[::4])
        strout.ylab = '$\mu$M'
        strout.units = '$\mu$M'
        strout.level = ''
        strout.level_int = ''

    elif (vnam == 'DIATOM'):
        strout.name = 'diatoms'
        strout.name_short = 'dia'
        strout.cntrs = _np.array([0.01,
                                  0.05,
                                  0.1,
                                  0.15,
                                  0.2,
                                  0.25,
                                  0.3,
                                  0.35,
                                  0.4,
                                  0.45,
                                  0.5,
                                  0.6,
                                  0.7,
                                  0.8,
                                  0.9,
                                  1.0,
                                  1.5,
                                  3.0,
                                  5.0,
                                  7.5,
                                  10.0])
        strout.cntrs = _np.array([0.01,
                                  0.05,
                                  0.1,
                                  0.15,
                                  0.2,
                                  0.25,
                                  0.3,
                                  0.35,
                                  0.4,
                                  0.45,
                                  0.5,
                                  0.6,
                                  0.7,
                                  0.8,
                                  0.9,
                                  1.0])
        strout.clab = list(strout.cntrs[:])
        strout.ylab = 'mg/m$^3$'
        strout.units = 'mg/m$^3$'
        strout.level = ''
        strout.level_int = ''

    elif (vnam == 'CYANO'):
        strout.name = 'cyanobacteria'
        strout.name_short = 'cya'
        strout.cntrs = _np.array([0.01,
                                  0.05,
                                  0.1,
                                  0.15,
                                  0.2,
                                  0.25,
                                  0.3,
                                  0.35,
                                  0.4,
                                  0.45,
                                  0.5,
                                  0.6,
                                  0.7,
                                  0.8,
                                  0.9,
                                  1.0,
                                  1.5,
                                  3.0,
                                  5.0,
                                  7.5,
                                  10.0])
        strout.cntrs = _np.array([0.01,
                                  0.05,
                                  0.1,
                                  0.15,
                                  0.2,
                                  0.25,
                                  0.3,
                                  0.35,
                                  0.4,
                                  0.45,
                                  0.5,
                                  0.6,
                                  0.7,
                                  0.8,
                                  0.9,
                                  1.0])
        strout.clab = list(strout.cntrs[:])
        strout.ylab = 'mg/m$^3$'
        strout.units = 'mg/m$^3$'
        strout.level = ''
        strout.level_int = ''

    elif (vnam == 'COCCO'):
        strout.name = 'coccolithophores'
        strout.name_short = 'coc'
        strout.cntrs = _np.array([0.01,
                                  0.05,
                                  0.1,
                                  0.15,
                                  0.2,
                                  0.25,
                                  0.3,
                                  0.35,
                                  0.4,
                                  0.45,
                                  0.5,
                                  0.6,
                                  0.7,
                                  0.8,
                                  0.9,
                                  1.0,
                                  1.5,
                                  3.0,
                                  5.0,
                                  7.5,
                                  10.0])
        strout.cntrs = _np.array([0.01,
                                  0.05,
                                  0.1,
                                  0.15,
                                  0.2,
                                  0.25,
                                  0.3,
                                  0.35,
                                  0.4,
                                  0.45,
                                  0.5,
                                  0.6,
                                  0.7,
                                  0.8,
                                  0.9,
                                  1.0])
        strout.clab = list(strout.cntrs[:])
        strout.ylab = 'mg/m$^3$'
        strout.units = 'mg/m$^3$'
        strout.level = ''
        strout.level_int = ''

    elif (vnam == 'TOT'):
        strout.name = 'total chlorophyll'
        strout.name_short = 'tot'
        strout.cntrs = _np.array([0.01,
                                  0.05,
                                  0.1,
                                  0.15,
                                  0.2,
                                  0.25,
                                  0.3,
                                  0.35,
                                  0.4,
                                  0.45,
                                  0.5,
                                  0.6,
                                  0.7,
                                  0.8,
                                  0.9,
                                  1.0,
                                  1.5,
                                  3.0,
                                  5.0,
                                  7.5,
                                  10.0])
        strout.clab = list(strout.cntrs[:])
        strout.ylab = 'mg/m$^3$'
        strout.units = 'mg/m$^3$'
        strout.level = ''
        strout.level_int = ''

    elif (vnam == 'T10'):
        strout.name = '10m temperature'
        strout.name_short = 'T10'
        strout.cntrs = _np.arange(275, 317.5, 2.5)
        strout.clab = list(strout.cntrs[::2])
        strout.ylab = 'K'
        strout.units = 'K'
        strout.level = '10 meters'
        strout.level_int = '10'

    elif (vnam == 'U'):
        strout.name = 'zonal wind'
        strout.name_short = 'U'
        strout.cntrs = _np.arange(-100, 100, 5.0)
        strout.clab = list(strout.cntrs[::10])
        strout.ylab = 'm/s'
        strout.units = 'm/s'
        strout.level = ''
        strout.level_int = ''

    else:
        raise InputError('variable %s is not implemented yet' % vnam)

    return strout
