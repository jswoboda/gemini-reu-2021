

# Building GEMINI on MIT Supercloud


For some more detailed information on software, various commands, and requesting an account see: https://supercloud.mit.edu/
To begin, GEMINI must be first installed on the login node because compute nodes do not have an internet connection:
```bash
ssh <username>@txe1-login.mit.edu 
```

Building GEMINI on Supercloud is not too different than setting up on a personal computer:
```bash
git clone https://github.com/gemini3d/gemini3d.git
cd gemini3d
```
Depending on the internet connection this may take up to a minute or so. If git takes too long or doesn't work, the internet may be down (happened before). If this occurs contact supercloud@mit.edu and they can reset the connection.

CMake on Supercloud is outdated. To update it and add the path to our environment, we can do:
```bash
cmake -P scripts/install_cmake.cmake
export PATH="$HOME/cmake-3.21.0-linux-x86_64/bin:$PATH"
#If cmake  isn't in home directory, do something like: export PATH="$HOME/mydir/mysubdir/cmake-3.21.0-linux-x86_64/bin:$PATH"
# 	
```

MPI is needed to build. Load it and build:
```bash
module load mpi/openmpi-4.1.0
cmake -B build
cmake --build build -j
```
A full compile will take approximate 1-5 minutes depending on which packages need to be compiled; you will see lots of warnings but these can be safely ignored.  Executables are placed in the ```build``` directory and can be run from there.  

Another important software to install is PyGemini. PyGemini is a Python frontend for GEMINI. It contains several useful utilities such as grid generation and input interprolation. Install it with Anaconda.

``` bash
module load anaconda/2021a 
git clone https://github.com/gemini3d/pygemini
pip install --user -e pygemini
```

PyGEMINI needs enviroment variable GEMINI_ROOT to be set to top level Gemini directory. NOTE: There should be a way to do this permanently, but editing .profile and .bashrc don't work. For now you have to do this once every shell session you want to use PyGemini
 
``` bash
 export GEMINI_ROOT=/insert_path_here/gemini3d/
```
# Running an example
To make sure everything is working as intended, let's try creating and running an example:
``` bash
cd ~
mkdir GEMINI_test
cd GEMINI_test
nano config.nml
```

Paste the following into config.nml:

``` bash
&base
ymd = 2021,10,5       ! year month day date
UTsec0 = 0.0            !start time in seconds
tdur = 600.0             !tdur: length of sim in seconds
dtout = 120.0                          !dtout: how often to do output
activ=104.7,129.5,37.0              !activ:  f107a,f107,Ap
tcfl=0.9                           !tcfl:  target cfl number
Teinf=1500.0                        !Teinf:  exospheric electron temperature
/

&flags
potsolve = 0        ! solve electrodynamics:   0 - no; 1 - electrostatic; 2 - inductive
flagperiodic = 0    ! whether periodic
flagoutput = 1      ! 1 - full parameter output
/

&setup
glat=55
glon=285
xdist = 2500e3              ! eastward distance (meters)
ydist = 4500e3               ! northward distance (meters)
alt_min = 80e3              ! minimum altitude (meters)
alt_max = 900e3             ! maximum altitude (meters)
!alt_scale = 6e3, 1e3, 500e3, 150e3  ! altitude grid scales (meters)
alt_scale = 10.9e3, 8e3, 500e3, 150e3
lxp  = 102              ! number of x-cells
lyp = 128                   ! number of y-cells
Bincl = 90                  ! geomagnetic inclination
nmf = 5e11
nme = 2e11
/

&files
indat_size = 'inputs/simsize.h5'
indat_grid = 'inputs/simgrid.h5'
indat_file = 'inputs/initial_conditions.h5'
/

``` 

Now, we can try seting up the input files. A Python script works, but ipython may be easier

