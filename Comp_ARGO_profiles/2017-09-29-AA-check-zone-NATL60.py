def check_zone_NATL60_boundaries(latmin,latmax,lonmin,lonmax,datemin,datemax):
        ''' Check if the selected zone and period fall within NATL60 boundaries
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


        datetmin=pd.to_datetime(datemin)
        datetmax=pd.to_datetime(datemax)
        ttmin=datetime.datetime(int(datetmin.strftime('%Y')),int(datetmin.strftime('%m')),int(datetmin.strftime('%d')),int(datetmin.strftime('%H')),int(datetmin.strftime('%M')))
        ttmax=datetime.datetime(int(datetmax.strftime('%Y')),int(datetmax.strftime('%m')),int(datetmax.strftime('%d')),int(datetmax.strftime('%H')),int(datetmax.strftime('%M')))
        tsecmin=(ttmin-datetime.datetime(1958,1,1,0,0)).total_seconds()
        tsecmax=(ttmax-datetime.datetime(1958,1,1,0,0)).total_seconds()


        if (lamin < latmin < lamax) & (lamin < latmax < lamax) & (lomin < lonmin < lomax) & (lomin < lonmax < lomax) & (tmin < tsecmin < tmax) & (tmin < tsecmax < tmax):
                print "selected area and period fall within NATL60-CJM165 boundaries, the program is proceeding"
        else:
                print "selected area and period do not fall within NATL60-CJM165 boundaries, the program is stopping"
                sys.exit()
        return tsecmin,tsecmax

