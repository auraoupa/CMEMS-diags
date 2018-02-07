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


def check_zone_NATL60_boundaries(latmin,latmax,lonmin,lonmax):
        ''' Check if the selected zone falls within NATL60 boundaries
	'''

	#NATL60
	tfiles="/scratch/cnt0024/hmg2840/albert7a/NATL60/NATL60-CJM165-S/TS/NATL60-CJM165_y????m??d??.1d_TS.nc"

 	##Open NATL60 files to get boundaries of domain

	dsN = xr.open_mfdataset(tfiles,concat_dim='time_counter',decode_times=False, chunks={'deptht':1 ,'time_counter':10})

	latN = dsN.nav_lat
	lonN = dsN.nav_lon
	timN = dsN.time_counter

	lamin=np.nanmin(latN.values)
	lamax=np.nanmax(latN.values)
	lomin=np.nanmin(lonN.values)
	lomax=np.nanmax(lonN.values)
	tmin=np.min(timN.values)
	tmax=np.max(timN.values)

	if (lamin < latmin < lamax) | (lamin < latmax < lamax) | (lomin < lonmin < lomax) | (lomin < lonmax < lomax):
		print "selected area falls within NATL60-CJM165 boundaries, the program is proceeding"
	else:
		print "selected area does not fall within NATL60-CJM165 boundaries, the program is stopping"
		sys.exit()

	return dsN,dsen4,latN,lonN,timN,tmin,tmax

def select_profiles(latmin,latmax,lonmin,lonmax,fileEN4,tmin,tmax):
        ''' Select all the EN4 profiles inside the zone and within NATL60 period
        '''
        ## Datasets

        #EN4
        diren4="/scratch/cnt0024/hmg2840/albert7a/EN4/"
        tfileEN4=diren4+fileEN4

        dsen4=xr.open_dataset(tfileEN4)
        laten4=dsen4['LATITUDE']
        lonen4=dsen4['LONGITUDE']
        dayen4=dsen4['JULD']
        refen4=dsen4['DC_REFERENCE']
	tempen4=dsen4['POTM_CORRECTED']
	salten4=dsen4['PSAL_CORRECTED']
	depen4=dsen4['DEPH_CORRECTED']

	indz=np.where((lonmin<lonen4.values)&(lonen4.values<lonmax)&(latmin<laten4.values)&(laten4.values<latmax))
        prof_zone=[]
 	tsecen4z=[]
        for ref in np.arange(len(indz[0])):
		dateen4= pd.to_datetime(str(dayen4[indz[0][ref]].values))
		ten4 = datetime.datetime(int(dateen4.strftime('%Y')),int(dateen4.strftime('%m')),int(dateen4.strftime('%d')),int(dateen4.strftime('%H')),int(dateen4.strftime('%M')))
		tsecen4=(ten4-datetime.datetime(1958,1,1,0,0)).total_seconds()
		if (tsecen4 < tmax) & (tsecen4 > tmin):
			prof_zone.append(indz[0][ref])
			tsecen4z.append(tsecen4)

 	laten4z=laten4[prof_zone].values
 	lonen4z=lonen4[prof_zone].values
 	refen4z=refen4[prof_zone].values
 	tempen4z=tempen4[prof_zone].values
 	salten4z=salten4[prof_zone].values
 	depen4z=depen4[prof_zone].values
	
	return laten4z,lonen4z,refen4z,tsecen4z,tempen4z,salten4z,depen4z

        

  
