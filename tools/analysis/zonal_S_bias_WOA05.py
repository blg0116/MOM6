#!/usr/bin/env python

import netCDF4
import numpy
import m6plot
import matplotlib.pyplot as plt

try: import argparse
except: raise Exception('This version of python is not new enough. python 2.7 or newer is required.')

parser = argparse.ArgumentParser(description='''Script for plotting annual-average zonal salinity bias.''')
parser.add_argument('annual_file', type=str, help='''Annually-averaged file containing 3D 'salt' and 'e'.''')
parser.add_argument('-l','--label', type=str, default='', help='''Label to add to the plot.''')
parser.add_argument('-o','--outdir', type=str, default='.', help='''Directory in which to place plots.''')
parser.add_argument('-g','--gridspecdir', type=str, required=True,
  help='''Directory containing mosaic/grid-spec files (ocean_hgrid.nc and ocean_mask.nc).''')
parser.add_argument('-w','--woa', type=str, required=True,
  help='''File containing WOA (or obs) data to compare against.''')
cmdLineArgs = parser.parse_args()

rootGroup = netCDF4.Dataset( cmdLineArgs.annual_file )
if 'salt' not in rootGroup.variables: raise Exception('Could not find "salt" in file "%s"'%(cmdLineArgs.annual_file))

y = netCDF4.Dataset(cmdLineArgs.gridspecdir+'/ocean_hgrid.nc').variables['y'][1::2,1::2].max(axis=-1)
msk = netCDF4.Dataset(cmdLineArgs.gridspecdir+'/ocean_mask.nc').variables['mask'][:]
area = msk*netCDF4.Dataset(cmdLineArgs.gridspecdir+'/ocean_hgrid.nc').variables['area'][:,:].reshape([msk.shape[0], 2, msk.shape[1], 2]).sum(axis=-3).sum(axis=-1)
basin = netCDF4.Dataset(cmdLineArgs.gridspecdir+'/basin_codes.nc').variables['basin'][:]

def zonalAverage(T, eta, area, mask=1.):
  vols = ( mask * area ) * ( eta[:-1] - eta[1:] ) # mask * area * level thicknesses
  return numpy.sum( vols * T, axis=-1 ) / numpy.sum( vols, axis=-1 ), (mask*eta).min(axis=-1)

Sobs = netCDF4.Dataset( cmdLineArgs.woa ).variables['salt'][:]
Zobs = netCDF4.Dataset( cmdLineArgs.woa ).variables['eta'][:]

variable = rootGroup.variables['salt']
if variable.shape[0]>1:
  Smod = variable[:,:].mean(axis=0)
  Zmod = rootGroup.variables['e'][0]
else:
  Smod = variable[0]
  Zmod = rootGroup.variables['e'][0]

ci=m6plot.pmCI(0.125,2.25,.25)

# Global
sPlot, z = zonalAverage(Smod, Zmod, area)
sObsPlot, _ = zonalAverage(Sobs, Zobs, area)
m6plot.yzplot( sPlot - sObsPlot , y, z, splitscale=[0., -1000., -6500.],
      suptitle=rootGroup.title+' '+cmdLineArgs.label, title='''Global zonal-average salinity bias (w.r.t. WOA'05) [ppt]''',
      clim=ci, colormap='dunnePM', centerlabels=True, extend='both',
      save=cmdLineArgs.outdir+'/S_global_xave_bias_WOA05.png')

m6plot.yzcompare( sPlot, sObsPlot , y, z, splitscale=[0., -1000., -6500.],
      suptitle=rootGroup.title+' '+cmdLineArgs.label,
      title1='Global zonal-average salinity [ppt]',
      title2='''WOA'05 salinity [ppt]''',
      clim=m6plot.linCI(20,30,10, 31,39,.5), colormap='dunneRainbow', extend='both',
      dlim=ci, dcolormap='dunnePM', dextend='both', centerdlabels=True,
      save=cmdLineArgs.outdir+'/S_global_xave_bias_WOA05.3_panel.png')

