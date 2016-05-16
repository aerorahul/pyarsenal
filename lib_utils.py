#!/usr/bin/env python

###############################################################
# < next few lines under version control, D O  N O T  E D I T >
# $Date$
# $Revision$
# $Author$
# $Id$
###############################################################

'''
lib_utils.py contains handy utility functions
'''

__author__ = "Rahul Mahajan"
__email__ = "rahul.mahajan@nasa.gov"
__copyright__ = "Copyright 2016, NOAA / NCEP / EMC"
__license__ = "GPL"
__status__ = "Prototype"
__all__ = [
            'float10Power','roundNumber',
            'pickle','unpickle',
            'writeHDF','readHDF',
            'EmptyDataFrame'
          ]


import numpy as _np
import cPickle as _pickle
import pandas as _pd

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
    '''
    Input: Number
    Output: Number rounded to the nearest 10th.
    eg.
    0.01231 => 0.01    0.0164  => 0.02
    2.3     => 2.0     2.8     => 3.0
    6.2     => 10
    59      => 60
    '''

    d = float10Power(value)
    round_value = _np.round(abs(value)/10**d) * 10**d * _np.sign(value)

    return round_value


def pickle(fname,data,mode='wb'):
    '''
    fname - filename to pickle to
    data  - data to pickle
    mode - mode to pickle (default: wb)
    '''
    print('pickling ... %s' % fname)
    try:
        _pickle.dump(data, open(fname, mode))
    except _pickle.PicklingError:
        raise
    print ' ... done'
    return


def unpickle(fname, mode='rb'):
    '''
    fname - filename to unpickle to
    mode - mode to unpickle (default: rb)
    '''
    print('unpickling ... %s' % fname),
    try:
        data = _pickle.load(open(fname, mode))
    except _pickle.UnpicklingError:
        raise
    print ' ... done'
    return data


def writeHDF(fname,vname,data):
    print('writing ... %s' % fname),
    try:
        hdf = _pd.HDFStore(fname)
        hdf.put(vname,data,format='table',append=True)
        hdf.close()
    except RuntimeError:
        raise
    print ' ... done'
    return


def readHDF(fname,vname,**kwargs):
    print('reading ... %s' % fname),
    try:
        data = _pd.read_hdf(fname,vname,**kwargs)
    except RuntimeError:
        raise
    print ' ... done'
    return data


def EmptyDataFrame(columns,names,dtype=None):
    '''
        Create an empty Multi-index DataFrame
        Input:
            columns = 'name of all columns; including indices'
            names = 'name of index columns'
        Output:
            df = Multi-index DataFrame object
    '''

    levels = [[] for i in range(len(names))]
    labels = [[] for i in range(len(names))]
    indices = _pd.MultiIndex(levels=levels,labels=labels,names=names)
    df = _pd.DataFrame(index=indices, columns=columns, dtype=dtype)

    return df
