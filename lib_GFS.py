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
__email__ = "rahul.mahajan@nasa.gov"
__copyright__ = "Copyright 2016, NOAA / NCEP / EMC"
__license__ = "GPL"
__status__ = "Prototype"
__all__ = ['get_akbk','get_pcoord']

import numpy as _np

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
    pres = ak[:-1]. + bk[:-1]*pref

    return pres * 10.
