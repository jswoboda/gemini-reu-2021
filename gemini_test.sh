#!/bin/bash

#Slurm sbatch options
#SBATCH -N 7 # Number of nodes
#SBATCH -n 256 # Number of cores
#SBATCH --gres=gpu:volta:1

#Error & output handling
#SBATCH -o /home/gridsan/swoboj/GEMINI/GEMINI_test/out.log-%j #%j refers to job number, so output files are saved with unique name
#SBATCH -e /home/gridsan/swoboj/GEMINI/GEMINI_test/error.log-%j

#Initalize module command
source /etc/profile
#Load mpi
module load mpi/openmpi-4.1.0

OPENMPI_OPTS="${OPENMPI_OPTS} --mca pml ob1 --mca btl openib,self,vader --mca btl_openib_cpc_include rdmacm --mca btl_openib_rroce_enable 1 "
OPENMPI_OPTS="${OPENMPI_OPTS} --mca btl_openib_receive_queues P,128,64,32,32,32:S,2048,1024,128,32:S,12288,1024,128,32:S,65536,1024,128,32 "

#Run the program
mpirun $OPENMPI_OPTS -np $SLURM_NTASKS /home/gridsan/swoboj/GEMINI/gemini3d/build/gemini.bin /home/gridsan/swoboj/GEMINI/GEMINI_test
