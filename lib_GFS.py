#!/usr/bin/env python

###############################################################
# < next few lines under version control, D O  N O T  E D I T >
# $Date$
# $Revision$
# $Author$
# $Id$
###############################################################

'''
lib_GFS.py contains utility functions for GFS
'''

__author__ = "Rahul Mahajan"
__email__ = "rahul.mahajan@noaa.gov"
__copyright__ = "Copyright 2016, NOAA / NCEP / EMC"
__license__ = "GPL"
__status__ = "Prototype"
__all__ = ['get_akbk',
           'get_pcoord',
           'read_atcf']

import numpy as _np
import pandas as _pd

def get_akbk():
    '''
    Returns ak,bk for 64 level GFS model
    vcoord is obtained from global_fcst.fd/gfsio_module.f
    ak,bk are as computed from treadeo.gfsio.f for
    hybrid = .true. and idvc == 2
    '''

    vcoord = _np.array([1.0000000,0.99467099,0.98863202,0.98180002,0.97408301, \
           0.96538502,0.95560300,0.94463098,0.93235999,0.91867799,0.90347999, \
           0.88666302,0.86813903,0.84783000,0.82568502,0.80167699,0.77581102, \
           0.74813300,0.71872902,0.68773103,0.65531600,0.62170500,0.58715999, \
           0.55197400,0.51646298,0.48095500,0.44577801,0.41124901,0.37765899, \
           0.34526899,0.31430000,0.28492799,0.25728399,0.23145400,0.20748200, \
           0.18537199,0.16509899,0.14660800,0.12982300,0.11465500,0.10100200, \
           0.88756002E-01,0.77808000E-01,0.68048999E-01,0.59370000E-01, \
           0.51670998E-01,0.44854999E-01,0.38830999E-01,0.33514999E-01, \
           0.28829999E-01,0.24707999E-01,0.21083999E-01,0.17901000E-01, \
           0.15107000E-01,0.12658000E-01,0.10511000E-01,0.86310003E-02, \
           0.69849999E-02,0.55439998E-02,0.42840000E-02,0.31830000E-02, \
           0.22199999E-02,0.13780000E-02,0.64200000E-03,0.0000000])

    ak = vcoord / 1000.
    bk = vcoord / 1.

    return ak,bk

def get_pcoord():
    '''
    Returns the pressure levels in hPa of the native GFS model with 64 levels.

    OUTPUT:
        pres = pressure levels (hPa) assuming pref=1013.0
    '''

    ak,bk = get_akbk()
    pref = 101.3
    pres = ak[:-1] + bk[:-1]*pref

    return pres * 10.

def read_atcf(filename):
    '''
    Read an ATCF file into a dataframe for ease of processing.
    INPUT:
        filename = ATCF filename
        The file contents are specified at:
        http://www.nrlmry.navy.mil/atcf_web/docs/database/new/abdeck.html
    OUTPUT:
        df = DataFrame containing the file contents
    '''

    def _to_number(s):
        tmp = 0.1 * _np.float(s[:-1])
        if s[-1] in ['S','W']:
            v = -1.0 * tmp if s[-1] in ['S'] else 360.0 - tmp
        else:
            v = tmp
        return v

    # column names
    names = ['BASIN','CY','YYYYMMDDHH','TECHNUM','TECH','TAU','LAT','LON','VMAX','MSLP','TY','RAD','WINDCODE','RAD1','RAD2','RAD3','RAD4','POUTER','ROUTER','RMW','GUSTS','EYE','SUBREGION','MAXSEAS','INITIALS','DIR','SPEED','STORMNAME','DEPTH','SEAS','SEASCODE','SEAS1','SEAS2','SEAS3','SEAS4','USERDEFINE1','USERDATA1','USERDEFINE2','USERDATA2','USERDEFINE3','USERDATA3','USERDEFINE4','USERDATA4','USERDEFINE5','USERDATA5']

    # column datatypes
    dtypes = {'BASIN':str,'CY':str,'YYYYMMDDHH':str,'TECHNUM':_np.float,'TECH':str,'TAU':_np.float,'LAT':str,'LON':str,'VMAX':_np.float,'MSLP':_np.float,'TY':str,'RAD':_np.float,'WINDCODE':str,'RAD1':_np.float,'RAD2':_np.float,'RAD3':_np.float,'RAD4':_np.float,'POUTER':_np.float,'ROUTER':_np.float,'RMW':_np.float,'GUSTS':_np.float,'EYE':_np.float,'SUBREGION':str,'MAXSEAS':_np.float,'INITIALS':str,'DIR':_np.float,'SPEED':_np.float,'STORMNAME':str,'DEPTH':str,'SEAS':_np.float,'SEASCODE':str,'SEAS1':_np.float,'SEAS2':_np.float,'SEAS3':_np.float,'SEAS4':_np.float,'USERDEFINE1':str,'USERDATA1':str,'USERDEFINE2':str,'USERDATA2':str,'USERDEFINE3':str,'USERDATA3':str,'USERDEFINE4':str,'USERDATA4':str,'USERDEFINE5':str,'USERDATA5':str}

    df = _pd.read_csv(filename,skipinitialspace=True,header=None,names=names,dtype=dtypes)

    # convert YYYYMMDDHH into datetime
    df['YYYYMMDDHH'] = _pd.to_datetime(df['YYYYMMDDHH'], format='%Y%m%d%H')

    # set index columns
    index_cols = ['BASIN','CY','YYYYMMDDHH','TECHNUM','TECH','TAU','TY','SUBREGION']
    df.set_index(index_cols, inplace=True)

    # drop columns that have no information
    df.dropna(axis=1,how='all',inplace=True)

    # convert Lat/Lon to floats from hemisphere info
    df['LAT'] = df['LAT'].apply(lambda f: _to_number(f))
    df['LON'] = df['LON'].apply(lambda f: _to_number(f))

    return df
