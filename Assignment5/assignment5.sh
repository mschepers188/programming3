#!/bin/bash
#SBATCH --mail-type=ALL
#SBATCH --mail-user=m.a.schepers@st.hanze.nl
#SBATCH --time 4:00:00
#SBATCH --nodes=1
#SBATCH --cpus-per-task=16
#SBATCH --job-name=assignment5_maschepers
#SBATCH --partition=assemblix

# Run python file for cleanup
python3 assignment5.py