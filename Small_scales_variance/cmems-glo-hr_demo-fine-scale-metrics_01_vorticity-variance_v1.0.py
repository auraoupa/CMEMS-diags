
# coding: utf-8

# # Fine scale variance of surface relative vorticity
# 
# 
# __author__ : Aurélie Albert & Julien Le Sommer (MEOM)
# 
# __context__ : 22-GLO-HR project : Lot 1 - Ocean Modelling
# 
# __date__ : 30 May 2017
# 
# __purpose__ : Metric for the intensity of the fine scale of surface relative vorticity in NATL60-CJM165 simulation
# 
# __detailed description__ : 
# Fine scale variance is defined at a given time and space by :
# 
# $$V(X) = (X - \langle X \rangle)^{2}$$
# 
# with $\langle . \rangle$ the low pass filtering operator. An average in time and space of the variance is then defined as : 
# 
# $$\overline{(X(t)-\langle X \rangle)^{2}}^{t,x,y}$$
# 
# with $\overline{X}^{t,x,y}$ a boxcar averager.
# 
# __practical steps__ :
# 
#   * Input data are NATL60-CJM165 daily outputs of surface relative vorticity (computed from U and V fields with cdfcurl cdftool : https://github.com/meom-group/CDFTOOLS) for the month March and September 2013
#   * step 1. : Snapshots of relative vorticity (15 March - 15 October 2013 )
#   * step 2. : Filtering of input data is performed with Lanczos2DHighPassFilter.py on command line so that the filtered signal is kept in netcdf files equivalent to input data
#   * step 3. : Variance of the high-pass filtered relative surface vorticity and boxcar averaging in 1°x1°x1 month boxes
#   * step 4. : Maps of fine scale variance of relative vorticity in March and October 2013
#   
# __external libraries needed to run this script__ : 
# 
#  * GriddedData : https://github.com/lesommer/codes/blob/master/GriddedData.py
#  * WavenumberSpectrum : https://github.com/lesommer/codes/blob/master/WavenumberSpectrum.py
#  * oocgcm filtering module : https://github.com/lesommer/oocgcm
#  
# __licence__ : This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.

# ## 0. Importing external modules

# In[41]:

## magics

get_ipython().magic(u'load_ext version_information')
get_ipython().magic(u'version_information numpy,xarray,netCDF4')


# In[42]:

## path for mdules

import sys
sys.path.insert(0,"/home/albert/lib/python")


# In[43]:

## imports

import numpy as np
import dask
import xarray as xr
import GriddedData
import time


# In[44]:

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
get_ipython().magic(u'matplotlib inline')


# ## 1. Snapshots of relative vorticity (15 March - 15 October 2013 )

# In[6]:

## Dataset

dir="/media/extra/DATA/NATL60/NATL60-CJM165-S/"
files03="NATL60-CJM165_y2013m03d*.1d_curloverf.nc"
files09="NATL60-CJM165_y2013m09d*.1d_curloverf.nc"

tfiles03=dir+files03
tfiles09=dir+files09

get_ipython().system(u'ls $tfiles03')
get_ipython().system(u'ls $tfiles09')


# In[7]:

gridfile="/media/extra/DATA/NATL60/NATL60-I/NATL60_grid.nc"
get_ipython().system(u'ls $gridfile')
grid=xr.open_dataset(gridfile)
navlat= grid['nav_lat']
navlon= grid['nav_lon']


# In[10]:

def load_and_plot(tfile,title):
    '''  load one daily file and plot the surface field
        
    '''
    curls = xr.open_dataset(tfile)
    curl15=curls['socurloverf'][0]
    navlat= curls['nav_lat']
    navlon= curls['nav_lon']
    cont=np.isnan(curl15)
    
    plt.figure(figsize=(15,11))
    ax = plt.subplot(111)
    ax.autoscale(tight=True)
    pcolor = ax.pcolormesh(navlon,navlat,
      ma.masked_invalid(curl15),cmap=div_cmap,vmin=-1,vmax=1,alpha=1)
    ax.tick_params(labelsize=25)
    ax.contour(navlon,navlat,cont,alpha=0.5,linewidth=0.000001,antialiased=True)
    cbar = plt.colorbar(pcolor,orientation='horizontal',pad=0.1)
    cbar.ax.tick_params(labelsize=35)
    ax.set_xlabel('Longitude (in degree)',fontsize=20)
    ax.set_ylabel('Latitude (in degree)',fontsize=20)
    cbar.ax.tick_params(labelsize=25)
    plt.title(title,fontsize=25)
    


