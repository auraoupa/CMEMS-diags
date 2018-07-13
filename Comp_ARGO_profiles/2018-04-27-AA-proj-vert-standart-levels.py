#!/usr/bin/env python
#
#
#Statistical measure of the bias of NATL60 versus hydrographic data set EN4 : step 2

# - We provide the coordinates of a zone comprised in NATL60 boudaries 
# - We get the EN4 profiles inside that zone
# - We calculate for every profile the model mean, percent 10 and 90 T and S 
# - We create netcdf files containing EN4 and NATL60 profiles

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
import yaml
import io
import json
import os


def proj(jsonfile,infos,prof,outname,outname2,reference):

	vert_standart=[0,2,4,6,8,10,12,14,16,18,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,110,120,130,140,150,160,170,180,190,200,220,240,260,280,300,320,340,360,380,400,420,440,460,480,500,520,540,560,580,600,620,640,660,680,700,720,740,760,780,800,820,840,860,880,900,920,940,960,980,1000,1050,1100,1150,1200,1250,1300,1350,1400,1450,1500,1550,1600,1650,1700,1750,1800,1850,1900,1950,2000]


	depth_en4,depth_model,temp_en4,salt_en4,mean_temp_model,mean_salt_model,percent10_temp_model,percent10_salt_model,percent90_temp_model,percent90_salt_model,obs_lat,obs_lon,obs_time = get_netcdf_profiles(outname)
        if depth_en4[-1] > 500:
	        temp_en4_standart,salt_en4_standart,mean_temp_model_standart,mean_salt_model_standart,percent10_temp_model_standart,percent10_salt_model_standart,percent90_temp_model_standart,percent90_salt_model_standart = project_standart_vertical_levels(depth_en4,depth_model,temp_en4,salt_en4,mean_temp_model,mean_salt_model,percent10_temp_model,percent10_salt_model,percent90_temp_model,percent90_salt_model,vert_standart)
		print "profile "+reference+" has been projected, output file is"+outname2
		dsout=Dataset(outname2,'w')

		today=date.today()
		dsout.description = "This file contains one profile of temperature and salinity from EN4 dataset and the mean and 10 and 90 percentile of NATL60-CJM165 data within a 0.25deg circle around the location of the profile and 15 days before and after it has been sampled. Data have been projected on a standart vertical grid. This file has been created "+str(today.day)+"/"+str(today.month)+"/"+str(today.year)

		depth=dsout.createDimension('depth',len(vert_standart))
		x=dsout.createDimension('x',1)
		y=dsout.createDimension('y',1)
		
		lat = dsout.createVariable('latitude_profileEN4', 'f8', ('y','x'))
		lat.standart_name="latitude_profileEN4"
		lat.long_name = "Latitude of selected EN4 profile"
		lat.units = "degrees_north"

		lon = dsout.createVariable('longitude_profileEN4', 'f8', ('y','x'))
		lon.standart_name="longitude_profileEN4"
		lon.long_name = "Longitude of selected EN4 profile"
		lon.units = "degrees_east"

		time = dsout.createVariable('time_profileEN4', 'f8', ('y','x'))
		time.standart_name="time_profileEN4"
		time.timeg_name = "Time in seconds from 1-1-1958 of selected EN4 profile"
		time.units = "seconds"

		depth_stand = dsout.createVariable('depth_en4', 'f8', ('depth'),fill_value=0.)
		depth_stand.units = "m"
		depth_stand.valid_min = 0.
		depth_stand.valid_max = 8000.
		depth_stand.long_name = "Depth"

		temp_en4 = dsout.createVariable('temp_profileEN4', 'f8', ('depth'),fill_value=0.)
		temp_en4.units = "degC"
		temp_en4.valid_min = -10.
		temp_en4.valid_max = 40.
		temp_en4.long_name = "Temperature profile of the selected EN4 profile"
		
		salt_en4 = dsout.createVariable('salt_profileEN4', 'f8', ('depth'),fill_value=0.)
		salt_en4.units = "PSU"
		salt_en4.valid_min = 20.
		salt_en4.valid_max = 40.
		salt_en4.long_name = "Salinity profile of the selected EN4 profile"

		mean_temp_model = dsout.createVariable('mean_temp_model', 'f8', ('depth'),fill_value=0.)
		mean_temp_model.units = "degC"
		mean_temp_model.valid_min = -10.
		mean_temp_model.valid_max = 40.
		mean_temp_model.long_name = "Mean Temperature profile of the model"
		
		mean_salt_model = dsout.createVariable('mean_salt_model', 'f8', ('depth'),fill_value=0.)
		mean_salt_model.units = "PSU"
		mean_salt_model.valid_min = 20.
		mean_salt_model.valid_max = 40.
		mean_salt_model.long_name = "Mean Salinity profile of the model"
		
		percent10_temp_model = dsout.createVariable('percent10_temp_model', 'f8', ('depth'),fill_value=0.)
		percent10_temp_model.units = "degC"
		percent10_temp_model.valid_min = -10.
		percent10_temp_model.valid_max = 40.
		percent10_temp_model.long_name = "Percent 10 Temperature profile of the model"

		percent10_salt_model = dsout.createVariable('percent10_salt_model', 'f8', ('depth'),fill_value=0.)
		percent10_salt_model.units = "PSU"
		percent10_salt_model.valid_min = 20.
		percent10_salt_model.valid_max = 40.
		percent10_salt_model.long_name = "Percent 10 Salinity profile of the model"

		percent90_temp_model = dsout.createVariable('percent90_temp_model', 'f8', ('depth'),fill_value=0.)
		percent90_temp_model.units = "degC"
		percent90_temp_model.valid_min = -90.
		percent90_temp_model.valid_max = 40.
		percent90_temp_model.long_name = "Percent 90 Temperature profile of the model"

		percent90_salt_model = dsout.createVariable('percent90_salt_model', 'f8', ('depth'),fill_value=0.)
		percent90_salt_model.units = "PSU"
		percent90_salt_model.valid_min = 20.
		percent90_salt_model.valid_max = 40.
		percent90_salt_model.long_name = "Percent 90 Salinity profile of the model"

		lat[:]=obs_lat
		lon[:]=obs_lon
		time[:]=obs_time
		depth_stand[:]=vert_standart
		temp_en4[:]=temp_en4_standart
		salt_en4[:]=salt_en4_standart
		mean_temp_model[:]=mean_temp_model_standart
		mean_salt_model[:]=mean_salt_model_standart
		percent10_temp_model[:]=percent10_temp_model_standart
		percent10_salt_model[:]=percent10_salt_model_standart
		percent90_temp_model[:]=percent90_temp_model_standart
		percent90_salt_model[:]=percent90_salt_model_standart
		dsout.close()  # close the new file

	else:
		print "profile "+reference+" does not go as deep as 500m, not projecting"



