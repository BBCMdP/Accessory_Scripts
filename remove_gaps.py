#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
Created on Thu Jul  4 16:31:34 2019

@author: Nicolas Stocchi
"""

import re
import glob
from Bio import SeqIO
from datetime import datetime
startTime = datetime.now()

numbers = re.compile(r'(\d+)')


def numericalSort(value):

    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])

    return parts


def input_files(ftype):

    list_of_files = sorted((glob.glob(ftype)), key=numericalSort)

    return list_of_files


def seqs_extractor(fasta_file):

    names = []
    seqs = []

    for seq_record in SeqIO.parse(fasta_file, "fasta"):
        names.append(seq_record.id)
        seqs.append(seq_record.seq)

    return names, seqs


def remove_gaps(fasta_file):

    names, seqs = seqs_extractor(fasta_file)
    
    seqs_wo_gaps = []
    
    for seq in seqs:
        str_seq = ""

        for aa in seq:
            if aa != "-":
                str_seq += aa

        seqs_wo_gaps.append(str_seq)
    
    filename = str((fasta_file.split(".")[:-1])[0])
    output_file = str(filename) + ".fsa"
    
    f1 = open(output_file, "w")
    for name, seq in zip(names, seqs_wo_gaps):
        f1.write(">" + str(name) + "\n")
        f1.write(str(seq) + "\n")
    f1.close()
    
    return output_file

list_of_fasta = input_files("*.faa")

for fasta in list_of_fasta:
    output_file = remove_gaps(fasta)
    print('Output faa ' + str(output_file) + ' generated' + 
    ' - Total time: ' + str((datetime.now() - startTime)))
