

# # Filtering all dates, writing a file containing filtered data and plotting results
# 
# 

# ## 0. Installations required
# 
# 

# ## 1. Importing external modules


## path for mdules

import sys
sys.path.insert(0,"/home/albert/lib/python")



## imports

import numpy as np
import dask
import xarray as xr
import GriddedData
import time



#- Other modules
import os
from glob import glob
import numpy.ma as ma
import scipy as sc
import WavenumberSpectrum as ws
import dask.array as da
from netCDF4 import Dataset

### palette
from matplotlib.colors import LogNorm
import matplotlib.cm as mplcm
import colormap as cmaps
import matplotlib.cm as cm

import seaborn as sns

seq_cmap = mplcm.Blues
div_cmap = mplcm.seismic

### quick plot
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

## local/specific imports
import oocgcm
import oocgcm.filtering
import oocgcm.filtering.linearfilters as tf


# ## 2. Dataset


dir="/media/extra/DATA/NATL60/NATL60-CJM165-S/"
files03="NATL60-CJM165_y2013m03d*.1d_curloverf.nc"
files09="NATL60-CJM165_y2013m09d*.1d_curloverf.nc"

tfiles03=dir+files03
tfiles09=dir+files09



# ## 4. 2D filtering


gridfile="/media/extra/DATA/NATL60/NATL60-I/NATL60_grid.nc"
grid=xr.open_dataset(gridfile)
navlat= grid['nav_lat']
navlon= grid['nav_lon']

def plot_and_save_curl_total_filt(curl,signal_LS,t,month):
    cont=np.isnan(curl)
    plt.figure(figsize=(15,33))
    ax = plt.subplot(311)
    ax.autoscale(tight=True)
    pcolor = ax.pcolormesh(navlon,navlat,
      ma.masked_invalid(curl),cmap=div_cmap,vmin=-1,vmax=1,alpha=1)
    ax.tick_params(labelsize=25)
    ax.contour(navlon,navlat,cont,alpha=0.5,linewidth=0.000001,antialiased=True)
    cbar = plt.colorbar(pcolor,orientation='horizontal',pad=0.1)
    cbar.ax.tick_params(labelsize=35)
    ax.set_xlabel('Longitude (in degree)',fontsize=20)
    ax.set_ylabel('Latitude (in degree)',fontsize=20)
    cbar.ax.tick_params(labelsize=25)
    plt.title('Total surface relative vorticity '+str(t)+' month '+str(month),fontsize=25)
    cont=np.isnan(signal_LS)
    ax = plt.subplot(312)
    ax.autoscale(tight=True)
    pcolor = ax.pcolormesh(navlon,navlat,
      ma.masked_invalid(signal_LS),cmap=div_cmap,vmin=-1,vmax=1,alpha=1)
    ax.tick_params(labelsize=25)
    ax.contour(navlon,navlat,cont,alpha=0.5,linewidth=0.000001,antialiased=True)
    cbar = plt.colorbar(pcolor,orientation='horizontal',pad=0.1)
    cbar.ax.tick_params(labelsize=35)
    ax.set_xlabel('Longitude (in degree)',fontsize=20)
    ax.set_ylabel('Latitude (in degree)',fontsize=20)
    cbar.ax.tick_params(labelsize=25)
    plt.title('Large scale surface relative vorticity '+str(t)+' month '+str(month),fontsize=25)
    signal_SS=curl-signal_LS
    cont=np.isnan(signal_SS)
    ax = plt.subplot(313)
    ax.autoscale(tight=True)
    pcolor = ax.pcolormesh(navlon,navlat,
      ma.masked_invalid(signal_SS),cmap=div_cmap,vmin=-1,vmax=1,alpha=1)
    ax.tick_params(labelsize=25)
    ax.contour(navlon,navlat,cont,alpha=0.5,linewidth=0.000001,antialiased=True)
    cbar = plt.colorbar(pcolor,orientation='horizontal',pad=0.1)
    cbar.ax.tick_params(labelsize=35)
    ax.set_xlabel('Longitude (in degree)',fontsize=20)
    ax.set_ylabel('Latitude (in degree)',fontsize=20)
    cbar.ax.tick_params(labelsize=25)
    plt.title('Small scale surface relative vorticity '+str(t)+' month '+str(month),fontsize=25)
    figname='/media/extra/DATA/NATL60/NATL60-CJM165-PLOTS/filt_socurloverf/filtering_socurloverf_NATL60-CJM165_'+str(t)+'0'+str(month)+'.png'
    plt.savefig(figname)
    


month=3
tfiles=tfiles03
curls = xr.open_mfdataset(tfiles,concat_dim='time_counter')['socurloverf']


for t in np.arange(13,31):
    print t
    filename='/media/extra/DATA/NATL60/NATL60-CJM165-S/NATL60-CJM165_y2013m0'+str(month)+'d'+str(t+1)+'.1d_socurloverf_filt2deg_n120.nc'
    print filename
    filtset = Dataset(filename, 'w', format='NETCDF4')
    filtset.description = "NATL60 data filtered with Lanczos filter with cut-off frequency of 2deg"
    
    time=filtset.createDimension('time_counter',None)
    x=filtset.createDimension('x', 5422)
    y=filtset.createDimension('y', 3454)

    lat = filtset.createVariable('nav_lat', 'f8', ('y','x'))
    lat.standart_name="latitude"
    lat.long_name = "Latitude" 
    lat.units = "degrees_north"
    lat.nav_model = "grid_U"

    lon = filtset.createVariable('nav_lon', 'f8', ('y','x'))
    lon.standard_name = "longitude" 
    lon.long_name = "Longitude" 
    lon.units = "degrees_east" 
    lon.nav_model = "grid_U" 
    
    time = filtset.createVariable('time_counter', 'f8', ('time_counter'))
    time.axis = "T" 
    time.standard_name = "time" 
    time.long_name = "Time axis" 
    time.calendar = "gregorian" 
    time.units = "seconds since 1958-01-01 00:00:00" 
    time.time_origin = "1958-01-01 00:00:00" 
    time.bounds = "time_counter_bounds" 

    socurloverf = filtset.createVariable('socurloverf', 'f8', ('time_counter','y','x'),fill_value=0.)
    socurloverf.units = "-" 
    socurloverf.valid_min = -1000.
    socurloverf.valid_max = 1000.
    socurloverf.long_name = "Filtered Relative_Vorticity (curl)" 
    socurloverf.short_name = "socurl" 
    socurloverf.iweight = 1 
    socurloverf.online_operation = "N/A" 
    socurloverf.axis = "TYX" 
    socurloverf.scale_factor = 1.
    socurloverf.add_offset = 0.
    socurloverf.savelog10 = 0. 

    curl0=curls[t]
    win_box2D = curl0.win
    win_box2D.set(window_name='lanczos', n=[120, 120], dims=['x', 'y'], fc=0.00833)
    bw = win_box2D.boundary_weights(drop_dims=[])
    signal_LS = win_box2D.apply(weights=bw)
    plot_and_save_curl_total_filt(curl0,signal_LS,t+1,month)
    signal_SS=curl0-signal_LS
    truc=np.zeros((1,3454,5422))
    truc[0,:,:]=signal_SS[:,:]
    socurloverf[0,:,:] = truc[0,:,:]
    filtset.close()  # close the new file





