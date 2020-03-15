# coding: utf-8 -*-

'''
GrADS.py contains an interface to PyGrADS object GrADS
It makes reading a binary grads and ctl file easy
'''

from grads import GrADS as _GrADS

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

    def read_gridded_data(self, var=None,
            x=None, y=None, z=None, t=None,
            lon=None, lat=None, lev=None, time=None,
            GaField=True):
        '''
        Set dimension limits and then read gridded data
        default time used 00Z01Jan2000
        Returns a GAField by default, unless only data is requested
        via GaField=False
        '''

        if var == None:
            print 'Need to specify as variable'
            raise

        if x != None and lon != None:
            print 'Cannot specify both x and lon concurrently, chose one'
            raise

        if y != None and lat != None:
            print 'Cannot specify both y and lat concurrently, chose one'
            raise

        if z != None and lev != None:
            print 'Cannot specify both z and lev concurrently, chose one'
            raise

        self.ga('set dfile %d' % self.fh.fid)

        if x != None:
            if len(x) == 1:
                self.ga('set x %d' % (x[0]))
            else:
                self.ga('set x %d %d' % (x[0], x[1]))
        elif lon != None:
            if len(lon) == 1:
                self.ga('set lon %f' % (lon[0]))
            else:
                self.ga('set lon %f %f' % (lon[0], lon[1]))
        else:
            print 'WARNING! both x and lon are None'

        if y != None:
            if len(y) == 1:
                self.ga('set y %d' % (y[0]))
            else:
                self.ga('set y %d %d' % (y[0], y[1]))
        elif lat != None:
            if len(lat) == 1:
                self.ga('set lat %f' % (lat[0]))
            else:
                self.ga('set lat %f %f' % (lat[0], lat[1]))
        else:
            print 'WARNING! both y and lat are None'

        if z != None:
            if len(z) == 1:
                self.ga('set z %d' % (z[0]))
            else:
                self.ga('set z %d %d' % (z[0], z[1]))
        elif lev != None:
            if len(lev) == 1:
                self.ga('set lev %f' % (lev[0]))
            else:
                self.ga('set lev %d %d' % (lev[0], lev[1]))
        else:
            print 'WARNING! both z and lev are None'

        if t != None:
            if len(t) == 1:
                self.ga('set t %d' % (t[0]))
            else:
                self.ga('set t %d %d' % (t[0], t[1]))
        elif time != None:
            if len(time) == 1:
                self.ga('set time %d' % (t[0]))
            else:
                self.ga('set time %d %d' % (t[0], t[1]))
        else:
            if x != None:
                self.ga('set t 00Z01Jan2000')
            elif lon != None:
                self.ga('set time 00Z01Jan2000')

        return self.ga.expr('%s' % var) if GaField else self.ga.expr('%s' % var).data