# In[11]:

files0315="NATL60-CJM165_y2013m03d15.1d_curloverf.nc"
tfiles0315=dir+files0315

load_and_plot(tfiles0315,'Relative surface vorticity NATL60-CJM165 15-March-2013')


# In[12]:

files0915="NATL60-CJM165_y2013m09d15.1d_curloverf.nc"
tfiles0915=dir+files0915

load_and_plot(tfiles0915,'Relative surface vorticity NATL60-CJM165 15-September-2013')


# ## 2. Filtering of input data

# We used Lanczos2DHighPassFilter.py script to filter vorticity files with the options n=80 (size of Lanczos window) and f=0.0125 (cut-off frequency) : 
# 
# ```
# python Lanczos2DHighPassFilter.py -v 'socurloverf' -s  /media/extra/DATA/NATL60/NATL60-CJM165-S/NATL60-CJM165_y2013m03d*.1d_curloverf.nc 80 0.0125
# ```
# 
# These parameters have been chosen for NATL60 outputs, they have to be tuned regarding the resolution of the data.
# A spectra of the resulting filtered signal compared to the total signal confirm that the filter has the wanted effective cut-off frequency and a clean energy separation.

# In[55]:

# compute the spectra over 10°x10° box for one example file

dir="/media/extra/DATA/NATL60/NATL60-CJM165-S/"
test_file="NATL60-CJM165_y2013m03d01.1d_curloverf.nc"
tf_test_file="NATL60-CJM165_y2013m03d01.1d_curloverf_filt-n80-f0.0125.nc"
test=dir+test_file
tf_test=dir+tf_test_file

gridfile="/media/extra/DATA/NATL60/NATL60-I/NATL60_grid.nc"

ds = xr.open_dataset(test)
hpds = xr.open_dataset(tf_test)
grid=xr.open_dataset(gridfile)

navlon = np.array(grid["nav_lon"]).squeeze()
navlat = np.array(grid["nav_lat"]).squeeze()

curl = ds['socurloverf']
hpcurl = hpds['socurloverf_filt']


zfull = curl[0,600:1200,1800:2400].values # si pas .values plot ok mais ne peut pas calculer le spectre
zfull[np.where(np.isnan(zfull))]=0. # 0. are missing values so they are converted to nan

zhp = hpcurl[0,600:1200,1800:2400].values
zhp[np.where(np.isnan(zhp))]=0. # 0. are missing values so they are converted to nan

zlp = zfull - zhp

zlon = navlon[600:1200,1800:2400]
zlat = navlat[600:1200,1800:2400]

#- compute the wavenumber spectrum
interp = 'basemap'

def compute_spectrum(var):
    data = var.squeeze()
    x_reg,y_reg,data_reg = ws.interpolate(data,zlon,zlat,interp=interp)
    pspec,kstep = ws.get_spectrum_1d(data_reg,x_reg,y_reg)
    return pspec, kstep

get_ipython().magic(u'time spectre_full = compute_spectrum(zfull)')
get_ipython().magic(u'time spectre_hp   = compute_spectrum(zhp)')
get_ipython().magic(u'time spectre_lp   = compute_spectrum(zlp)')

#- plot the mean spectrum 
rad2cyc = 1.E3 / np.pi / 2. 

def nice_spectrum(spectre_full,spectre_hp,spectre_lp):
    fig, axarr = plt.subplots(1,1)
    fig.set_figheight(8)
    fig.set_figwidth(15)
    #
    pspec,kstep = spectre_full
    pspec_lp,kstep_lp = spectre_lp
    pspec_hp,kstep_hp = spectre_hp
    skstep = kstep * rad2cyc
    y_min = 10 ** np.floor(np.log10(pspec.min())-1)
    y_max = 10 ** np.ceil( np.log10(pspec.max())+1)
    axarr.plot(skstep[1:], pspec[1:],'k-', lw=3, label='Full relative vorticity')
    axarr.plot(skstep[1:], pspec_lp[1:],'r-', lw=3, label='Low passed relative vorticity f=0.0125 n=80')
    axarr.plot(skstep[1:], pspec_hp[1:],'b-', lw=3, label='Full - Low passed  f=0.0125 n=80')
    axarr.set_xscale('log')
    axarr.set_yscale('log')
    axarr.set_xbound(1e-5*rad2cyc, 1e-2*rad2cyc)
    axarr.set_ybound(y_min, y_max)
    axarr.set_title('',fontsize=20)
    axarr.grid(True,which='both',ls='-')
    axarr.axis('tight')
    axarr.legend(loc="lower left", fontsize=25)
    axarr.tick_params(labelsize=25)


