#!/usr/bin/env bash

#rossby_file=/data/CLIMATOLOGY/GLORYS/GLORYS12V1_ORCA12_2000-2014_RossbyRadius_filtered.nc

cutoff=10e3

main_output_path=/data/RESULTS/SURFACE_GRADIENTS_10KM

LEGOS_input_files=/data/OBS/TSG/LEGOS/*.nc
FRESH_input_files=/data/OBS/TSG/FRESH/*/*.nc
MEOP_input_files=/data/OBS/SEA_MAMMALS/MEOP-CTD_2017-11-11/*/DATA_ncARGO/*.nc
IMOS_input_files=/data/OBS/TSG/IMOS/*.nc
GOSUD_input_path=/data/OBS/TSG/GOSUD/


LEGOS_output_path=$main_output_path/TSG_LEGOS/
FRESH_output_path=/data/RESULTS/SURFACE_GRADIENTS/TSG_FRESH/
GOSUD_output_path=$main_output_path/TSG_GOSUD/
MEOP_output_path=/data/RESULTS/SURFACE_GRADIENTS/CTD_MEOP/
IMOS_output_path=/data/RESULTS/SURFACE_GRADIENTS/TSG_IMOS/

case $1 in 
    LEGOS)
        compute_tracer_gradients.py $LEGOS_input_files --dataset LEGOS  --outpath $LEGOS_output_path
    ;;
    
    FRESH)
        compute_tracer_gradients.py $FRESH_input_files --cutoff $cutoff --dataset FRESH --outpath $FRESH_output_path
    ;;
    
    MEOP)
        compute_tracer_gradients.py $MEOP_input_files --cutoff $cutoff --dataset MEOP --outpath $MEOP_output_path
    ;;
    
    IMOS)
        compute_tracer_gradients.py $IMOS_input_files --cutoff $cutoff --dataset IMOS --outpath $IMOS_output_path
    ;;
    GOSUD)
        for year in $(ls $GOSUD_input_path)
        do
            mkdir -p $GOSUD_output_path/$year
            mpiexec -n 3 compute_tracer_gradients.py $GOSUD_input_path/$year/NRT/*/*.nc --cutoff $cutoff --dataset GOSUD --outpath $GOSUD_output_path/$year/
        done
    ;;
    *)
        echo "Not a valid dataset"
        exit 1
esac


# Run the computation on NOAA TSG dataset

#for year in $(ls $NOAA_input_path)
#do
#mkdir $NOAA_output_path/$year 
#./compute_tracer_gradients.py $NOAA_input_path/$year/*/*.nc --rossby $rossby_file --dataset NOAA --outpath $NOAA_output_path/$year/
#done