``` bash
ipython
import gemini3d.model as g
g.setup("config.nml",'.')
exit
```
For somewhat large grids (>1M grid cells), this may take a while. Ours should take about a minute or two.
### Batch job submission ###
Now to run the example. Supercloud uses a SLURM scheduler, for this example we will must use of it. Create a batch file like so:
``` bash
nano gemini_test.sh
```

Here is a batch script that will run our example. Make sure to use the appropiate directory names when applicable. We are using only 256 cores, but theoretically one could use up to 8 nodes x 48 cores = 384 cores. One difficult aspect of running a simulation on Supercloud is determining an acceptable x2 x x3 dimension for the number of cores being used. Here, our 256 cores are being split into a process grid of 4x64 where 4 divides into 108, and 64 divides into 128. Future work needs to be done to look more into the most efficent partition setup. Occasionally, if the partition is awkwardly sized, the simulation will run at an extremely slow rate. If you notice this, rerun the simulation with a different amount of cores, or try redefining the dimensions of your grid.


``` text file
#!/bin/bash

#Slurm sbatch options
#SBATCH -N 7 # Number of nodes
#SBATCH -n 256 # Number of cores

#Error & output handling
#SBATCH -o /home/gridsan/iwright/GEMINI_example/out.log-%j #%j refers to job number, so output files are saved with unique name
#SBATCH -e /home/gridsan/iwright/GEMINI_example/error.log-%j

#Initalize module command
source /etc/profile

#Load mpi
module load mpi/openmpi-4.1.0

#Resolve "No Open Fabrics Error" with confusing and long flag list
#From: "What is this message I get when I try to run MPI with the new OpenMPI module?"-> https://supercloud.mit.edu/transition-guide 

OPENMPI_OPTS="${OPENMPI_OPTS} --mca pml ob1 --mca btl openib,self,vader --mca btl_openib_cpc_include rdmacm --mca btl_openib_rroce_enable 1 "
OPENMPI_OPTS="${OPENMPI_OPTS} --mca btl_openib_receive_queues P,128,64,32,32,32:S,2048,1024,128,32:S,12288,1024,128,32:S,65536,1024,128,32 "

#Run the program
mpirun $OPENMPI_OPTS -np $SLURM_NTASKS /home/gridsan/iwright/gemini3d/build/gemini.bin /home/gridsan/iwright/GEMINI_example

```
Finally, to submit the job:
``` batch
sbatch gemini_test.sh
```
To check the status of your current jobs, use 
``` batch
LLstat
```
And if you want to cancel a job, use LLstat to grab the Job ID of the job you want to cancel. Then use:
``` batch
scancel JOB_ID
```
### Interactive job submission ###
An interactive job is more similar to how one would run GEMINI on his/her personal computer. Interactive jobs can be useful in testing to make sure to a job is running correctly. Another helpful flag for testing purposes is ```-dryrun```, this only runs the simulation for the first time step. One thing to note is that interactive jobs have a time limit of 24 hours. To run our example interactively, use:
``` bash
LLsub -i -N 8 -n 256
module load mpi/openmpi-4.1.0
OPENMPI_OPTS="${OPENMPI_OPTS} --mca pml ob1 --mca btl openib,self,vader --mca btl_openib_cpc_include rdmacm --mca btl_openib_rroce_enable 1 "
OPENMPI_OPTS="${OPENMPI_OPTS} --mca btl_openib_receive_queues P,128,64,32,32,32:S,2048,1024,128,32:S,12288,1024,128,32:S,65536,1024,128,32 "
mpirun $OPENMPI_OPTS -np $SLURM_NTASKS /home/gridsan/iwright/gemini3d/build/gemini.bin /home/gridsan/iwright/GEMINI_example

```
# Retrieving files
Once your simulation is finished. Rysnc the files you need to your personal computer. Provided in this repo are some example scripts for doing so (albiet messy at the moment). Perhaps a better option to consider is processing on Supercloud and rsyncing just the plots/tables.

```bash
rsync -av --progress username@txe1-login.mit.edu:~/GEMINI_example .
```
 
