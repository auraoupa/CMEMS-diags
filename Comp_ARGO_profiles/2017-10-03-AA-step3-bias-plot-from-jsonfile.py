#!/usr/bin/env python
#
#
#Statistical measure of the bias of NATL60 versus hydrographic data set EN4 : step 3

# - We provide a jsonfile containing all the profiles we want to compare with NATL60
# - We get the EN4 profiles and the model equivalent from the netcdf files
# - We interpolate on a standard vertical grid
# - We produce a plot with the mean bias and percent

## path for mdules

import sys
sys.path.insert(0,"/home/albert7a/lib/python")


## imports

import numpy as np
import dask
import xarray as xr
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import glob as glob
import matplotlib.gridspec as gridspec
from mpl_toolkits.basemap import Basemap
import time
from dask.diagnostics import ProgressBar
from datetime import date
import json
import os
import warnings
warnings.filterwarnings('ignore')

def get_netcdf_profiles(jsonfile,infos,prof):
	list_profiles = infos.keys()
	reference_profile = str(list_profiles[prof])
	print 'Getting profile ', reference_profile

        namezone=jsonfile[0:-5]
	dirname="/scratch/cnt0024/hmg2840/albert7a/EN4/profiles_files/"+namezone

        netcdf_name=dirname+"/profiles_EN4-"+reference_profile[1:]+"_NATL60-CJM165_TS.nc"

        dsprof=xr.open_dataset(netcdf_name)
	
	depth_en4=dsprof['depth_en4']
	depth_model=dsprof['depth_model']
	temp_en4=dsprof['temp_profileEN4']
	salt_en4=dsprof['salt_profileEN4']
	mean_temp_model=dsprof['mean_temp_model']
	mean_salt_model=dsprof['mean_salt_model']
	percent10_temp_model=dsprof['percent10_temp_model']
	percent10_salt_model=dsprof['percent10_salt_model']
	percent90_temp_model=dsprof['percent90_temp_model']
	percent90_salt_model=dsprof['percent90_salt_model']

	

	return depth_en4,depth_model,temp_en4,salt_en4,mean_temp_model,mean_salt_model,percent10_temp_model,percent10_salt_model,percent90_temp_model,percent90_salt_model,dirname


