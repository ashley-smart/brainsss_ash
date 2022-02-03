#!/bin/bash
#SBATCH --job-name=bm_brainsss_ash
#SBATCH --time=4-00:00:00
#SBATCH --ntasks=1
#SBATCH --partition=trc
##two should comemnt out SBATCH --mem 260G
#SBATCH --cpus-per-task=20
#SBATCH --output=./logs/mainlog.out
#SBATCH --open-mode=append
#SBATCH --mail-type=ALL

ml python/3.6.1
# ml antspy/0.2.2
date
python3 -u /home/users/asmart/projects/brainsss_ash/scripts/main.py
