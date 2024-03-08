#!/usr/bin/env python

#################################################################
#   Modified by Fernando Villarreal 04/11/2022                  #
#   Edited for output filenames and compatibility with python 3 #
#   v3 2024-03-08 15:47:09 FV                                   # 
#   edited to deal with spaces in sequence header               #
#   line 32: seq_record.description replaced seq_record.id      # 
#################################################################

import argparse
from Bio import SeqIO
from datetime import datetime
startTime = datetime.now()

### Command Line Arguments ####################################################
parser = argparse.ArgumentParser()
parser.add_argument('-i', default='Fasta file', help='Fasta file')
parser.add_argument('-id', default='KEY', help='ID Key sequence name')

args = vars(parser.parse_args())

fasta_file = str(args['i'])
key = str(args['id'])
###############################################################################
real_fasta = str((fasta_file.split(".")[:-1])[0])

def seqs_extractor(file_fasta):
    names = []
    seqs = []
    for seq_record in SeqIO.parse(file_fasta, "fasta"):
        names.append(seq_record.description)
        seqs.append(seq_record.seq)
    return names, seqs

names, seqs = seqs_extractor(fasta_file)

new_names = []

for name, l in zip(names, list(range(1, len(names) + 1))):
    nk = 10 - len(key)
    nn = str(key) + str(l).zfill(nk)
    new_names.append(nn)

with open(str(real_fasta) + "_renamed.fsa", "w") as f1:
    for i, j in zip(new_names, seqs):
        f1.write(">" + str(i) + "\n")
        f1.write(str(j) + "\n")
f1.close()

with open(str(real_fasta) + "_file_map", "w") as f2:
    for i, j in zip(new_names, names):
        print(i, '\t', j, file=f2)
f2.close()

print(("Execution Successful: " + str((datetime.now() - startTime))))
