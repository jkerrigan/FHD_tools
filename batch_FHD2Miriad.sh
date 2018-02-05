#!/bin/bash
#SBATCH -t 1:00:00
#SBATCH -n 1                                                                                                  
####SBATCH --array=0-64:1%25
#SBATCH --array=66-73:1
                                     
#SBATCH -p default-batch
#SBATCH --mem=20G
source activate PAPER

cd ~/data/shared/HERA_new/IDR1/
obsids=(zen.*.*.xx.HH.uvOR)
obs=${obsids[$SLURM_ARRAY_TASK_ID]}
obs=(${obs//.xx.HH.uvOR/ })

base_path=/users/jkerriga/data/jkerriga/HERAFHD/fhd_IDR1_PSPEC
vis_data_path=${base_path}/vis_data
metadata_path=${base_path}/metadata

cd ~/scratch/FHD_tools/
python sav2miriad.py --subtract --keepcal ${vis_data_path}/${obs}* ${metadata_path}/${obs}*