def model_mean_percent_profile(ref_prof,dsN,dsen4,latN,lonN,timN,laten4,lonen4,dayen4,tsecen4):
    #select NATL60 data at the closest depth and within 0.25 and 15days near the location and date of the ARGO profile
    observation_lon=lonen4
    observation_lat=laten4
    observation_time=tsecen4

    tempen4=dsen4['POTM_CORRECTED'][ref_prof]
    salten4=dsen4['PSAL_CORRECTED'][ref_prof]
    depen4=dsen4['DEPH_CORRECTED'][ref_prof]

    observation_dep=depen4
    observation_temp=tempen4
    observation_salt=salten4

    depN = dsN.deptht
    tempN=dsN.votemper
    saltN=dsN.vosaline

    #get the number of useful levels in EN4 profile
    dep_level=np.zeros(1)

    for k in np.arange(len(observation_dep)):
        if not np.isnan(observation_dep[k]):
            dep_level[0]=k

    #get the corresponding model level
    model_level=np.zeros(dep_level[0])
    model_dep=np.zeros(dep_level[0])
    obsred_dep=np.zeros(dep_level[0])
    obsred_temp=np.zeros(dep_level[0])
    obsred_salt=np.zeros(dep_level[0])
    for z in np.arange(dep_level[0]):
        obsred_dep[int(z)]=observation_dep[int(z)]
        obsred_temp[int(z)]=observation_temp[int(z)]
        obsred_salt[int(z)]=observation_salt[int(z)]
        diff_dep=0*depN.values
        for k in np.arange(len(depN.values)):
            diff_dep[k]=depN.values[k]-obsred_dep[int(z)]
        lev=np.where(np.abs(diff_dep)==np.min(np.abs(diff_dep)))
        model_level[z]=lev[0]
        model_dep[z]=depN.values[lev[0]]

    #Coarse box in which EN4 profile is contained
    step=1
    indxBOX=np.where((lonN>observation_lon-1)&(lonN<observation_lon+1)&(latN>observation_lat-1)&(latN<observation_lat+1))
    model_lonBOX=lonN[np.min(indxBOX[0]):np.max(indxBOX[0]):step,np.min(indxBOX[1]):np.max(indxBOX[1]):step]
    model_latBOX=latN[np.min(indxBOX[0]):np.max(indxBOX[0]):step,np.min(indxBOX[1]):np.max(indxBOX[1]):step]
    model_lonBOX_array=model_lonBOX.values
    model_latBOX_array=model_latBOX.values
    indtBOX=np.where((timN.values < tsecen4 + 15*24*3600) & (timN.values > tsecen4 - 15*24*3600) )
    model_tBOX=timN[indtBOX[0][0]:indtBOX[0][-1]]
    t_dim=np.arange(len(model_tBOX))
    x_dim=np.arange(model_lonBOX_array.shape[1])
    y_dim=np.arange(model_lonBOX_array.shape[0])

    def profile_mean_percent(k):

        #decoupage grossier autour de la position du profile ARGO pour un niveau vertical

        model_tempBOX=tempN[indtBOX[0][0]:indtBOX[0][-1],k,np.min(indxBOX[0]):np.max(indxBOX[0]):step,np.min(indxBOX[1]):np.max(indxBOX[1]):step]
        model_saltBOX=saltN[indtBOX[0][0]:indtBOX[0][-1],k,np.min(indxBOX[0]):np.max(indxBOX[0]):step,np.min(indxBOX[1]):np.max(indxBOX[1]):step]

        model_tempBOX_array=model_tempBOX.values
        model_saltBOX_array=model_saltBOX.values
        model_tBOX_array=model_tBOX.values

        # construction d'un nouveau xarray
        d = {}
        d['time_counter'] = ('time_counter',t_dim)
        d['y'] = ('y',y_dim)
        d['x'] = ('x',x_dim)
        d['nav_lat'] = (['y','x'],model_latBOX_array)
        d['nav_lon'] = (['y','x'],model_lonBOX_array)

        d['votemper'] = (['time_counter','y','x'], model_tempBOX_array)
        d['vosaline'] = (['time_counter','y','x'], model_saltBOX_array)
        d['time_counter'] = (['time_counter'], model_tBOX_array)
        dset = xr.Dataset(d)

        latB = dset.nav_lat
        lonB = dset.nav_lon
        model_temperatureB = dset.votemper
        model_salinityB = dset.vosaline
        model_timeB = dset.time_counter

        # selection plus fine des profils

        lon_stacked = lonB.stack(profile=('x', 'y'))
        lat_stacked = latB.stack(profile=('x', 'y'))

        distance_threshold = 0.25
        square_distance_to_observation = (lon_stacked - observation_lon)**2 + (lat_stacked-observation_lat)**2
        is_close_to_observation = square_distance_to_observation < distance_threshold**2

        model_temperature_stacked = model_temperatureB.stack(profile=('x', 'y'))
        model_salinity_stacked = model_salinityB.stack(profile=('x', 'y'))

        model_temperature_near_observation = model_temperature_stacked.where(is_close_to_observation,drop=True)
        model_salinity_near_observation = model_salinity_stacked.where(is_close_to_observation, drop=True)
        lat_near_observation = lat_stacked.where(is_close_to_observation, drop=True)
        lon_near_observation = lon_stacked.where(is_close_to_observation, drop=True)

        model_temp_dask=dask.array.from_array(model_temperature_near_observation,chunks=(100,100))
        model_temp_dask_concat=dask.array.concatenate(model_temp_dask)
        model_salt_dask=dask.array.from_array(model_salinity_near_observation,chunks=(100,100))
        model_salt_dask_concat=dask.array.concatenate(model_salt_dask)
        temp_model_mean = model_temp_dask_concat.mean().compute()
        temp_percentile_10= np.percentile(model_temp_dask_concat,10)
        temp_percentile_90= np.percentile(model_temp_dask_concat,90)
        salt_model_mean = model_salt_dask_concat.mean().compute()
        salt_percentile_10= np.percentile(model_salt_dask_concat,10)
        salt_percentile_90= np.percentile(model_salt_dask_concat,90)

        return lat_near_observation,lon_near_observation,temp_model_mean,temp_percentile_10,temp_percentile_90,salt_model_mean,salt_percentile_10,salt_percentile_90

    profil_temp_model_mean=np.zeros(dep_level[0])
    profil_temp_model_percent10=np.zeros(dep_level[0])
    profil_temp_model_percent90=np.zeros(dep_level[0])
    profil_salt_model_mean=np.zeros(dep_level[0])
    profil_salt_model_percent10=np.zeros(dep_level[0])
    profil_salt_model_percent90=np.zeros(dep_level[0])


    for z in np.arange(dep_level[0]):
        lat_near_observation,lon_near_observation,temp_model_mean,temp_percentile_10,temp_percentile_90,salt_model_mean,salt_percentile_10,salt_percentile_90=profile_mean_percent(model_level[z].astype(int))
        profil_temp_model_mean[z]=temp_model_mean
        profil_temp_model_percent10[z]=temp_percentile_10
        profil_temp_model_percent90[z]=temp_percentile_90
        profil_salt_model_mean[z]=salt_model_mean
        profil_salt_model_percent10[z]=salt_percentile_10
        profil_salt_model_percent90[z]=salt_percentile_90

	
    return profil_temp_model_mean,profil_temp_model_percent10,profil_temp_model_percent90,profil_salt_model_mean,profil_salt_model_percent10,profil_salt_model_percent90,observation_dep,obsred_temp,obsred_salt,dep_level,model_dep,obsred_dep


