# Check SeqIO for parsing .fa files and calculating the N50

from Bio import SeqIO
import sys

FileIn = '/homes/maschepers/Documents/GithubRepos/programming3/Assignment4/output/contigs.fa'

def contig_parser(file):
    handle = open(file, 'r')
    SeqRecords = SeqIO.parse(handle, 'fasta')
    len_list = []  # create list to store lengths
    for record in SeqRecords:   # loop through each fasta entry
        length = len(record.seq)    # get sequence length
        # print(length)  # print("%s: %i bp" % (record.id, length))
        len_list.append(length)


def calculate_N50(list_of_lengths):
    """
    Calculate N50 for a sequence of numbers.
    Args:list_of_lengths (list): List of numbers.
    Returns:float: N50 value.
    """
    tmp = []
    for tmp_number in set(list_of_lengths):
            tmp += [tmp_number] * list_of_lengths.count(tmp_number) * tmp_number
    tmp.sort()
 
    if (len(tmp) % 2) == 0:
        median = (tmp[int(len(tmp) / 2) - 1] + tmp[int(len(tmp) / 2)]) / 2
    else:
        median = tmp[int(len(tmp) / 2)]
 
    return median


lenghts = contig_parser(FileIn)
print(calculate_N50(lenghts))