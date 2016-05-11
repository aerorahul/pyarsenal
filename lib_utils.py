#!/usr/bin/env python

###############################################################
# < next few lines under version control, D O  N O T  E D I T >
# $Date$
# $Revision$
# $Author$
# $Id$
###############################################################

'''
lib_utils.py contains commonly used utility functions
'''

__author__ = "Rahul Mahajan"
__email__ = "rahul.mahajan@nasa.gov"
__copyright__ = "Copyright 2016, NOAA / NCEP / EMC"
__license__ = "GPL"
__status__ = "Prototype"
__all__ = ['float10Power','roundNumber']


import numpy as _np


def float10Power(value):
    if value == 0:
        return 0
    d = _np.log10(abs(value))
    if d >= 0:
        d = _np.ceil(d) - 1.
    else:
        d = _np.floor(d)
    return d


def roundNumber(value):

    d = float10Power(value)
    round_value = _np.round(abs(value)/10**d) * 10**d * _np.sign(value)

    return round_value
