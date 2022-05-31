#!/bin/bash
#SBATCH --job-name=assignment3_maschepers
export BLASTDB=/local-fs/datasets/

mkdir -p output

for n in {1..16}
do /usr/bin/time -o output/timings.txt --append -f "${n}:%e" blastp -query MCRA.faa -db refseq_protein/refseq_protein -num_threads $n -outfmt 6 >> blastoutput.txt
done

python3 assignment3.py