# Atlantic + Arctic
newMask = 1.*msk; newMask[ (basin!=2) & (basin!=4) ] = 0.
sPlot, z = zonalAverage(Smod, Zmod, area, mask=newMask)
sObsPlot, _ = zonalAverage(Sobs, Zobs, area, mask=newMask)
m6plot.yzplot( sPlot - sObsPlot , y, z, splitscale=[0., -1000., -6500.],
      suptitle=rootGroup.title+' '+cmdLineArgs.label, title='''Atlantic zonal-average salinity bias (w.r.t. WOA'05) [ppt]''',
      clim=ci, colormap='dunnePM', centerlabels=True, extend='both',
      save=cmdLineArgs.outdir+'/S_Atlantic_xave_bias_WOA05.png')

m6plot.yzcompare( sPlot, sObsPlot , y, z, splitscale=[0., -1000., -6500.],
      suptitle=rootGroup.title+' '+cmdLineArgs.label,
      title1='Atlantic zonal-average salinity [ppt]',
      title2='''WOA'05 salinity [ppt]''',
      clim=m6plot.linCI(20,30,10, 31,39,.5), colormap='dunneRainbow', extend='both',
      dlim=ci, dcolormap='dunnePM', dextend='both', centerdlabels=True,
      save=cmdLineArgs.outdir+'/S_Atlantic_xave_bias_WOA05.3_panel.png')

# Pacific
newMask = 1.*msk; newMask[ (basin!=3) ] = 0.
sPlot, z = zonalAverage(Smod, Zmod, area, mask=newMask)
sObsPlot, _ = zonalAverage(Sobs, Zobs, area, mask=newMask)
m6plot.yzplot( sPlot - sObsPlot , y, z, splitscale=[0., -1000., -6500.],
      suptitle=rootGroup.title+' '+cmdLineArgs.label, title='''Pacific zonal-average salinity bias (w.r.t. WOA'05) [ppt]''',
      clim=ci, colormap='dunnePM', centerlabels=True, extend='both',
      save=cmdLineArgs.outdir+'/S_Pacific_xave_bias_WOA05.png')

m6plot.yzcompare( sPlot, sObsPlot , y, z, splitscale=[0., -1000., -6500.],
      suptitle=rootGroup.title+' '+cmdLineArgs.label,
      title1='Pacific zonal-average salinity [ppt]',
      title2='''WOA'05 salinity [ppt]''',
      clim=m6plot.linCI(20,30,10, 31,39,.5), colormap='dunneRainbow', extend='both',
      dlim=ci, dcolormap='dunnePM', dextend='both', centerdlabels=True,
      save=cmdLineArgs.outdir+'/S_Pacific_xave_bias_WOA05.3_panel.png')

# Indian
newMask = 1.*msk; newMask[ (basin!=5) ] = 0.
sPlot, z = zonalAverage(Smod, Zmod, area, mask=newMask)
sObsPlot, _ = zonalAverage(Sobs, Zobs, area, mask=newMask)
m6plot.yzplot( sPlot - sObsPlot , y, z, splitscale=[0., -1000., -6500.],
      suptitle=rootGroup.title+' '+cmdLineArgs.label, title='''Indian zonal-average salinity bias (w.r.t. WOA'05) [ppt]''',
      clim=ci, colormap='dunnePM', centerlabels=True, extend='both',
      save=cmdLineArgs.outdir+'/S_Indian_xave_bias_WOA05.png')

m6plot.yzcompare( sPlot, sObsPlot , y, z, splitscale=[0., -1000., -6500.],
      suptitle=rootGroup.title+' '+cmdLineArgs.label,
      title1='Indian zonal-average salinity [ppt]',
      title2='''WOA'05 salinity [ppt]''',
      clim=m6plot.linCI(20,30,10, 31,39,.5), colormap='dunneRainbow', extend='both',
      dlim=ci, dcolormap='dunnePM', dextend='both', centerdlabels=True,
      save=cmdLineArgs.outdir+'/S_Indian_xave_bias_WOA05.3_panel.png')