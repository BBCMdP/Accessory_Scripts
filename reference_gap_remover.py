'''
21/06/2023 15:42
created by FV, using blocks from weblog_generator_v3.py, plus ideas from ChatGPT
Given a MSA and a ref seq, the script will remove all columns in which the reference has a gap. 
The output will be a trimmed MSA. The MSA can now be used to SDPfox. 
'''
import argparse
from Bio import SeqIO

parser = argparse.ArgumentParser()
parser.add_argument('-i', default='input_fasta', help='Insert your FASTA file')
parser.add_argument('-o', default='output_fasta', help='Insert your profile file')
parser.add_argument('-r', default='ref_seq', help='Reference sequence')
args = vars(parser.parse_args())

arguments = []

input_fasta = str(args['i'])
output_fasta = str(args['o'])
ref_seq = str(args['r'])

arguments.append(input_fasta)
arguments.append(output_fasta)
arguments.append(ref_seq)


def seqs_extractor(fasta_file):
    names = []
    seqs = []
    for seq_record in SeqIO.parse(fasta_file, "fasta"):
        names.append(seq_record.id)
        seqs.append(seq_record.seq)
    return names, seqs

names, seqs = seqs_extractor(input_fasta)

if ref_seq != 'ref_seq':
    ref_name = ref_seq
    ref_pos = []

    gf = open(input_fasta, "r")
    lines = gf.readlines()

    for gp, gl in zip(lines, range(0, len(lines))):
        if ref_seq in gp:
            ref_pos = list(lines[gl + 1])
            break

else:
    ref_name = 'ref_seq'
    ref_pos = []

    gf = open(input_fasta, "r")
    lines = gf.readlines()

    for gp, gl in zip(lines, range(0, len(lines))):
        if '>' in gp:
            ref_seq = gp[1:]
            ref_pos = list(lines[gl + 1])
            break

#print(f'List ref_pos: {ref_pos}')
      
if ref_seq == 'ref_seq':
    ref_n = names[0]
    ref_s = seqs[0]
    
    ref_pos = list(ref_s)
    
    rnn = -1
    ref_columns = []
    
    for rp, rn in zip(ref_pos, range(0, len(ref_pos))):
        if rp != '-':
            rnn = rnn + 1
        ref_columns.append(str(rnn))
        

else:
    
    ref_pos = 'none'
    
    for name, seq in zip(names, seqs):
        if name == ref_seq:
            ref_pos = list(seq)
            break

    rnn = -1
    ref_columns = []
    
    for rp, rn in zip(ref_pos, range(0, len(ref_pos))):
        if rp != '-':
            rnn = rnn + 1
        
        ref_columns.append(str(rnn))
#print(f'list ref_columns: {ref_columns}')

ref_num_col = [index for index, entry in enumerate(ref_pos) if entry != '-']
#print(f'list ref_num_col: {ref_num_col}')

col_seqs = []

for seq in seqs:
    new_seq = list(seq)
    col_seq = []
    for c in ref_num_col:
        col_seq.append(new_seq[c])
    col_seqs.append(col_seq)

col_seqs2 = []

for cs in col_seqs:
    cstr = ''.join(cs)
    #print(cstr)
    col_seqs2.append(cstr)

f = open(str(output_fasta), "w")
for name, cols in zip(names, col_seqs2):
    f.write(">" + str(name) + "\n")
    f.write(str(cols) + "\n")
f.close()