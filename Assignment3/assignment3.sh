#!/bin/bash


for i in {1..16}
do
export BLASTDB=/local-fs/datasets/
blastp -query MCRA.faa -db refseq_protein/refseq_protein -num_threads 1 -outfmt 6 >> blastoutput.txt
done
