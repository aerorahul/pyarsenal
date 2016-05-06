#!/usr/bin/env python

###############################################################
# < next few lines under version control, D O  N O T  E D I T >
# $Date$
# $Revision$
# $Author$
# $Id$
###############################################################

'''
lib_GSI.py contains utility functions for GSI
'''

__author__ = "Rahul Mahajan"
__email__ = "rahul.mahajan@nasa.gov"
__copyright__ = "Copyright 2016, NOAA / NCEP / EMC"
__license__ = "GPL"
__status__ = "Prototype"
__all__ = ['get_convdiag_indices','get_convdiag_data','get_raddiag_indices', 'get_raddiag_data']

import numpy as _np
import read_diag as _rd

def get_convdiag_indices(fname,obtype,code=None,iused=1,endian='big'):
    '''
    Given parameters, get the indicies of observation locations from a conventional diagnostic file
    INPUT:
        fname  : name of the conventional diagnostic file
        obtype : observation type e.g. 'ps', 'u', 'v', 't' etc
        code   : KX (default: None)
        iused  : qc flag (default: 1)
        endian : filetype (default: 'big')
    OUTPUT:
        index  : indices of the requested data in the file
    '''

    try:
        diag = _rd.diag_conv(fname,endian=endian)
        diag.read_obs()
    except:
        raise Exception('Error handling %s' % fname)

    indx = diag.obtype == obtype.rjust(3)
    if code is not None:
        indx = _np.logical_and(indx,diag.code==code)
    indx = _np.logical_and(indx,diag.used==iused)

    return indx

def get_convdiag_data(fname,indx,qty,endian='big'):
    '''
    Given indices, get a specific quantity from the radiance diagnostic file.
    For searching through the quantities, do a dir(diag)
    INPUT:
        fname  : name of the conventional diagnostic file
        index  : indices of the requested data in the file
        qty    : quantity to retrieve e.g. 'hx', 'ob', 'oberr', etc ...
    OUTPUT:
        data   : requested data
    '''

    try:
        diag = _rd.diag_conv(fname,endian=endian)
        diag.read_obs()
    except:
        raise Exception('Error handling %s' % fname)

    exec('val = diag.%s[indx]' % qty)

    return val

def get_raddiag_indices(fname,ichan,iused=1,oberr=1.e9,water=False,land=False,ice=False,snow=False,snowice=False,endian='big'):
    '''
    Given parameters, get the indicies of observation locations from a radiance diagnostic file
    INPUT:
        fname  : name of the conventional diagnostic file
        ichan  : channel number
        iused  : qc flag (default: 1)
        oberr  : filter through observation error (default: 1.e9)
        water  : filter observations over water (default: False)
        land   : filter observations over land (default: False)
        ice    : filter observations over ice (default: False)
        snow   : filter observations over snow (default: False)
        snowice: filter observations over snowice (default: False)
        endian : filetype (default: 'big')
    OUTPUT:
        index  : indices of the requested data in the file
    '''

    try:
        diag = _rd.diag_rad(fname,endian=endian)
        diag.read_obs()
    except:
        raise Exception('Error handling %s' % fname)

    indx = _np.logical_and(diag.channel==ichan,diag.used==iused)
    indx = _np.logical_and(indx,diag.oberr<oberr)
    if ( water   ): indx = _np.logical_and(indx,diag.water_frac<0.99)
    if ( land    ): indx = _np.logical_and(indx,diag.land_frac<0.01)
    if ( ice     ): indx = _np.logical_and(indx,diag.ice_frac<0.99)
    if ( snow    ): indx = _np.logical_and(indx,diag.snow_frac<0.99)
    if ( snowice ): indx = _np.logical_and(indx,diag.snow_frac+diag.ice_frac<0.99)

    return indx

def get_raddiag_data(fname,indx,qty,endian='big'):
    '''
    Given indices, get a specific quantity from the radiance diagnostic file.
    For searching through the quantities, do a dir(diag)
    INPUT:
        fname  : name of the conventional diagnostic file
        index  : indices of the requested data in the file
        qty    : quantity to retrieve e.g. 'hx', 'ob', 'oberr', etc ...
    OUTPUT:
        data   : requested data
    '''

    try:
        diag = _rd.diag_rad(fname,endian=endian)
        diag.read_obs()
    except:
        raise Exception('Error handling %s' % fname)

    exec('val = diag.%s[indx]' % qty)

    return val
