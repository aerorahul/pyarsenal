#!/usr/bin/env python

'''
lib_GSI.py contains utility functions for GSI
'''

__all__ = ['GSIstat']


import numpy as _np
import pandas as _pd
import re as _re


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

        # Drop the o-g from the indicies list
        if 'o-g' in list(df.index.names):
            df.reset_index(level='o-g',drop=True,inplace=True)

        # Add datetime index
        df = self._add_datetime_index(df)

        # Cache it for faster access
        self._cache[name] = df

        return df

    def _add_datetime_index(self,df):
        '''
        Add the datetime as the first index
        INPUT:
            df = dataframe without datetime index
        OUTPUT:
            df = dataframe with datetime as the 1st index
        '''

        # If date is already present, return
        if 'date' in list(df.index.names):
            return df

        indices = ['date'] + list(df.index.names)
        df['date'] = self.analysis_date
        df.set_index('date', append=True, inplace=True)
        df = df.reorder_levels(indices)

        return df

    def extract_instrument(self,obtype,instrument):
        '''
        From the gsistat file, extract detailed information on an instrument:
        INPUT:
            obtype     = observation type to extract (rad or oz)
            instrument = instrument name [must be in the observation type]
            E.g.:
                amsua, mhs, iasi, hirs, etc
        OUTPUT:
            df = dataframe containing information
        '''

        # If instrument has already been parsed,
        # just return it from cache
        if instrument in self._cache:
            df = self._cache[instrument]
            return df

        # Ensure obtype is already called,
        # if not call it and cache it
        if obtype in self._cache.keys():
            otype = self._cache[obtype]
        else:
            otype = self.extract(obtype)
            self._cache[obtype] = otype

        instruments = sorted(otype.index.get_level_values('instrument').unique())
        satellites  = sorted(otype.index.get_level_values('satellite' ).unique())

        if instrument not in instruments:
            print 'Instrument %s not found!' % instrument
            print '%s contains ...' % self.filename
            print ', '.join(str(x) for x in instruments)
            return None

        # Handle special instruments
        if instrument in ['iasi','iasi616']:
            inst = 'iasi616'
        elif instrument in ['airs','airs281SUBSET']:
            inst = 'airs281SUBSET'
        else:
            inst = instrument

        tmp = []
        pattern = '\s+\d+\s+\d+\s+%s_\S+\s+\d+\s+\d+\s+' % (inst)
        for line in self._lines:
            if _re.match(pattern,line):
                tst = line.strip().split()
                tst = tst[:2] + tst[2].split('_') + tst[3:]
                tmp.append(tst)

        columns = ['it','channel','instrument','satellite','nassim','nrej','oberr','OmF_bc','OmF_wobc','col1','col2','col3']
        df = _pd.DataFrame(data=tmp,columns=columns)
        df.drop(['col1','col2','col3'],inplace=True,axis=1)
        df[['channel','nassim','nrej']] = df[['channel','nassim','nrej']].astype(_np.int)
        df[['oberr','OmF_bc','OmF_wobc']] = df[['oberr','OmF_bc','OmF_wobc']].astype(_np.float)

        # Since iteration number is not readily available, make one
        lendf = len(df)
        nouter = lendf / len(df['it'].unique())
        douter = lendf / nouter
        it = _np.zeros(lendf,dtype=int)
        for i in range(nouter):
            its = douter * i
            ite = douter * (i+1)
            it[its:ite] = i+1
        df['it'] = it

        df = df[['it','instrument','satellite','channel','nassim','nrej','oberr','OmF_bc','OmF_wobc']]
        df.set_index(['it','instrument','satellite','channel'],inplace=True)

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
        Search for ozone summary statistics
        '''

        # Get header
        pattern = 'it\s+sat\s+inst\s+'
        for line in self._lines:
            if _re.search(pattern,line):
                header = _re.sub('#',' ',line)
                header = 'o-g ' + header.strip()
                break

        tmp = []
        pattern = 'o-g (\d\d) %2s' % ('oz')
        for line in self._lines:
            if _re.match(pattern,line):
                # don't add monitored or rejected data
                if any(x in line for x in ['mon','rej']):
                    continue
                line = _re.sub('oz',' ',line)
                tmp.append(line.strip().split())

        columns = header.split()
        df = _pd.DataFrame(data=tmp,columns=columns)
        df[['it','read','keep','assim']] = df[['it','read','keep','assim']].astype(_np.int)
        df[['penalty','cpen','qcpen','qcfail']] = df[['penalty','cpen','qcpen','qcfail']].astype(_np.float)
        df.set_index(columns[:4],inplace=True)
        df = df.swaplevel('sat','inst')
        df.index.rename(['satellite','instrument'],level=['sat','inst'],inplace=True)

        return df

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


def kt_def():
    '''
    These values of kt are taken from GMAO.
    Some may be consistent with NCEP, others need careful examination
    Use at your own risk!
    '''
    kt = {
        4   : ['u', 'Upper-air zonal wind', 'm/sec'],
        5   : ['v', 'Upper-air meridional wind','m/sec'],
        11  : ['q', 'Upper-air specific humidity','g/kg'],
        12  : ['w10', 'Surface (10m) wind speed','m/sec'],
        17  : ['rr', 'Rain Rate','mm/hr'],
        18  : ['tpw', 'Total Precipitable Water',''],
        21  : ['col_o3', 'Total column ozone','DU'],
        22  : ['lyr_o3', 'Layer ozone','DU'],
        33  : ['ps', 'Surface (2m) pressure','hPa'],
        39  : ['sst', 'Sea-surface temperature','K'],
        40  : ['Tb', 'Brightness temperature','K'],
        44  : ['Tv', 'Upper-air virtual temperature','K'],
        89  : ['ba', 'Bending Angle','N'],
        101 : ['zt', 'Sub-surface temperature','C'],
        102 : ['zs', 'Sub-surface salinity',''],
        103 : ['ssh', 'Sea-surface height anomaly','m'],
        104 : ['zu', 'Sub-surface zonal velocity','m/s'],
        105 : ['zv', 'Sub-surface meridional velocity','m/s'],
        106 : ['ss', 'Synthetic Salinity','']
    }
    return kt

def kx_def():
    '''
    These values of kx are taken from GMAO.
    Some may be consistent with NCEP, others need careful examination
    Use at your own risk!
    '''
    kx = {}
    for key in [120,220]:
        kx[key] = 'Radiosonde'
    for key in [221,229]:
        kx[key] = 'PIBAL'
    for key in [132,182,232]:
        kx[key] = 'Dropsonde'
    for key in [130,230]:
        kx[key] = 'AIREP'
    for key in [131,231]:
        kx[key] = 'ASDAR'
    for key in [133,233]:
        kx[key] = 'MDCARS'
    for key in [180,280]:
        kx[key] = 'Ship'
    for key in [282]:
        kx[key] = 'Moored_Buoy'
    for key in [181]:
        kx[key] = 'Land_Surface'
    for key in [187]:
        kx[key] = 'METAR'
    for key in [199,299]:
        kx[key] = 'Drifting_Buoy'
    for key in [223]:
        kx[key] = 'Profiler_Wind'
    for key in [224]:
        kx[key] = 'NEXRAD_Wind'
    for key in [242,243,245,246,250,252,253]:
        kx[key] = 'Geo_Wind'
    for key in [244]:
        kx[key] = 'AVHRR_Wind'
    for key in [257,258,259]:
        kx[key] = 'MODIS_Wind'
    for key in [285]:
        kx[key] = 'RAPIDSCAT_Wind'
    for key in [290]:
        kx[key] = 'ASCAT_Wind'
    for key in [3,4,42,43,722,740,741,743,744,745]:
        kx[key] = 'GPSRO'
    for key in [112,210]:
        kx[key] = 'TCBogus'

    return kx