def project_standart_vertical_levels(depth_en4,depth_model,temp_en4,salt_en4,mean_temp_model,mean_salt_model,percent10_temp_model,percent10_salt_model,percent90_temp_model,percent90_salt_model,vert_standart):

	temp_en4_standart=np.zeros(len(vert_standart))
	salt_en4_standart=np.zeros(len(vert_standart))
	mean_temp_model_standart=np.zeros(len(vert_standart))
	mean_salt_model_standart=np.zeros(len(vert_standart))
	percent10_temp_model_standart=np.zeros(len(vert_standart))
	percent10_salt_model_standart=np.zeros(len(vert_standart))
	percent90_temp_model_standart=np.zeros(len(vert_standart))
	percent90_salt_model_standart=np.zeros(len(vert_standart))

	for k in np.arange(len(vert_standart)-1):
	    zs1=vert_standart[k]
	    zs2=vert_standart[k+1]
	    zs=(zs1+zs2)/2.
	    idz=np.where(np.abs(depth_en4-zs)==np.min(np.abs(depth_en4-zs)))
	    if (idz[0]==0) | (idz[0]==len(depth_en4)-1):
	        temp_en4_standart[k]='nan'
	        salt_en4_standart[k]='nan'
	        mean_temp_model_standart[k]='nan'
	        mean_salt_model_standart[k]='nan'
	        percent10_temp_model_standart[k]='nan'
	        percent10_salt_model_standart[k]='nan'
	        percent90_temp_model_standart[k]='nan'
	        percent90_salt_model_standart[k]='nan'
	    else:
	        if depth_en4[idz[0]] < zs:
	            temp_en4_standart[k]=(1 - (zs-depth_en4[idz[0]])/(depth_en4[idz[0]+1]-depth_en4[idz[0]])) * temp_en4[idz[0]] + (1 - (depth_en4[idz[0]+1] - zs)/(depth_en4[idz[0]+1]-depth_en4[idz[0]])) * temp_en4[idz[0]+1]
	            salt_en4_standart[k]=(1 - (zs-depth_en4[idz[0]])/(depth_en4[idz[0]+1]-depth_en4[idz[0]])) * salt_en4[idz[0]] + (1 - (depth_en4[idz[0]+1] - zs)/(depth_en4[idz[0]+1]-depth_en4[idz[0]])) * salt_en4[idz[0]+1]
	            mean_temp_model_standart[k]=(1 - (zs-depth_model[idz[0]])/(depth_model[idz[0]+1]-depth_model[idz[0]])) * mean_temp_model[idz[0]] + (1 - (depth_model[idz[0]+1] - zs)/(depth_model[idz[0]+1]-depth_model[idz[0]])) * mean_temp_model[idz[0]+1]
	            mean_salt_model_standart[k]=(1 - (zs-depth_model[idz[0]])/(depth_model[idz[0]+1]-depth_model[idz[0]])) * mean_salt_model[idz[0]] + (1 - (depth_model[idz[0]+1] - zs)/(depth_model[idz[0]+1]-depth_model[idz[0]])) * mean_salt_model[idz[0]+1]
	            percent10_temp_model_standart[k]=(1 - (zs-depth_model[idz[0]])/(depth_model[idz[0]+1]-depth_model[idz[0]])) * percent10_temp_model[idz[0]] + (1 - (depth_model[idz[0]+1] - zs)/(depth_model[idz[0]+1]-depth_model[idz[0]])) * percent10_temp_model[idz[0]+1]
	            percent10_salt_model_standart[k]=(1 - (zs-depth_model[idz[0]])/(depth_model[idz[0]+1]-depth_model[idz[0]])) * percent10_salt_model[idz[0]] + (1 - (depth_model[idz[0]+1] - zs)/(depth_model[idz[0]+1]-depth_model[idz[0]])) * percent10_salt_model[idz[0]+1]
	            percent90_temp_model_standart[k]=(1 - (zs-depth_model[idz[0]])/(depth_model[idz[0]+1]-depth_model[idz[0]])) * mean_temp_model[idz[0]] + (1 - (depth_model[idz[0]+1] - zs)/(depth_model[idz[0]+1]-depth_model[idz[0]])) * mean_temp_model[idz[0]+1]
	            percent90_salt_model_standart[k]=(1 - (zs-depth_model[idz[0]])/(depth_model[idz[0]+1]-depth_model[idz[0]])) * mean_salt_model[idz[0]] + (1 - (depth_model[idz[0]+1] - zs)/(depth_model[idz[0]+1]-depth_model[idz[0]])) * mean_salt_model[idz[0]+1]
	        if depth_en4[idz[0]] > zs:
	            temp_en4_standart[k]=(1 - (zs-depth_en4[idz[0]-1])/(depth_en4[idz[0]]-depth_en4[idz[0]-1])) * temp_en4[idz[0]-1] + (1 - (depth_en4[idz[0]] - zs)/(depth_en4[idz[0]]-depth_en4[idz[0]-1])) * temp_en4[idz[0]]
	            salt_en4_standart[k]=(1 - (zs-depth_en4[idz[0]-1])/(depth_en4[idz[0]]-depth_en4[idz[0]-1])) * salt_en4[idz[0]-1] + (1 - (depth_en4[idz[0]] - zs)/(depth_en4[idz[0]]-depth_en4[idz[0]-1])) * salt_en4[idz[0]]
	            mean_temp_model_standart[k]=(1 - (zs-depth_model[idz[0]-1])/(depth_model[idz[0]]-depth_model[idz[0]-1])) * mean_temp_model[idz[0]-1] + (1 - (depth_model[idz[0]] - zs)/(depth_model[idz[0]]-depth_model[idz[0]-1])) * mean_temp_model[idz[0]]
	            mean_salt_model_standart[k]=(1 - (zs-depth_model[idz[0]-1])/(depth_model[idz[0]]-depth_model[idz[0]-1])) * mean_salt_model[idz[0]-1] + (1 - (depth_model[idz[0]] - zs)/(depth_model[idz[0]]-depth_model[idz[0]-1])) * mean_salt_model[idz[0]]
	            percent10_temp_model_standart[k]=(1 - (zs-depth_model[idz[0]-1])/(depth_model[idz[0]]-depth_model[idz[0]-1])) * percent10_temp_model[idz[0]-1] + (1 - (depth_model[idz[0]] - zs)/(depth_model[idz[0]]-depth_model[idz[0]-1])) * percent10_temp_model[idz[0]]
	            percent10_salt_model_standart[k]=(1 - (zs-depth_model[idz[0]-1])/(depth_model[idz[0]]-depth_model[idz[0]-1])) * percent10_salt_model[idz[0]-1] + (1 - (depth_model[idz[0]] - zs)/(depth_model[idz[0]]-depth_model[idz[0]-1])) * percent10_salt_model[idz[0]]
	            percent90_temp_model_standart[k]=(1 - (zs-depth_model[idz[0]-1])/(depth_model[idz[0]]-depth_model[idz[0]-1])) * percent90_temp_model[idz[0]-1] + (1 - (depth_model[idz[0]] - zs)/(depth_model[idz[0]]-depth_model[idz[0]-1])) * percent90_temp_model[idz[0]]
	            percent90_salt_model_standart[k]=(1 - (zs-depth_model[idz[0]-1])/(depth_model[idz[0]]-depth_model[idz[0]-1])) * percent90_salt_model[idz[0]-1] + (1 - (depth_model[idz[0]] - zs)/(depth_model[idz[0]]-depth_model[idz[0]-1])) * percent90_salt_model[idz[0]]
	

	return temp_en4_standart,salt_en4_standart,mean_temp_model_standart,mean_salt_model_standart,percent10_temp_model_standart,percent10_salt_model_standart,percent90_temp_model_standart,percent90_salt_model_standart




