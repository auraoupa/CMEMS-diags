import xarray as xr
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import sys
sys.path.insert(0,"/home/albert7a/git/cmclimate")
import cmclimate
import os
matplotlib.rcParams['figure.figsize']= (20, 8)
matplotlib.rcParams['xtick.labelsize']= 14
matplotlib.rcParams['ytick.labelsize']= 14
matplotlib.rcParams['axes.labelsize']= 16
import numpy.ma as ma
import glob



def binning_gradients(data, lon_res=0.05, lat_res=0.05,
                            lon_min=0., lon_max=360.,
                            lat_min=-80., lat_max=80,
                            min_nobs=100):
    lon_bins = np.arange(lon_min, lon_max, lon_res)
    lon_labels = lon_bins[:-1] - np.diff(lon_bins) / 2
    lat_bins = np.arange(lat_min, lat_max, lat_res)
    lat_labels = lat_bins[:-1] - np.diff(lat_bins) / 2
    mean_gradients = []
    total_nobs = []
    lat_values = []
    vo=data['vohgradb']
    vo.coords['nav_lat']=data.nav_lat
    vo.coords['nav_lon']=data.nav_lon
    for i, ds in list(vo.groupby_bins('nav_lat', lat_bins, 
                                        labels=lat_labels, 
                                        include_lowest=True)):
        try:
            group = ds.groupby_bins('nav_lon', lon_bins, 
                                    labels=lon_labels, 
                                    include_lowest=True)
            bins = group.median().sortby('nav_lon_bins')
            nobs = group.count().sortby('nav_lon_bins')
            mean_gradients.append(bins)
            total_nobs.append(nobs)
            lat_values.append(i)
        except (ValueError, StopIteration, KeyError):
            dummy_array = xr.DataArray(np.full(len(lon_labels), 
                                               np.nan), 
                                       dims='nav_lon_bins',
                                       coords={'nav_lon_bins': 
                                               ('nav_lon_bins', lon_labels)
                                              }
                                      )
            mean_gradients.append(dummy_array)
            lat_values.append(i)
    res_bins = (xr.concat(mean_gradients, dim='nav_lat')
                  .assign_coords(nav_lat=lat_values)
                  .rename({'nav_lon_bins': 'nav_lon'})
                  .sortby('nav_lat')
               )
    res_obs = (xr.concat(total_nobs, dim='nav_lat')
                 .assign_coords(nav_lat=lat_values)
                 .rename({'nav_lon_bins': 'nav_lon'})
                 .sortby('nav_lat')
              )

    return xr.Dataset({'vohgradb':res_bins, 'nobs':res_obs})

ds_hgradT_JFM=xr.open_dataset('/scratch/cnt0024/hmg2840/albert7a/NATL60/NATL60-CJM165-S/filt/NATL60-CJM165_y2013m01-m03.1d_hgradT_filt-n80-f0.1.nc')

binned_temperature_gradients = binning_gradients(ds_hgradT_JFM, lon_res=1, lat_res=1,lon_min=-87,lon_max=20,lat_min=26,lat_max=68)

binned_temperature_gradients.to_netcdf('/scratch/cnt0024/hmg2840/albert7a/NATL60/NATL60-CJM165-S/filt/NATL60-CJM165_JFM_hgradT_filt10km_bin1x1.nc')


ds_hgradT_JAS=xr.open_dataset('/scratch/cnt0024/hmg2840/albert7a/NATL60/NATL60-CJM165-S/filt/NATL60-CJM165_y2013m06-m08.1d_hgradT_filt-n80-f0.1.nc')

binned_temperature_gradients = binning_gradients(ds_hgradT_JAS, lon_res=1, lat_res=1,lon_min=-87,lon_max=20,lat_min=26,lat_max=68)

binned_temperature_gradients.to_netcdf('/scratch/cnt0024/hmg2840/albert7a/NATL60/NATL60-CJM165-S/filt/NATL60-CJM165_JAS_hgradT_filt10km_bin1x1.nc')

ds_hgradS_JFM=xr.open_dataset('/scratch/cnt0024/hmg2840/albert7a/NATL60/NATL60-CJM165-S/filt/NATL60-CJM165_y2013m01-m03.1d_hgradS_filt-n80-f0.1.nc')

binned_temperature_gradients = binning_gradients(ds_hgradS_JFM, lon_res=1, lat_res=1,lon_min=-87,lon_max=20,lat_min=26,lat_max=68)

binned_temperature_gradients.to_netcdf('/scratch/cnt0024/hmg2840/albert7a/NATL60/NATL60-CJM165-S/filt/NATL60-CJM165_JFM_hgradS_filt10km_bin1x1.nc')


ds_hgradS_JAS=xr.open_dataset('/scratch/cnt0024/hmg2840/albert7a/NATL60/NATL60-CJM165-S/filt/NATL60-CJM165_y2013m06-m08.1d_hgradS_filt-n80-f0.1.nc')

binned_temperature_gradients = binning_gradients(ds_hgradS_JAS, lon_res=1, lat_res=1,lon_min=-87,lon_max=20,lat_min=26,lat_max=68)

binned_temperature_gradients.to_netcdf('/scratch/cnt0024/hmg2840/albert7a/NATL60/NATL60-CJM165-S/filt/NATL60-CJM165_JAS_hgradS_filt10km_bin1x1.nc')








