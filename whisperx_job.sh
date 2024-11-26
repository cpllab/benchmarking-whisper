#!/bin/bash                      
#SBATCH -t 06:30:00          # walltime 
#SBATCH --gres=gpu:QUADRORTX6000:1        
#SBATCH --mem=32G
# echo job info on joblog:
echo "Job $JOB_ID started on:   " `hostname -s`
echo "Job $JOB_ID started on:   " `date `
echo " "

# Execute commands to run your program here, taking Python for example,

source /etc/profile.d/modules.sh
module load openmind8/anaconda/3-2023.09-0
module load openmind8/cuda/12.1                 
module load openmind8/cudnn/8.8.1-cuda12   
module load openmind/gcc/11.1.0
module load openmind/ffmpeg/20160310 

source ~/.bashrc
#conda activate whisperx 
#python3 whisperx_demo.py 'chunks_34_KS_Recording4-LR_2165-2465_CT/minute_1.wav'
conda activate r_env 
cd wget
python3 /om/user/arjunp/transferwee.py download https://talkbank.wetransfer.com/downloads/e96311495e5e5af4256e72fda2c081ff20240821011110/0eb47efb1814fd4bf6019258758b6e8820240821011110/2b5c95

# echo job info on joblog:
echo "Job $JOB_ID ended on:   " `hostname -s`
echo "Job $JOB_ID ended on:   " `date `
echo " "

 