def plot_mean_percent_bias_profile(all_temp_mean_model,all_salt_mean_model,all_temp_mean_en4,all_salt_mean_en4,all_temp_percent10_model,all_salt_percent10_model,all_temp_percent90_model,all_salt_percent90_model,dirname):
	all_temp_bias=all_temp_mean_model-all_temp_en4
	mean_temp_bias=np.nanmin(all_temp_bias,0)
	all_salt_bias=all_salt_mean_model-all_salt_en4
	mean_salt_bias=np.nanmin(all_salt_bias,0)
	all_temp_percent10_cent=all_temp_percent10_model-all_temp_mean_model
	temp_percent10=np.nanmin(all_temp_percent10_cent,0)
	all_salt_percent10_cent=all_salt_percent10_model-all_salt_mean_model
	salt_percent10=np.nanmin(all_salt_percent10_cent,0)
	all_temp_percent90_cent=all_temp_percent90_model-all_temp_mean_model
	temp_percent90=np.nanmin(all_temp_percent90_cent,0)
	all_salt_percent90_cent=all_salt_percent90_model-all_salt_mean_model
	salt_percent90=np.nanmin(all_salt_percent90_cent,0)
	
	gs = gridspec.GridSpec(2, 2, width_ratios=[1,1], height_ratios=[2,2])
	fig1 = plt.figure(figsize=(14, 16))  # (w,h)

	ax1 = plt.subplot(gs[0,0])

	ax1.plot(mean_temp_bias,vert_standart,'b.-')
	ax1.set_xlabel('Bias in temperature [$^\circ$C]', size=16)
	ax1.set_ylabel('Depth [m]', size=14)
	ax1.set_ylim(2000, 0)
	ax1.grid(True, which='both')
	ax1.xaxis.tick_top()
	ax1.xaxis.set_label_position('top') 
	ax1.axvline(0)

	ax2 = plt.subplot(gs[0,1])
	
	ax2.plot(mean_salt_bias,vert_standart,'b.-')
	ax2.set_xlabel('Bias in salinity PSU', size=16)
	ax2.set_ylabel('Depth [m]', size=14)
	ax2.set_ylim(2000, 0)
	ax2.grid(True, which='both')
	ax2.xaxis.tick_top()
	ax2.xaxis.set_label_position('top') 
	ax2.axvline(0)


	ax3 = plt.subplot(gs[1,0])

	ax3.plot(temp_percent10,vert_standart,'b.-', label='percent10')
	ax3.set_xlabel('Percentiles in temperature [$^\circ$C]', size=16)
	ax3.set_ylabel('Depth [m]', size=14)
	ax3.set_ylim(2000, 0)
	ax3.grid(True, which='both')
	ax3.xaxis.tick_top()
	ax3.xaxis.set_label_position('top') 
	ax3.axvline(0)
	ax3.plot(temp_percent90,vert_standart,'g.-', label='percent90')

	ax4 = plt.subplot(gs[1,1])

	ax4.plot(salt_percent10,vert_standart,'b.-', label='percent10')
	ax4.set_xlabel('Percentiles in salinity PSU', size=16)
	ax4.set_ylabel('Depth [m]', size=14)
	ax4.set_ylim(2000, 0)
	ax4.grid(True, which='both')
	ax4.xaxis.tick_top()
	ax4.xaxis.set_label_position('top') 
	ax4.axvline(0)
	ax4.plot(salt_percent90,vert_standart,'g.-', label='percent90')
	plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

	plt.savefig(dirname+"/plots_bias_percent_profiles_temperature_salinity.png")
	return




