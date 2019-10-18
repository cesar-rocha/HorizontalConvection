#!/bin/bash
#PBS -q normalsl
#PBS -P g40
#PBS -l ncpus=992 
#PBS -l mem=5748GB
#PBS -l jobfs=400GB
#PBS -l walltime=10:00:00
#PBS -l software=python
#PBS -l wd
 
# Load modules.
module load python3/3.6.2
module load mpi4py/3.0.0-py36-omp10.2
module load hdf5/1.8.14

# Run Python applications
mpirun -n 992 python3 2D_HC.py > $PBS_JOBID.log   
