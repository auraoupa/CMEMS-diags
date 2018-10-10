import xarray as xr
import dask
import dask.threaded
import dask.multiprocessing
from dask.distributed import Client
c = Client()

import xarray as xr
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import sys
sys.path.insert(0,"/mnt/meom/workdir/albert/git/cmclimate")
import cmclimate
import os
matplotlib.rcParams['figure.figsize']= (20, 8)
matplotlib.rcParams['xtick.labelsize']= 14
matplotlib.rcParams['ytick.labelsize']= 14
matplotlib.rcParams['axes.labelsize']= 16
import numpy.ma as ma



ds_hgradT_J=xr.open_mfdataset('/mnt/meom/workdir/albert/NATL60/NATL60-CJM165-S/filt/NATL60-CJM165_y2013m01d??.1d_hgradT_filt-n80-f0.1.nc', concat_dim='time_counter')
ds_hgradS_J=xr.open_mfdataset('/mnt/meom/workdir/albert/NATL60/NATL60-CJM165-S/filt/NATL60-CJM165_y2013m01d??.1d_hgradS_filt-n80-f0.1.nc', concat_dim='time_counter')
ds_hgradT_F=xr.open_mfdataset('/mnt/meom/workdir/albert/NATL60/NATL60-CJM165-S/filt/NATL60-CJM165_y2013m02d??.1d_hgradT_filt-n80-f0.1.nc', concat_dim='time_counter')
ds_hgradS_F=xr.open_mfdataset('/mnt/meom/workdir/albert/NATL60/NATL60-CJM165-S/filt/NATL60-CJM165_y2013m02d??.1d_hgradS_filt-n80-f0.1.nc', concat_dim='time_counter')
ds_hgradT_M=xr.open_mfdataset('/mnt/meom/workdir/albert/NATL60/NATL60-CJM165-S/filt/NATL60-CJM165_y2013m03d??.1d_hgradT_filt-n80-f0.1.nc', concat_dim='time_counter')
ds_hgradS_M=xr.open_mfdataset('/mnt/meom/workdir/albert/NATL60/NATL60-CJM165-S/filt/NATL60-CJM165_y2013m03d??.1d_hgradS_filt-n80-f0.1.nc', concat_dim='time_counter')

ds_hgradT_JFM=xr.merge([ds_hgradT_J,ds_hgradT_F,ds_hgradT_M])
ds_hgradS_JFM=xr.merge([ds_hgradS_J,ds_hgradS_F,ds_hgradS_M])

