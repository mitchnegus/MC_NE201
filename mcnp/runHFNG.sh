#!/bin/bash
# Job name:
#SBATCH --job-name=HFNG-Edist
# Account:
#SBATCH --account=fc_deans
# Partition:
#SBATCH --partition=savio
# QoS:
#SBATCH --qos=savio_normal
# Number of nodes needed for use case:
#SBATCH --nodes=20
# Tasks per node based on number of cores per node (example):
#SBATCH --ntasks-per-node=20
# Processors per task:
#SBATCH --cpus-per-task=1
# Wall clock limit:
#SBATCH --time=00:30:00
## Command(s) to run (example):
date
module load intel openmpi
mpirun -np 400 mcnp6.mpi  i=HFNG.inp o=HFNG.out
date
