

import xarray as xr
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import sys
sys.path.insert(0,"/home/albert/git/cmclimate")
import cmclimate
import os

import seaborn as sns
sns.set(color_codes=True)

sys.path.insert(0,'/home/albert/lib/python')
from natl60_3_5_by_5_boxes import boxes
sys.path.insert(0,'/home/albert/lib/python/PowerSpec')
import plot_box as pb



ds_natl_T_surf = xr.open_dataset('/mnt/meom/workdir/albert/NATL60/NATL60-CJM165-S/filt/NATL60-CJM165_y2012m10d01-y2013m09d30.1d_hgradT_large-n80-f0.1.nc',chunks={'time_counter':1})
ds_natl_S_surf = xr.open_dataset('/mnt/meom/workdir/albert/NATL60/NATL60-CJM165-S/filt/NATL60-CJM165_y2012m10d01-y2013m09d30.1d_hgradS_large-n80-f0.1.nc',chunks={'time_counter':1})
ds_natl_b_surf = xr.open_dataset('/mnt/meom/workdir/albert/NATL60/NATL60-CJM165-S/filt/NATL60-CJM165_y2012m10d01-y2013m09d30.1d_hgradb_large-n80-f0.1.nc',chunks={'time_counter':1})




ds_natl_T_10m = xr.open_dataset('/mnt/meom/workdir/albert/NATL60/NATL60-CJM165-S/filt10m/NATL60-CJM165_y2012m10d01-y2013m09d30.1d_hgradT_10m_large-n80-f0.1.nc',chunks={'time_counter':1})
ds_natl_S_10m = xr.open_dataset('/mnt/meom/workdir/albert/NATL60/NATL60-CJM165-S/filt10m/NATL60-CJM165_y2012m10d01-y2013m09d30.1d_hgradS_10m_large-n80-f0.1.nc',chunks={'time_counter':1})
ds_natl_b_10m = xr.open_dataset('/mnt/meom/workdir/albert/NATL60/NATL60-CJM165-S/filt10m/NATL60-CJM165_y2012m10d01-y2013m09d30.1d_hgradb_10m_large-n80-f0.1.nc',chunks={'time_counter':1})



fig = plt.figure(figsize=(18.0, 12.0))

for box in boxes:
    
    gradT_surf=ds_natl_T_surf['vohgradb'][:,box.jmin:box.jmax,box.imin:box.imax].stack(z=('x', 'y','time_counter'))
    gradS_surf=ds_natl_S_surf['vohgradb'][:,box.jmin:box.jmax,box.imin:box.imax].stack(z=('x', 'y','time_counter'))
    gradb_surf=ds_natl_b_surf['vohgradb'][:,box.jmin:box.jmax,box.imin:box.imax].stack(z=('x', 'y','time_counter'))
    
    gradT_10m=ds_natl_T_10m['vohgradb'][:,box.jmin:box.jmax,box.imin:box.imax].stack(z=('x', 'y','time_counter'))
    gradS_10m=ds_natl_S_10m['vohgradb'][:,box.jmin:box.jmax,box.imin:box.imax].stack(z=('x', 'y','time_counter'))
    gradb_10m=ds_natl_b_10m['vohgradb'][:,box.jmin:box.jmax,box.imin:box.imax].stack(z=('x', 'y','time_counter'))
    
    gradT_nonan_surf=gradT_surf[~np.isnan(gradT_surf)]
    gradS_nonan_surf=gradS_surf[~np.isnan(gradS_surf)]
    gradb_nonan_surf=gradb_surf[~np.isnan(gradb_surf)]
    
    gradT_nonan_10m=gradT_10m[~np.isnan(gradT_10m)]
    gradS_nonan_10m=gradS_10m[~np.isnan(gradS_10m)]
    gradb_nonan_10m=gradb_10m[~np.isnan(gradb_10m)]
    
    axes1 = fig.add_subplot(3, 3, (box.nb-1)*3+1)
    weights_surf = np.ones_like(gradT_nonan_surf)/float(len(gradT_nonan_surf))
    med_surf=np.median(np.abs(gradT_nonan_surf))
    axes1.hist(gradT_nonan_surf,30, alpha = 0.5,range=(0,1e-4),color='r', weights=weights_surf, label='surf')
    axes1.axvline(med_surf, color='r', linestyle='dashed', linewidth=1)
    weights_10m = np.ones_like(gradT_nonan_10m)/float(len(gradT_nonan_10m))
    med_10m=np.median(np.abs(gradT_nonan_10m))
    axes1.hist(gradT_nonan_10m,30, alpha = 0.5,range=(0,1e-4),color='r', weights=weights_10m, label='10m')
    axes1.axvline(med_10m, color='r', linestyle='dashed', linewidth=1)
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    plt.xlabel('deg C / m')
    plt.legend()
    plt.title('Large scale grad T in '+box.name+' box')

    axes2 = fig.add_subplot(3, 3, (box.nb-1)*3+2)
    weights_surf = np.ones_like(gradS_nonan_surf)/float(len(gradS_nonan_surf))
    med_surf=np.median(np.abs(gradS_nonan_surf))
    axes2.hist(gradS_nonan_surf,30, alpha = 0.5,range=(0,5e-5),color='r', weights=weights_surf, label='surf')
    axes2.axvline(med_surf, color='r', linestyle='dashed', linewidth=1)
    weights_10m = np.ones_like(gradS_nonan_10m)/float(len(gradS_nonan_10m))
    med_10m=np.median(np.abs(gradS_nonan_10m))
    axes2.hist(gradS_nonan_10m,30, alpha = 0.5,range=(0,5e-5),color='r', weights=weights_10m, label='10m')
    axes2.axvline(med_10m, color='r', linestyle='dashed', linewidth=1)
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    plt.xlabel('PSU / m')
    plt.legend()
    plt.title('Large scale grad S in '+box.name+' box')

    axes3 = fig.add_subplot(3, 3, (box.nb-1)*3+3)
    weights_surf = np.ones_like(gradb_nonan_surf)/float(len(gradb_nonan_surf))
    med_surf=np.median(np.abs(gradb_nonan_surf))
    axes3.hist(gradb_nonan_surf,30, alpha = 0.5,range=(0,2e-7),color='r', weights=weights_surf, label='NATL60')
    axes3.axvline(med_surf, color='r', linestyle='dashed', linewidth=1)
    weights_10m = np.ones_like(gradb_nonan_10m)/float(len(gradb_nonan_10m))
    med_10m=np.median(np.abs(gradb_nonan_10m))
    axes3.hist(gradb_nonan_10m,30, alpha = 0.5,range=(0,2e-7),color='r', weights=weights_10m, label='NATL60')
    axes3.axvline(med_10m, color='r', linestyle='dashed', linewidth=1)
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    plt.xlabel(' m / m $s^2$')
    plt.legend()
    plt.title('Large scale grad b in '+box.name+' box')
plt.savefig('hist_grad_natl60_surf-10m.png', dpi=100, bbox_inches = 'tight')