def get_netcdf_profiles(outname):
	
	dsprof=xr.open_dataset(outname)

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
	obs_lat=dsprof['latitude_profileEN4']
	obs_lon=dsprof['longitude_profileEN4']
	obs_time=dsprof['time_profileEN4']

        return depth_en4,depth_model,temp_en4,salt_en4,mean_temp_model,mean_salt_model,percent10_temp_model,percent10_salt_model,percent90_temp_model,percent90_salt_model,obs_lat,obs_lon,obs_time

def project_standart_vertical_levels(depth_en4,depth_model,temp_en4,salt_en4,mean_temp_model,mean_salt_model,percent10_temp_model,percent10_salt_model,percent90_temp_model,percent90_salt_model,vert_standart):
	
	temp_en4_standart=np.interp(vert_standart,depth_en4,temp_en4)
        salt_en4_standart=np.interp(vert_standart,depth_en4,salt_en4)
        mean_temp_model_standart=np.interp(vert_standart,depth_model,mean_temp_model)
        mean_salt_model_standart=np.interp(vert_standart,depth_model,mean_salt_model)
        percent10_temp_model_standart=np.interp(vert_standart,depth_model,percent10_temp_model)
        percent10_salt_model_standart=np.interp(vert_standart,depth_model,percent10_salt_model)
        percent90_temp_model_standart=np.interp(vert_standart,depth_model,percent90_temp_model)
        percent90_salt_model_standart=np.interp(vert_standart,depth_model,percent90_salt_model)

	ien4=np.where(vert_standart[:]>depth_en4[-1].values)
	imod=np.where(vert_standart[:]>depth_model[-1].values)

	if len(ien4[:][0]) > 1:
		temp_en4_standart[np.min(ien4)-1:]=np.nan
		salt_en4_standart[np.min(ien4)-1:]=np.nan
        if len(imod[:][0]) > 1:
                mean_temp_model_standart[np.min(imod)-1:]=np.nan
		mean_salt_model_standart[np.min(imod)-1:]=np.nan
	        percent10_temp_model_standart[np.min(imod)-1:]=np.nan
	        percent10_salt_model_standart[np.min(imod)-1:]=np.nan
	        percent90_temp_model_standart[np.min(imod)-1:]=np.nan
	        percent90_salt_model_standart[np.min(imod)-1:]=np.nan


        return temp_en4_standart,salt_en4_standart,mean_temp_model_standart,mean_salt_model_standart,percent10_temp_model_standart,percent10_salt_model_standart,percent90_temp_model_standart,percent90_salt_model_standart



## parser and main
def script_parser():
    """Customized parser.
    """
    from optparse import OptionParser
    usage = "usage: %prog  --jsonfile name --dir dir"
    parser = OptionParser(usage=usage)
    parser.add_option('--jsonfile', help="Filename", dest="jsonfile", type="string", nargs=1)
    parser.add_option('--dir', help="Dirname", dest="dir", type="string", nargs=1)
    return parser

def main():
    parser = script_parser()
    (options, args) = parser.parse_args()
    optdic=vars(options)

    jsonfile = optdic['jsonfile']
    dirn = optdic['dir']

    sourcefile=open(jsonfile,'rU')
    infos=json.load(sourcefile)
    nb_profilesEN4=len(infos)


    for prof in np.arange(nb_profilesEN4):

        list_profiles = infos.keys()
        reference =  str(list_profiles[prof])
        namezone=jsonfile[0:-5]
        outname=dirn+"/profiles_EN4-"+reference[1:]+"_NATL60-CJM165_TS.nc"

	if os.path.exists(outname):
		outname2=outname.replace('TS','TS_vert-stand')
		if not os.path.exists(outname2):
			proj(jsonfile,infos,prof,outname,outname2,reference)

				


if __name__ == '__main__':
    sys.exit(main() or 0)