nice_spectrum(spectre_full,spectre_hp,spectre_lp)


# In[16]:

dir="/media/extra/DATA/NATL60/NATL60-CJM165-S/"
filt_files03="NATL60-CJM165_y2013m03d*.1d_socurloverf_filt2deg_fc80-n80.nc"
filt_files09="NATL60-CJM165_y2013m09d*.1d_socurloverf_filt2deg_n120.nc"

tf_files03=dir+filt_files03
tf_files09=dir+filt_files09

get_ipython().system(u'ls $tf_files03')
get_ipython().system(u'ls $tf_files09')


# ## 3. Variance of the high-pass filtered relative surface vorticity and boxcar averaging in 1°x1°x1 month boxes

# In[50]:

def fine_scale_variance(files):
    ''' from a list of files containing one month of data compute variance and average in 1°x1°x1 month boxes
    '''
    hpcurl = xr.open_mfdataset(files,concat_dim='time_counter',decode_times=False)['socurloverf']
    hpcurl2 = hpcurl ** 2
    hpcurl2m = hpcurl2.mean(axis=0,keep_attrs=True)
    navlat2=np.array(navlat).squeeze()
    navlon2=np.array(navlon).squeeze()
    mgrd = GriddedData.grid2D(navlat=navlat2, navlon=navlon2)
    crs = GriddedData.grdCoarsener(mgrd,crs_factor=60)
    hpcurl2mc = crs.return_ravel(np.asarray(hpcurl2m))
    hpcurl2mcm = np.mean(hpcurl2mc,axis=-3)
    latcrs=crs.return_ravel(np.asarray(navlat2))
    loncrs=crs.return_ravel(np.asarray(navlon2))
    latcrsm=np.mean(latcrs,axis=-3)
    loncrsm=np.mean(loncrs,axis=-3)
    return loncrsm,latcrsm,hpcurl2mcm,hpcurl2m



# In[52]:

loncrsm03, latcrsm03, boxvarcurl03, hpvarm03 = fine_scale_variance(tf_files03)


# In[51]:

loncrsm09, latcrsm09, boxvarcurl09, hpvarm09  = fine_scale_variance(tf_files09)


# ## 4. Maps of fine scale variance of relative vorticity in March and October 2013

# In[53]:

def plot_fine_scale_variance(var,loncrs,latcrs,lon,lat,hpvarm,month):
    ''' map of the averaged fine scale variance
    '''
    fig = plt.figure(figsize=(15,11))
    ax = plt.subplot(111)
    ax.autoscale(tight=True)
    cont=np.isnan(hpvarm)

    pcolor = ax.pcolormesh(loncrs,latcrs,ma.masked_invalid(var),cmap=seq_cmap,vmin=0,vmax=0.1,alpha=1)
    ax.tick_params(labelsize=25)
    ax.contour(lon,lat,cont,alpha=0.5,linewidth=0.000001,antialiased=True)
    cbar = plt.colorbar(pcolor,orientation='horizontal',pad=0.1)
    cbar.ax.tick_params(labelsize=35)
    ax.set_xlabel('Longitude (in degree)',fontsize=20)
    ax.set_ylabel('Latitude (in degree)',fontsize=20)
    cbar.ax.tick_params(labelsize=25)
    cbar.set_label('Small scales relative vorticity variance in '+month,fontsize=25)
    plt.savefig('fine_scale_variance_socurloverf_NATL60-CJM165_'+month+'.png')
  


# In[54]:

plot_fine_scale_variance(boxvarcurl03,loncrsm03, latcrsm03,navlon,navlat,hpvarm03,'March')


# In[40]:

plot_fine_scale_variance(boxvarcurl09,loncrsm09, latcrsm09,navlon,navlat,hpvarm09,'September')

