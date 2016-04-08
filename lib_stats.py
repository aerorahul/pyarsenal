#!/usr/bin/env python

###############################################################
# < next few lines under version control, D O  N O T  E D I T >
# $Date$
# $Revision$
# $Author$
# $Id$
###############################################################

'''
lib_stats.py contains statistics utility functions
'''

__author__ = "Rahul Mahajan"
__email__ = "rahul.mahajan@nasa.gov"
__copyright__ = "Copyright 2016, NOAA / NCEP / EMC"
__license__ = "GPL"
__status__ = "Prototype"
__all__ = ['mstats', 'lregress', 'ttest', 'get_weights', 'get_weighted_mean']

import numpy as _np
from scipy.stats import t.ppf as _t.ppf


def mstats(x):
    '''
    mstats : function that computes and displays
             various statistics of a variable
             A better alternative is scipy.stats.describe()

    mstats(x)

        x - variable whose statistics are to be computed and displayed
    '''

    OUT = type('', (), {})

    OUT.MatrixSize = _np.shape(x)
    OUT.NElements = _np.prod(OUT.MatrixSize)
    OUT.Nnans = _np.sum(_np.isnan(x))
    OUT.NAnalyzedElements = OUT.NElements - OUT.Nnans

    datatype = x.dtype

    xf = x.flatten()
    xf = xf[~_np.isnan(xf)]
    absxf = _np.abs(xf)

    OUT.Mean = _np.mean(xf)
    OUT.Max = _np.max(xf)
    OUT.Min = _np.min(xf)
    OUT.Median = _np.median(xf)
    OUT.StDev = _np.std(xf, ddof=1)
    OUT.MeanAbs = _np.mean(absxf)
    OUT.MinAbs = _np.min(absxf[absxf > 0.0])
    OUT.FracZero = len(xf[xf == 0.0]) / OUT.NAnalyzedElements
    OUT.FracNan = OUT.Nnans / OUT.NElements

    print '================= m s t a t s =================='
    print '        MatrixSize: %s' % (str(OUT.MatrixSize))
    print '         NElements: %d' % (OUT.NElements)
    print ' NAnalyzedElements: %d' % (OUT.NAnalyzedElements)
    if datatype in ['int', 'int8', 'int16', 'int32', 'int64',
                    'uint8', 'uint16', 'uint32', 'uint64',
                    'float', 'float16', 'float32', 'float64']:
        print '              Mean: %f' % (OUT.Mean)
        print '               Max: %f' % (OUT.Max)
        print '               Min: %f' % (OUT.Min)
        print '            Median: %f' % (OUT.Median)
        print '             StDev: %f' % (OUT.StDev)
        print '           MeanAbs: %f' % (OUT.MeanAbs)
        print '            MinAbs: %f' % (OUT.MinAbs)
    if datatype in ['complex', 'complex64', 'complex128']:
        print '              Mean: %f + %fi' % (OUT.Mean.real, OUT.Mean.imag)
        print '               Max: %f + %fi' % (OUT.Max.real, OUT.Max.imag)
        print '               Min: %f + %fi' % (OUT.Min.real, OUT.Min.imag)
        print '            Median: %f + %fi' % (OUT.Median.real, OUT.Median.imag)
        print '             StDev: %f + %fi' % (OUT.StDev.real, OUT.StDev.imag)
        print '           MeanAbs: %f + %fi' % (OUT.MeanAbs.real, OUT.MeanAbs.imag)
        print '            MinAbs: %f + %fi' % (OUT.MinAbs.real, OUT.MinAbs.imag)
    print '          FracZero: %f' % (OUT.FracZero)
    print '           FracNaN: %f' % (OUT.FracNan)
    print '================================================'

    return


def lregress(x, y, tcrit=0.0):
    '''
    lregress : function that computes the linear regression between
               two variables and returns the regression coefficient and statistical significance
               for a t-value at a desired confidence interval.

    [rc, sb, ssig] = lregress(x, y, tcrit=0.0)

        x - independent variable
        y - dependent variable
    tcrit - t statistic critical factor [Default: tcrit = 0.0]
       rc - linear regression coefficient
       sb - standard error on the linear regression coefficient
     ssig - statistical significance of the linear regression coefficient
    '''

    # make sure the two samples are of the same size
    if (len(x) != len(y)):
        raise ValueError('samples x and y are not of the same size')
    else:
        nsamp = len(x)

    covmat = _np.cov(x, y=y, ddof=1)
    cov_xx = covmat[0, 0]
    cov_yy = covmat[1, 1]
    cov_xy = covmat[0, 1]

    # regression coefficient (rc)
    rc = cov_xy / cov_xx
    # total standard error squared (se)
    se = (cov_yy - (rc**2) * cov_xx) * (nsamp - 1) / (nsamp - 2)
    # standard error on rc (sb)
    sb = _np.sqrt(se / (cov_xx * (nsamp - 1)))
    # error bar on rc
    eb = tcrit * sb

    if ((_np.abs(rc) - _np.abs(eb)) > 0.0):
        ssig = True
    else:
        ssig = False

    return [rc, sb, ssig]


def ttest(x, y, ci=95.0, paired=True):
    '''
    Given two samples, perform the Student's t-test and return the errorbar
    '''

    pval = 1.0 - (1.0 - ci / 100.0) / 2.0
    tcrit = _t.ppf(pval, 2 * len(y) - 2)

    diffmean = x.mean() - y.mean()

    if (paired):
        # paired t-test
        std_err = _np.sqrt(_np.var(x - y, ddof=1) / len(y))
    else:
        # unpaired t-test
        std_err = _np.sqrt((x.var(ddof=1) + y.var(ddof=1)) / (len(y) - 1.0))

    errorbar = tcrit * std_err

    # normalize (rescale) the diffmean and errorbar
    scale_fac = 100.0 / y.mean()
    diffmean_norm = diffmean * scale_fac
    errorbar_norm = errorbar * scale_fac

    return x.mean(), diffmean_norm, errorbar_norm


def get_weights(lats):
    '''
    Get weights for latitudes to do weighted mean
    '''
    return _np.cos((_np.pi / 180.0) * lats)


def get_weighted_mean(data, wght, axis=0):
    '''
    Given the weights for latitudes, computed weighted mean of data in that direction
    Note, data and wght must be same dimension
    '''
    if (data.shape != wght.shape):
        raise ValueError('data and weights mis-match array size')

    return (wght * data).mean(axis=axis) / wght.mean(axis=axis)
