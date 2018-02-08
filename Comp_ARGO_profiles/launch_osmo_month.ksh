#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=24
#SBATCH --ntasks-per-node=24
#SBATCH --threads-per-core=1
#SBATCH --constraint=HSW24
#SBATCH -J osmo_en4
#SBATCH -e osmo_en4.e%j
#SBATCH -o osmo_en4.o%j
#SBATCH --time=13:00:00
#SBATCH --exclusive
#SBATCH --mail-type=ALL
#SBATCH --mail-user=$MAILT

set -x
ulimit -s
ulimit -s unlimited

for month in jan feb mar apr may jun jul aug sep oct nov dec; do
	2017-10-25-AA-step2-netcdf-files-EN4-profiles-model-from-jsonfile-NATL60-util_opti-step.py osmo_${month}.json > output.${month} &
done

wait
