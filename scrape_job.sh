#!/bin/bash                      
#SBATCH -t 03:30:00          # walltime 
#SBATCH -n 1                 # one CPU (hyperthreaded) cores
#SBATCH --mem=32G
# echo job info on joblog:
echo "Job $JOB_ID started on:   " `hostname -s`
echo "Job $JOB_ID started on:   " `date `
echo " "

# Execute commands to run your program here, taking Python for example,

source /etc/profile.d/modules.sh
#module load openmind8/cuda/12.1                 
#module load openmind8/cudnn/8.8.1-cuda12   
module load openmind8/anaconda/3-2023.09-0
module load openmind/gcc/11.1.0
module load openmind/ffmpeg/20160310 

source ~/.bashrc
conda activate r_env

python childespyscrape.py 
"67"

# echo job info on joblog:
echo "Job $JOB_ID ended on:   " `hostname -s`
echo "Job $JOB_ID ended on:   " `date `
echo " "

 