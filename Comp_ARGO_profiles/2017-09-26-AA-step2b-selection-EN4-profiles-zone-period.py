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


def select_profiles(latmin,latmax,lonmin,lonmax,datemin,datemax,jsonfile):
        ''' Identify all the EN4 profiles that fall within the selected zone and period
        '''
        ## Datasets

        #EN4
        diren4="/scratch/cnt0024/hmg2840/albert7a/EN4/"

        yearmin=datemin[0:4]
	monthmin=datemin[5:7]
        yearmax=datemax[0:4]
	monthmax=datemax[5:7]

        list_filesEN4=[]
	if yearmin == yearmax:
	    for m in np.arange(int(monthmin),int(monthmax)+1):
	        if m < 10:
	            list_filesEN4.append('EN.4.2.0.f.profiles.g10.'+yearmin+'0'+str(m)+'.nc')
        	else:
	            list_filesEN4.append('EN.4.2.0.f.profiles.g10.'+yearmin+str(m)+'.nc')
	else:
            for m in np.arange(int(monthmin),13):
		if m < 10:
	            list_filesEN4.append('EN.4.2.0.f.profiles.g10.'+yearmin+'0'+str(m)+'.nc')
	        else:
	            list_filesEN4.append('EN.4.2.0.f.profiles.g10.'+yearmin+str(m)+'.nc')
	    for m in np.arange(1,int(monthmax)+1):
	        if m < 10:
	            list_filesEN4.append('EN.4.2.0.f.profiles.g10.'+yearmax+'0'+str(m)+'.nc')
	        else:
	            list_filesEN4.append('EN.4.2.0.f.profiles.g10.'+yearmax+str(m)+'.nc')

	print list_filesEN4

        datetmin=pd.to_datetime(datemin)
        datetmax=pd.to_datetime(datemax)
        ttmin=datetime.datetime(int(datetmin.strftime('%Y')),int(datetmin.strftime('%m')),int(datetmin.strftime('%d')),int(datetmin.strftime('%H')),int(datetmin.strftime('%M')))
        ttmax=datetime.datetime(int(datetmax.strftime('%Y')),int(datetmax.strftime('%m')),int(datetmax.strftime('%d')),int(datetmax.strftime('%H')),int(datetmax.strftime('%M')))
        tsecmin=(ttmin-datetime.datetime(1958,1,1,0,0)).total_seconds()
        tsecmax=(ttmax-datetime.datetime(1958,1,1,0,0)).total_seconds()

	for f in np.arange(len(list_filesEN4)):
		fileEN4=list_filesEN4[f]
	        tfileEN4=diren4+fileEN4

	        dsen4=xr.open_dataset(tfileEN4)
	        laten4=dsen4['LATITUDE']
	        lonen4=dsen4['LONGITUDE']
	        dayen4=dsen4['JULD']
	        refen4=dsen4['DC_REFERENCE']

		indz=np.where((lonmin<lonen4.values)&(lonen4.values<lonmax)&(latmin<laten4.values)&(laten4.values<latmax))
	        prof_zone=[]
	 	tsecen4z=[]
	        for ref in np.arange(len(indz[0])):
			dateen4= pd.to_datetime(str(dayen4[indz[0][ref]].values))
			ten4 = datetime.datetime(int(dateen4.strftime('%Y')),int(dateen4.strftime('%m')),int(dateen4.strftime('%d')),int(dateen4.strftime('%H')),int(dateen4.strftime('%M')))
			tsecen4=(ten4-datetime.datetime(1958,1,1,0,0)).total_seconds()
			if (tsecen4 < tsecmax) & (tsecen4 > tsecmin):
				prof_zone.append(indz[0][ref])
				tsecen4z.append(tsecen4)

		for ref in np.arange(len(prof_zone)):
			if 'dictyml' in locals():
				up={str(refen4[prof_zone[ref]].values):{'reference':str(refen4[prof_zone[ref]].values),'file':fileEN4,'profile no':int(prof_zone[ref]),'latitude':float(laten4[prof_zone[ref]].values),'longitude':float(lonen4[prof_zone[ref]].values),'date':str(dayen4[prof_zone[ref]].values)}}
				dictyml.update(up)
			else:
				dictyml={str(refen4[prof_zone[ref]].values):{'reference':str(refen4[prof_zone[ref]].values),'file':fileEN4,'profile no':int(prof_zone[ref]),'latitude':float(laten4[prof_zone[ref]].values),'longitude':float(lonen4[prof_zone[ref]].values),'date':str(dayen4[prof_zone[ref]].values)}}
		

        
	with io.open(jsonfile, 'w', encoding='utf8') as outfile:
		outfile.write(unicode(json.dumps(dictyml, sort_keys=True,indent=4, separators=(',', ': '))))



        

## parser and main
def script_parser():
    """Customized parser.
    """
    from optparse import OptionParser
    usage = "usage: %prog  --coord latmin latmax lonmin lonmax --date datemin datemax --jsonfile name"
    parser = OptionParser(usage=usage)
    parser.add_option('--coord', help="Coordinate", dest="coord", type="float", nargs=4)
    parser.add_option('--date', help="Date", dest="date", type="string", nargs=2)
    parser.add_option('--jsonfile', help="Filename", dest="jsonfile", type="string", nargs=1)
    return parser


def main():
    parser = script_parser()
    (options, args) = parser.parse_args()
    optdic=vars(options)

    (latmin,latmax,lonmin,lonmax) = optdic['coord']
    (datemin,datemax) = optdic['date']
    jsonfile = optdic['jsonfile']

    print time.strftime('%d/%m/%y %H:%M',time.localtime())
    select_profiles(latmin,latmax,lonmin,lonmax,datemin,datemax,jsonfile)
    print time.strftime('%d/%m/%y %H:%M',time.localtime())

if __name__ == '__main__':
    sys.exit(main() or 0)

