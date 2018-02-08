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

ulimit -s
ulimit -s unlimited

#\rm head.json tail.json
#head -1 osmo_all_year.json >> head.json
#tail -2 osmo_all_year.json >> tail.json

#for k in $(seq 1 19); do

#  \rm osmo_${k}.json test*
#  kfin=$((k*824))
#  head -$kfin osmo_all_year.json >> test1.json
#  tail -n 823 test1.json >> test2.json
#  cat head.json test2.json tail.json >> osmo_${k}.json
#  \rm test*

#done

#\rm osmo_20.json
#tail -n 849 osmo_all_year.json >> test1.json
#cat head.json test1.json >> osmo_20.json

for k in $(seq 2 20); do
	2017-10-25-AA-step2-netcdf-files-EN4-profiles-model-from-jsonfile-NATL60_opti-step.py osmo_${k}.json &
done

