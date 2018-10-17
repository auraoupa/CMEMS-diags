#!/bin/bash

#SBATCH -J dask_test
#SBATCH -e dask_test.err
#SBATCH -o dask_test.out
#SBATCH -n 1
#SBATCH --cpus-per-task=24
#SBATCH --mem=10G
#SBATCH -t 00:30:00
#SBATCH --constraint=HSW24
#SBATCH --exclusive
#SBATCH --nodes=1



/scratch/cnt0024/hmg2840/albert7a/anaconda2/envs/pangeo/bin/python -m distributed.cli.dask_worker tcp://172.30.100.3:40756 --nthreads 24 --memory-limit 10.00GB --name dask_test-2 --death-timeout 60

cd /home/albert7a/git/CMEMS-diags/TSG_Guillaume

/scratch/cnt0024/hmg2840/albert7a/anaconda2/envs/pangeo/bin/python binning_1band.py
