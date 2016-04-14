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
__all__ = ['get_raddiag_indices', 'get_raddiag_data']

import numpy as _np
import read_diag as _rd

def get_raddiag_indices(fname,ichan,iused=1,oberr=1.e9,water=False,land=False,ice=False,snow=False,snowice=False,endian='big'):
    '''
    Given parameters, get the indicies of observation locations from a radiance diagnostic file
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
    '''

    try:
        diag = _rd.diag_rad(fname,endian=endian)
        diag.read_obs()
    except:
        raise Exception('Error handling %s' % fname)

    exec('val = diag.%s[indx]' % qty)

    return val

