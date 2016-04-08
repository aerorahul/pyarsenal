#!/usr/bin/env python
###############################################################
# < next few lines under version control, D O  N O T  E D I T >
# $Date$
# $Revision$
# $Author$
# $Id$
###############################################################

'''
lib_GrADS.py contains an interface to PyGrADS object GrADS
It makes reading a binary grads and ctl file easy
'''

from grads import GrADS as _GrADS

__author__ = "Rahul Mahajan"
__email__ = "rahul.mahajan@nasa.gov"
__copyright__ = "Copyright 2016, NOAA / NCEP / EMC"
__license__ = "GPL"
__status__ = "Prototype"
__version__ = "0.1"
__all__ = ['grads_session']


class grads_session(object):

    def __init__(self, ctl, window=False, verbose=False):
        '''
        Initialize a GrADS session
        gs = grads_session('grads.ctl',window=False,verbose=False)
        '''

        # init pygrads
        self.ga = _GrADS(Window=window, Echo=verbose)

        # open file
        self.fh = self.ga.open(ctl)

        return

    def read_data_ts(self, var='cor', exp=1, fhr=1, time=None):
        '''
        Read time-series data
        cor = self.read_data_ts(var='cor',exp=1,fhr=1,time=None)
        '''

        self.ga('set dfile %d' % self.fh.fid)

        if (time is None):
            time = self.fh.nt

        self.ga('set x   %d' % exp)
        self.ga('set y   %d' % fhr)
        self.ga('set z   %d' % 1)
        self.ga('set t 1 %d' % time)

        return self.ga.expr('%s' % var)

    def read_gridded_data(self,
                          var='T',
                          lons=[-180.0,
                                180.0],
                          lats=[-90.0,
                                90.0],
                          time=None,
                          z=[1],
                          lev=None):
        '''
        Read gridded data; default T at 00Z01Jan2000 on z=1 surface
        '''

        self.ga('set dfile %d' % self.fh.fid)

        if (len(lons) == 1):
            self.ga('set lon %f' % (lons[0]))
        else:
            self.ga('set lon %f %f' % (lons[0], lons[1]))

        if (len(lats) == 1):
            self.ga('set lat %f' % (lats[0]))
        else:
            self.ga('set lat %f %f' % (lats[0], lats[1]))

        if (len(z) == 1):
            self.ga('set z %f' % (z[0]))
        else:
            self.ga('set z %d %d' % (z[0], z[1]))

        if (lev is not None):
            self.ga('set lev %f' % lev)

        if (time is not None):
            self.ga('set time %s' % time)
        else:
            self.ga('set time 00Z01Jan2000')

        return self.ga.expr('%s' % var)
