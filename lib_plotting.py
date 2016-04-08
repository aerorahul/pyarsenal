#!/usr/bin/env python

###############################################################
# < next few lines under version control, D O  N O T  E D I T >
# $Date$
# $Revision$
# $Author$
# $Id$
###############################################################

'''
plotting.py contains plotting related functions
'''

__author__    = "Rahul Mahajan"
__email__     = "rahul.mahajan@noaa.gov"
__copyright__ = "Copyright 2016, NOAA / NCEP / EMC"
__license__   = "GPL"
__status__    = "Prototype"
__version__   = "0.1"
__all__       = ['rescale_cmap','make_cmap_from_RGB','make_cmap_from_NCARG',
                 'savefigure',
                 'get_region_bounds','get_plev_bounds','tripolar_to_latlon',
                 'plot_zonal_mean']

import os as _os
import numpy as _np
from matplotlib import cm as _cm
from matplotlib import pyplot as _pyplot
from matplotlib import colors as _colors
from matplotlib import ticker as _ticker

def rescale_cmap(cntrs,cmap='jet'):
    '''
    Rescale a colormap given the contours and colormap and
    return a rescaled colormap and norm
    '''

    cmap = _cm.get_cmap('cmap')

    ncolors  = cntrs.shape[0] + 1
    colors   = []
    for i in range(ncolors):
        color = cmap(1.0 * i/ncolors)
        colors.append(color)

    new_colors = colors[1:-1]
    new_cmap   = _colors.ListedColormap(new_colors)
    new_cmap.set_under(colors[0])
    new_cmap.set_over(colors[-1])
    new_cmap.set_bad('0.75',1.0)

    norm = _colors.BoundaryNorm(cntrs, new_cmap.N)

    return new_cmap, norm

def make_cmap_from_RGB(name='BlueYellowRed'):
    '''
    Create a colormap from a RGB file
    This is particularly useful when you can download an exotic
    RGB file off the internet
    '''

    dir_rgb = '/home/rmahajan/svn-work/python_lib/colormaps'
    filename = '%s/%s.rgb' % (dir_rgb,name)

    try:
        palette = open(filename)
    except IOError:
        raise IOError('Cannot read RGB file for %s from %s' % (name,dir_rgb))

    lines = palette.readlines()
    ncolors = len(lines)

    carray = _np.zeros([ncolors, 3])
    for num, line in enumerate(lines):
        carray[num, :] = [float(val) / 255.0 for val in line.strip().split()]
    cmap = _colors.ListedColormap(carray,name=name)
    _cm.register_cmap(name=name, cmap=cmap)

    return cmap

def make_cmap_from_NCARG(name='BlueYellowRed'):
    '''
    NCAR Graphics have some really good colormaps that you wish you could use
    '''

    dir_rgb = '%s/lib/ncarg/colormaps' % (_os.environ['NCARG_ROOT'])
    filename = '%s/%s.rgb' % (dir_rgb,name)

    try:
        palette = open(filename)
    except IOError:
        raise IOError('Cannot read RGB file for %s from %s' % (name,dir_rgb))

    lines = palette.readlines()
    tmplines = []

    for line in lines:
        line = line.strip()
        if not line: continue
        if line.startswith('#'): continue
        if 'ncolors' in line:
            ncolors = int(line.split('=')[-1])
            continue
        tmplines.append(line.split()[0:3])

    if ( len(tmplines) != ncolors ):
        raise Execption('error occurred parsing %s' % filename)
    lines = tmplines

    carray = _np.zeros([ncolors, 3])
    for num, line in enumerate(lines):
        carray[num, :] = [float(val) / 255.0 for val in line]
    cmap = _colors.ListedColormap(carray, name=name)
    _cm.register_cmap(name=name, cmap=cmap)

    return cmap

def savefigure(fname='test',format=['png','eps','pdf'],orientation='landscape',dpi=100):
    '''
    Save a figure in png, eps and pdf formats
    '''
    from matplotlib import pyplot

    if 'png' in format: pyplot.savefig(fname+'.png',format='png',dpi=1*dpi,orientation=orientation)
    if 'eps' in format: pyplot.savefig(fname+'.eps',format='eps',dpi=2*dpi,orientation=orientation)
    if 'pdf' in format: pyplot.savefig(fname+'.pdf',format='pdf',dpi=2*dpi,orientation=orientation)

    return

