#!/bin/bash
#SBATCH --mail-type=ALL
#SBATCH --mail-user=m.a.schepers@st.hanze.nl
#SBATCH --time 4:00:00
#SBATCH --nodes=1
#SBATCH --cpus-per-task=16
#SBATCH --job-name=assignment4_maschepers
#SBATCH --partition=assemblix

export FILE1=/data/dataprocessing/MinIONData/MG5267/MG5267_TGACCA_L008_R1_001_BC24EVACXX.filt.fastq
export FILE2=/data/dataprocessing/MinIONData/MG5267/MG5267_TGACCA_L008_R2_001_BC24EVACXX.filt.fastq

# Run velveth and velvetg
velveth output 21 -fastq -short $FILE1 -shortPaired $FILE2
velvetg output -exp_cov auto -cov_cutoff auto

# mkdir -p output

