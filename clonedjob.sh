#!/bin/bash                      
#SBATCH -t 03:30:00          # walltime 
 
#SBATCH --gres=gpu:1       # GPU access
#SBATCH --mem=16G
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
conda activate down_torch
# gpustat_
python  yinruiqing_trial.py first_min_030327.wav
#python3 speechbox_trial.py /om/user/arjunp/third_min_030327.wav
#python firstscript.py  



# echo job info on joblog:
echo "Job $JOB_ID ended on:   " `hostname -s`
echo "Job $JOB_ID ended on:   " `date `
echo " "

 