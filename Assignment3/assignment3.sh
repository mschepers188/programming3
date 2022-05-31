#!/bin/bash
#SBATCH --cpus-per-task=16
export BLASTDB=/local-fs/datasets/

mkdir -p output

for n in {25..26}
do /usr/bin/time -o output/timings.txt --append -f "${n}:%e" blastp -query MCRA.faa -db refseq_protein/refseq_protein -num_threads $n -outfmt 6 >> blastoutput.txt
done