## parser and main
def script_parser():
    """Customized parser.
    """
    from optparse import OptionParser
    usage = "usage: %prog [options] jsonfile"
    parser = OptionParser(usage=usage)
    return parser


def main():
    parser = script_parser()
    (options, args) = parser.parse_args()
    if len(args) < 1: # print the help message if number of args is not 3.
        parser.print_help()
        sys.exit()
    jsonfile = args[0]
    sourcefile=open(jsonfile,'rU')
    infos=json.load(sourcefile)
    nb_profilesEN4=len(infos)

    print time.strftime('%d/%m/%y %H:%M',time.localtime())

    vert_standart=[0,2,4,6,8,10,12,14,16,18,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,110,120,130,140,150,160,170,180,190,200,220,240,260,280,300,320,340,360,380,400,420,440,460,480,500,520,540,560,580,600,620,640,660,680,700,720,740,760,780,800,820,840,860,880,900,920,940,960,980,1000,1050,1100,1150,1200,1250,1300,1350,1400,14250,1500,1550,1600,1650,1700,1750,1800,1850,1900,1950,2000]

    all_temp_mean_model=np.zeros((nb_profilesEN4,len(vert_standart)))
    all_salt_mean_model=np.zeros((nb_profilesEN4,len(vert_standart)))
    all_temp_en4=np.zeros((nb_profilesEN4,len(vert_standart)))
    all_salt_en4=np.zeros((nb_profilesEN4,len(vert_standart)))
    all_temp_percent10_model=np.zeros((nb_profilesEN4,len(vert_standart)))
    all_salt_percent10_model=np.zeros((nb_profilesEN4,len(vert_standart)))
    all_temp_percent90_model=np.zeros((nb_profilesEN4,len(vert_standart)))
    all_salt_percent90_model=np.zeros((nb_profilesEN4,len(vert_standart)))

    for prof in np.arange(nb_profilesEN4):
	depth_en4,depth_model,temp_en4,salt_en4,mean_temp_model,mean_salt_model,percent10_temp_model,percent10_salt_model,percent90_temp_model,percent90_salt_model = get_netcdf_profiles(jsonfile,infos,prof)
        temp_en4_standart,salt_en4_standart,mean_temp_model_standart,mean_salt_model_standart,percent10_temp_model_standart,percent10_salt_model_standart,percent90_temp_model_standart,percent90_salt_model_standart = project_standart_vertical_levels(depth_en4,depth_model,temp_en4,salt_en4,mean_temp_model,mean_salt_model,percent10_temp_model,percent10_salt_model,percent90_temp_model,percent90_salt_model,vert_standart)
	all_temp_mean_model[prof,:]=mean_temp_model_standart[:]
	all_salt_mean_model[prof,:]=mean_salt_model_standart[:]
	all_temp_mean_en4[prof,:]=mean_temp_en4_standart[:]
	all_salt_mean_en4[prof,:]=mean_salt_en4_standart[:]
	all_temp_percent10_model[prof,:]=percent10_temp_model_standart[:]
	all_salt_percent10_model[prof,:]=percent10_salt_model_standart[:]
	all_temp_percent90_model[prof,:]=percent90_temp_model_standart[:]
	all_salt_percent90_model[prof,:]=percent90_salt_model_standart[:]
    
    plot_mean_percent_bias_profile(all_temp_mean_model,all_salt_mean_model,all_temp_mean_en4,all_salt_mean_en4,all_temp_percent10_model,all_salt_percent10_model,all_temp_percent90_model,all_salt_percent90_model)

        

    print time.strftime('%d/%m/%y %H:%M',time.localtime())

if __name__ == '__main__':
    sys.exit(main() or 0)

