#!/usr/bin/env python

###############################################################################
#1.Name: FastaHeaderConvert.py                                                #
#2.Description: Converts fasta headers to a ten-digit number. It also creates #
# a csv with the corresponding relations.                                     #
#3.Required libraries: sys, biopython, datetime                               #
#4.Inputs: fasta file                                                         #
#5.Execution: python FastaHeaderConvert.py                                    #
#6.Keywords: sequences, fasta, convert, header                                #
#7.Author: Nicolas Stocchi, UNMdP-IIB-CONICET, Argentina                      #
###############################################################################

import sys
from Bio import SeqIO
from datetime import datetime
startTime = datetime.now()

try:
    fasta_file = str(raw_input('Please, enter the name of your fasta file\n'))
except SyntaxError:
    print("Sorry, you put the wrong input, please try again")
    sys.exit()


def seqs_extractor(file_fasta):
    names = []
    seqs = []
    for seq_record in SeqIO.parse(file_fasta, "fasta"):
        names.append(seq_record.id)
        seqs.append(seq_record.seq)
    return names, seqs

names, seqs = seqs_extractor(fasta_file)

new_names = []

for name, l in zip(names, range(1, len(names) + 1)):
    nn = str(l).zfill(10)
    new_names.append(nn)

with open("renamed_" + str(fasta_file), "w") as f1:
    for i, j in zip(new_names, seqs):
        f1.write(">" + str(i) + "\n")
        f1.write(str(j) + "\n")
f1.close()

with open("file_map", "w") as f2:
    for i, j in zip(new_names, names):
        print >> f2, i, '\t', j
f2.close()

print(("Execution Successful: " + str((datetime.now() - startTime))))
