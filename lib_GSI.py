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
__all__ = ['get_convdiag_indices',
           'get_convdiag_data',
           'get_raddiag_indices',
           'get_raddiag_data',
           'GSIstat']

import numpy as _np
import pandas as _pd
import re as _re
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

class GSIstat(object):
    '''
    Object containing the GSI statistics
    '''

    def __init__(self,filename,adate):
        '''
        Initialize the GSIstat object
        INPUT:
            filename = filename of the gsistat file
            adate = analysis date
        OUTPUT:
            GSIstat: object containing the contents of the filename
        '''

        self.filename = filename
        self.analysis_date = adate

        fh = open(self.filename,'rb')
        self._lines = fh.readlines() # Keep lines private
        fh.close()

        # Initialize cache for fast parsing
        self._cache = {}

        return

    def extract(self,name):
        '''
        From the gsistat file, extract information:
        INPUT:
            name = information seeked
            Valid options are:
                ps, oz, uv, t, q, gps, rad, cost
        OUTPUT:
            df = dataframe containing information
        '''

        # If name has already been parsed,
        # just return it from cache
        if name in self._cache:
            df = self._cache[name]
            return df

        if name in ['ps']:
            df = self._get_ps()
        elif name in ['oz']:
            df = self._get_ozone()
        elif name in ['uv','t','q','gps']:
            df = self._get_conv(name)
        elif name in ['rad']:
            df = self._get_radiance()
        elif name in ['cost']:
            df = self._get_cost()
        else:
            raise IOError('option %s is not defined' % name)

        if name not in ['oz','cost']:
            df.reset_index(level='o-g',drop=True,inplace=True)

        if name not in ['oz']:
            indices = ['DATETIME'] + list(df.index.names)
            df['DATETIME'] = self.analysis_date
            df.set_index('DATETIME', append=True, inplace=True)
            df = df.reorder_levels(indices)

        self._cache[name] = df

        return df

    # Surface pressure Fit
    def _get_ps(self):
        '''
        Search for surface pressure
        '''

        pattern = 'obs\s+type\s+stype\s+count'
        for line in self._lines:
            if _re.search(pattern,line):
                header = 'o-g ' + line.strip()
                break

        tmp = []
        pattern = ' o-g (\d\d) %7s' % ('ps')
        for line in self._lines:
            if _re.match(pattern,line):
                # don't add monitored or rejected data
                if any(x in line for x in ['mon','rej']):
                    continue
                tmp.append(line.strip().split())

        columns = header.split()
        df = _pd.DataFrame(data=tmp,columns=columns)
        df[['it','type','count']] = df[['it','type','count']].astype(_np.int)
        df[['bias','rms','cpen','qcpen']] = df[['bias','rms','cpen','qcpen']].astype(_np.float)
        df.set_index(columns[:5],inplace=True)

        return df

    # Conventional Observation Fits
    def _get_conv(self,name):
        '''
        Search for uv, t, q, or gps
        '''

        # Get pressure levels
        for line in self._lines:
            if 'ptop' in line:
                ptops = _np.asarray(line.strip().split()[1:],dtype=_np.float)
            if 'pbot' in line:
                pbots = _np.asarray(line.strip().split()[5:],dtype=_np.float)
                header = 'o-g ' + line.strip()
                header = _re.sub('pbot','stat',header)
                header = _re.sub('2000.0','column',header)
                break

        tmp = []
        pattern = ' o-g (\d\d) %7s' % (name)
        for line in self._lines:
            if _re.match(pattern,line):
                # don't add monitored or rejected data
                if any(x in line for x in ['mon','rej']):
                    continue
                # don't add cpen or qcpen either
                # careful here, cpen here also removes qcpen
                # hence the extra space before qcpen and cpen
                if any(x in line for x in [' qcpen',' cpen']):
                    continue
                tmp.append(line.strip().split())

        columns = header.split()
        df = _pd.DataFrame(data=tmp,columns=columns)
        df[['it','type']] = df[['it','type']].astype(_np.int)
        df.set_index(columns[:6],inplace=True)
        df = df.astype(_np.float)

        return df

    # Ozone Fits
    def _get_ozone(self):
        '''
        Search for ozone penalty
        '''

        tmp = []
        pattern = 'ozone total'
        for line in self._lines:
            if _re.match(pattern,line):
                # remove qcpenalty
                if any(x in line for x in ['qcpenalty_all']):
                    continue
                tmp.append(line)

        oz = tmp
        return oz

    # Radiances
    def _get_radiance(self):
        '''
        Search for radiance summary statistics
        '''

        # Get header
        pattern = 'it\s+satellite\s+instrument\s+'
        for line in self._lines:
            if _re.search(pattern,line):
                header = _re.sub('#',' ',line)
                header = 'o-g ' + header.strip()
                break

        tmp = []
        pattern = 'o-g (\d\d) %3s' % ('rad')
        for line in self._lines:
            if _re.match(pattern,line):
                # don't add monitored or rejected data
                if any(x in line for x in ['mon','rej']):
                    continue
                line = _re.sub('rad',' ',line)
                tmp.append(line.strip().split())

        columns = header.split()
        df = _pd.DataFrame(data=tmp,columns=columns)
        df[['it','read','keep','assim']] = df[['it','read','keep','assim']].astype(_np.int)
        df[['penalty','qcpnlty','cpen','qccpen']] = df[['penalty','qcpnlty','cpen','qccpen']].astype(_np.float)
        df.set_index(columns[:4],inplace=True)
        df = df.swaplevel('satellite','instrument')

        return df

    # Minimization
    def _get_cost(self):
        '''
        Search for minimization and cost function information
        '''

        tmp = []
        pattern = 'costterms Jb,Jo,Jc,Jl'
        for line in self._lines:
            if _re.match(pattern,line):
                tmp.append(line.strip().split('=')[-1].split())

        columns = ['Outer','Inner','Jb','Jo','Jc','Jl']
        df = _pd.DataFrame(data=tmp,columns=columns)
        df[['Outer','Inner',]] = df[['Outer','Inner']].astype(_np.int)
        df.set_index(columns[:2],inplace=True)
        df = df.astype(_np.float)
        df['J'] = df.sum(axis=1)

        tmp = []
        pattern = 'cost,grad,step,b,step'
        for line in self._lines:
            if _re.match(pattern,line):
                tmp.append(line.strip().split('=')[-1].split()[3])

        s = _pd.Series(data=tmp,index=df.index)
        s = s.astype(_np.float)
        df.loc[:,'gJ'] = s

        return df