def get_region_bounds(lats,latbound=25.0):
    '''
    Given latitude vector (or array) and a bounding latitude, return indices of the boundaries
    '''
    if ( len(lats.shape) > 1 ): lats1 = lats[:,0]
    else:                       lats1 = lats.copy()
    latnh = lats1.tolist().index(min(lats1, key=lambda l:abs(l-latbound)))
    #latsh = lats1.tolist().index(min(lats1, key=lambda l:abs(l+latbound)))
    latsh = lats.shape[0] - latnh # since symmetric, this is same as above for latsh
    return latnh,latsh

def get_plev_bounds(plevs,plevbotbound=1013.25,plevtopbound=175.0):
    '''
    Given pressure levels and bounding levels, return indices of the boundaries
    '''
    if ( len(plevs) == 0 ): raise InputError('plevs is empty, cannot compute plev bounds')
    levbot = plevs.tolist().index(min(plevs, key=lambda l:abs(l-plevbotbound)))
    levtop = plevs.tolist().index(min(plevs, key=lambda l:abs(l-plevtopbound)))
    return [levbot,levtop]

def tripolar_to_latlon(in_lon, in_lat, in_var):
    '''
    Interpolate a variable on tripolar grid (such as MOM5) to LatLon grid
    '''

    # Make sure Longitude is monotonically increasing
    neg_lons         = in_lon < 0.0
    in_lon[neg_lons] = in_lon[neg_lons] + 360.0

    # Roll the indices by 80:
    # This has to do with the tri-polar grid; it starts at 80E (or -280)
    var_roll = _np.roll(in_var, 80, axis=1)
    lon_roll = _np.roll(in_lon, 80, axis=1)
    lat_roll = _np.roll(in_lat, 80, axis=1)

    # Shrink the 2D data in to 1D for interpolating from tri-polar to lat-lon grid
    var_1d = _np.ravel(var_roll)
    lon_1d = _np.ravel(lon_roll)
    lat_1d = _np.ravel(lat_roll)

    # Create a lat-lon uniform grid
    out_lon = _np.linspace(0.0,360.0,360.0,endpoint=False)
    out_lat = _np.linspace(-90.0,90.0,200)
    out_lon, out_lat = _np.meshgrid(out_lon, out_lat)

    # Interpolate from tri-polar to lat-lon grid and get rid of the ridiculous values
    out_var = _mlab.griddata(lon_1d, lat_1d, var_1d, out_lon, out_lat, interp='nn')
    out_var = _np.ma.masked_where(out_var > 1.1*in_var.max(), out_var)

    return out_lon, out_lat, out_var

