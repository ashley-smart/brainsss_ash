#!/bin/bash
#SBATCH --job-name=brainsss
#SBATCH --partition=bigmem
#SBATCH --time=1-00:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=12
#SBATCH --output=./logs/mainlog.out
#SBATCH --open-mode=append
#SBATCH --mail-type=ALL

ml python/3.6.1
ml antspy/0.2.2
date
python3 -u /home/users/brezovec/projects/brainsss/scripts/anat_moco.py
