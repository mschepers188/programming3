#!/bin/bash

#export BLASTDB=/local-fs/datasets/
n=25

mkdir -p output

for n in {1..16}
do /usr/bin/time -o output/test.txt --append -f "${n}:%e" echo "Hello"
done