def plot_zonal_mean(x, y, data, plotOpt=None, modelLevels=None, surfacePressure=None):
    '''
    Create a zonal mean contour plot of one variable
        plotOpt is a dictionary with plotting options:
          'scale_factor': multiply values with this factor before plotting (default: 1.0)
          'units': a units label for the colorbar (default: "")
          'levels': use list of values as contour intervals
          'title': a title for the plot (default: "Vertical cross section")
          'clevs_label_interval': how any ticks to show on colorbar (default: 1)
          'zero_contour': plot zero contour line (default: False)
        modelLevels: a list of pressure values indicating the model vertical resolution. If present,
            a small side panel will be drawn with lines for each model level
        surfacePressure: a list (dimension len(x)) of surface pressure values. If present, these will
            be used to mask out regions below the surface
    '''

    # explanation of axes:
    #   ax1: primary coordinate system latitude vs. pressure (left ticks on y axis)
    #   ax2: twinned axes for altitude coordinates on right y axis
    #   axm: small side panel with shared y axis from ax2 for display of model levels
    # right y ticks and y label will be drawn on axr if modelLevels are given, else on ax2
    #   axr: pointer to "right axis", either ax2 or axm

    if plotOpt is None: plotOpt = {}

    # create figure and axes
    fig = _pyplot.figure()
    ax1 = fig.add_subplot(111)
    # scale data if requested
    pdata = data * plotOpt.get('scale_factor', 1.0)
    # determine contour levels to be used; default: linear spacing, 21 levels
    clevs = plotOpt.get('levels', _np.linspace(data.min(), data.max(), 21))
    # map contour values to colors
    norm=_colors.BoundaryNorm(clevs, ncolors=plotOpt.get('ncolors',20), clip=False)
    # draw the (filled) contours
    contour = ax1.contourf(x, y, pdata, levels=clevs, norm=norm)
    if plotOpt.get('zero_contour',False):
        contourz = ax1.contour(x, y, pdata, colors='k', linewidths=2.0,levels=[0.0])
    # mask out surface pressure if given
    if not surfacePressure is None:
        ax1.fill_between(x, surfacePressure, surfacePressure.max(), color="white")
    # add a title
    title = plotOpt.get('title', 'Vertical cross section')
    ax1.set_title(title)
    # add colorbar
    # Note: use of the ticks keyword forces colorbar to draw all labels
    fmt = _ticker.FormatStrFormatter("%4.2g")
    clevs_label_interval = plotOpt.get('clevs_label_interval',1)
    cbar = fig.colorbar(contour, ax=ax1, orientation='horizontal', shrink=0.8,
                        ticks=clevs[::clevs_label_interval], format=fmt)
    cbar.set_label(plotOpt.get('units', ''))
    for t in cbar.ax.get_xticklabels():
        t.set_fontsize('small')
    # set up y axes: log pressure labels on the left y axis, altitude labels
    # according to model levels on the right y axis
    ax1.set_ylabel("Pressure [hPa]")
    ax1.set_yscale('log')
    ax1.set_ylim(10.*_np.ceil(y.max()/10.), y.min()) # avoid truncation of 1000 hPa
    subs = [1,2,5]
    if y.max()/y.min() < 30.:
        subs = [1,2,3,4,5,6,7,8,9]
    y1loc = _ticker.LogLocator(base=10., subs=subs)
    ax1.yaxis.set_major_locator(y1loc)
    fmt = _ticker.FormatStrFormatter("%g")
    ax1.yaxis.set_major_formatter(fmt)
    for t in ax1.get_yticklabels():
        t.set_fontsize('small')
    # calculate altitudes from pressure values (use fixed scale height)
    z0 = 8.400    # scale height for pressure_to_altitude conversion [km]
    altitude = z0 * _np.log(1013.25/y)
    # add second y axis for altitude scale
    ax2 = ax1.twinx()
    # change values and font size of x labels
    ax1.set_xlabel('Latitude [degrees]')
    xloc = _ticker.FixedLocator(_np.arange(-90.,91.,15.))
    ax1.xaxis.set_major_locator(xloc)
    for t in ax1.get_xticklabels():
        t.set_fontsize('small')
    # draw horizontal lines to the right to indicate model levels
    if not modelLevels is None:
        pos = ax1.get_position()
        axm = fig.add_axes([pos.x1,pos.y0,0.02,pos.height], sharey=ax2)
        axm.set_xlim(0., 1.)
        axm.xaxis.set_visible(False)
        modelLev = axm.hlines(altitude, 0., 1., color='0.5')
        axr = axm     # specify y axis for right tick marks and labels
        # turn off tick labels of ax2
        for t in ax2.get_yticklabels():
            t.set_visible(False)
        label_xcoor = 3.7
    else:
        axr = ax2
        label_xcoor = 1.05
    axr.set_ylabel("Altitude [km]")
    axr.yaxis.set_label_coords(label_xcoor, 0.5)
    axr.set_ylim(altitude.min(), altitude.max())
    yrloc = _ticker.MaxNLocator(steps=[1,2,5,10])
    axr.yaxis.set_major_locator(yrloc)
    axr.yaxis.tick_right()
    for t in axr.yaxis.get_majorticklines():
        t.set_visible(False)
    for t in axr.get_yticklabels():
        t.set_fontsize('small')

    return fig
