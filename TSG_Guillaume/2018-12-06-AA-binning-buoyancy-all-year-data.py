#!/usr/bin/env python
# coding: utf-8

# In[1]:


import xarray as xr
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import sys
sys.path.insert(0,"/Users/auraoupa/Work/git/cmclimate")
import cmclimate
import os
get_ipython().magic(u'matplotlib inline')
matplotlib.rcParams['figure.figsize']= (20, 8)
matplotlib.rcParams['xtick.labelsize']= 14
matplotlib.rcParams['ytick.labelsize']= 14
matplotlib.rcParams['axes.labelsize']= 16


# In[3]:


def binning_gradients(data, lon_res=0.05, lat_res=0.05, 
                            lon_min=0., lon_max=360., 
                            lat_min=-80., lat_max=80, 
                            min_nobs=100):
    # Define the latitudinal and longitudinal binning
    #lon_bins = np.arange(data['lon'].min().data
    #                     data['lon'].max().data, lon_res)
    lon_bins = np.arange(lon_min, lon_max, lon_res)
    lon_labels = lon_bins[:-1] - np.diff(lon_bins) / 2
    #lat_bins = np.arange(data['lat'].min().data,
    #                     data['lat'].max().data, lat_res)
    lat_bins = np.arange(lat_min, lat_max, lat_res)
    lat_labels = lat_bins[:-1] - np.diff(lat_bins) / 2
    mean_gradients = []
    total_nobs = []
    lat_values = []
    for i, ds in list(data.groupby_bins('lat', lat_bins, 
                                        labels=lat_labels, 
                                        include_lowest=True)):
        try:
            group = ds.groupby_bins('lon', lon_bins, 
                                    labels=lon_labels, 
                                    include_lowest=True)
            bins = group.median().sortby('lon_bins')
            nobs = group.count().sortby('lon_bins')
            mean_gradients.append(bins)
            total_nobs.append(nobs)
            lat_values.append(i)
        except (ValueError, StopIteration):
            dummy_array = xr.DataArray(np.full(len(lon_labels), 
                                               np.nan), 
                                       dims='lon_bins', 
                                       coords={'lon_bins': 
                                               ('lon_bins', lon_labels)
                                              }
                                      )
            mean_gradients.append(dummy_array)
            lat_values.append(i)
    res_bins = (xr.concat(mean_gradients, dim='lat')
                  .assign_coords(lat=lat_values)
                  .rename({'lon_bins': 'lon'})
                  .sortby('lat')
               )
    res_obs = (xr.concat(total_nobs, dim='lat')
                 .assign_coords(lat=lat_values)
                 .rename({'lon_bins': 'lon'})
                 .sortby('lat')
              )
    return xr.Dataset({data.name:res_bins, 'nobs':res_obs})


# In[4]:


ds = xr.open_dataset('/Users/auraoupa/Data/TSG/ALL_horizontal_gradients.nc', chunks={'time': 1e7})


# In[5]:


binned_buoyancy_gradients = binning_gradients(np.abs(ds['SSb' + '_LS']), lon_res=1, lat_res=1)
binned_buoyancy_gradients.to_netcdf('/Users/auraoupa/Data/TSG/ALL_buoyancy_gradients_1x1.nc')


# In[ ]:


binned_buoyancy_gradients = xr.open_dataset(path + 'GLOBAL/ALL_buoyancy_gradients_1x1_JAS.nc')
add_map(lon_min=-85, lon_max=20, lat_min=25, lat_max=70, scale='low')
binned_buoyancy_gradients['SSb_LS'].plot.pcolormesh(cmap=cmclimate.cm.BlGrYeOrReVi200, vmin=1e-9, vmax=1e-7)
plt.savefig('./Fig_3a-NATL_TSG_buoyancy_gradients_JAS_1x1.png', dpi=300, bbox_inches='tight')