def create_netcdf_profile(dsen4,ref_prof,laten4,lonen4,dayen4,tsecen4,profil_temp_model_mean,profil_temp_model_percent10,profil_temp_model_percent90,profil_salt_model_mean,profil_salt_model_percent10,profil_salt_model_percent90,observation_dep,obsred_temp,obsred_salt,dep_level,model_dep,obsred_dep):

    reference_profile=str(dsen4['DC_REFERENCE'][ref_prof].values)
    outname="/scratch/cnt0024/hmg2840/albert7a/EN4/profiles_files/profiles_EN4-"+reference_profile[1:-1]+"_NATL60-CJM165_TS.nc"
    print('output file is '+outname)
    dsout=Dataset(outname,'w')

    today=date.today()
    dsout.description = "This file contains one profile of temperature and salinity from EN4 dataset and the mean and 10 and 90 percentile of NATL60-CJM165 data within a 0.25deg circle around the location of the profile and 15 days before and after it has been sampled. This file has been created "+str(today.day)+"/"+str(today.month)+"/"+str(today.year)

    depth=dsout.createDimension('depth',dep_level[0])
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

    depth_en4 = dsout.createVariable('depth_en4', 'f8', ('depth'),fill_value=0.)
    depth_en4.units = "m" 
    depth_en4.valid_min = 0.
    depth_en4.valid_max = 8000.
    depth_en4.long_name = "Depth" 

    depth_model = dsout.createVariable('depth_model', 'f8', ('depth'),fill_value=0.)
    depth_model.units = "m" 
    depth_model.valid_min = 0.
    depth_model.valid_max = 8000.
    depth_model.long_name = "Depth" 

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

    depth_en4[:]=obsred_dep
    depth_model[:]=model_dep
    temp_en4[:]=observation_temp
    salt_en4[:]=observation_salt
    mean_temp_model[:]=profil_temp_model_mean
    mean_salt_model[:]=profil_salt_model_mean
    percent10_temp_model[:]=profil_temp_model_percent10
    percent10_salt_model[:]=profil_salt_model_percent10
    percent90_temp_model[:]=profil_temp_model_percent90
    percent90_salt_model[:]=profil_salt_model_percent90
    dsout.close()  # close the new file

## parser and main
def script_parser():
    """Customized parser.
    """
    from optparse import OptionParser
    usage = "usage: %prog [options] fileEN4 latmin latmax lonmin lonmax"
    parser = OptionParser(usage=usage)
    return parser


def main():
    parser = script_parser()
    (options, args) = parser.parse_args()
    if len(args) < 5: # print the help message if number of args is not 3.
        parser.print_help()
        sys.exit()
    optdic = vars(options)
    fileEN4 = args[0]
    latmin = args[1]
    latmax = args[2]
    lonmin = args[3]
    lonmax = args[4]
    print time.strftime('%d/%m/%y %H:%M',time.localtime())

    dsN,dsen4,latN,lonN,timN,tmin,tmax=check_zone_NATL60_boundaries(latmin,latmax,lonmin,lonmax)    
    laten4z,lonen4z,refen4z,tsecen4z,tempen4z,salten4z,depen4z=select_profiles(latmin,latmax,lonmin,lonmax,fileEN4,tmin,tmax)
    ref_prof=get_ref_prof(latmin,latmax,lonmin,lonmax)
    dsN,dsen4,latN,lonN,timN,laten4,lonen4,dayen4,tsecen4=check_profile_NATL60_boundaries(fileEN4,ref_prof)    
    profil_temp_model_mean,profil_temp_model_percent10,profil_temp_model_percent90,profil_salt_model_mean,profil_salt_model_percent10,profil_salt_model_percent90,observation_dep,obsred_temp,obsred_salt,dep_level,model_dep,obsred_dep=model_mean_percent_profile(ref_prof,dsN,dsen4,latN,lonN,timN,laten4,lonen4,dayen4,tsecen4)
    create_netcdf_profile(dsen4,ref_prof,laten4,lonen4,dayen4,tsecen4,profil_temp_model_mean,profil_temp_model_percent10,profil_temp_model_percent90,profil_salt_model_mean,profil_salt_model_percent10,profil_salt_model_percent90,observation_dep,obsred_temp,obsred_salt,dep_level,model_dep,obsred_dep)
if __name__ == '__main__':
    sys.exit(main() or 0)

