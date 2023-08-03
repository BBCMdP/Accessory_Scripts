from Bio import SeqIO
import os
import glob
import argparse

'''
7/7/2023
FV with assistance from ChatGPT

The script takes a list of files (.txt) with sequences IDs, and an aligned fasta file (-i).
A grouped file to be used as SDPfox input (-o) is automatically prepared, in a way that the sequences in a filename.txt
will be put together, tagged with ===filename===, the same for filename2.txt (tagged ===filename2===, and so on. 
If there are sequences in the .txt absent in the fasta file, the script will stop and print a warning. 
If there are seqs in the fasta file but not in neither of the .txt files, they will be placed as ungrouped.
Finally, the script will execute SDPfox (-m sdplight) with a reference sequence indicated by -ref, generating an output file (-sfo).
The SDPfox output file prints the full alignment at the end: to remove it use "-clean yes". This is useful if the file will be used
for MICS script later on.  
'''


parser = argparse.ArgumentParser(description=f'The script takes a list of files (.txt) with sequences IDs, and an aligned fasta file (-i). A grouped file to be used as SDPfox input (-o) is automatically prepared, in a way that the sequences in a filename.txt will be put together, tagged with ===filename===, the same for filename2.txt (tagged ===filename2===, and so on. If there are sequences in the .txt absent in the fasta file, the script will stop and print a warning. If there are seqs in the fasta file but not in neither of the .txt files, they will be placed as ungrouped. Finally, the script will execute SDPfox (-m sdplight) with a reference sequence indicated by -ref, generating an output file (-sfo). The SDPfox output file prints the full alignment at the end: to remove it use "-clean yes". This is useful if the file will be used for MICS script later on.')
parser.add_argument('-i', default='input_fasta.faa', help='name of the aligned FASTA file')
parser.add_argument('-o', default='grouped_fasta.faa', help='name of the output, grouped, FASTA file')
parser.add_argument('-sfo', default='grouped_fasta_SDPfox_output', help='name of the SDPfox output')
parser.add_argument('-ref', default='ref_seq', help='name of the reference sequence for SDPfox')
parser.add_argument('-clean', default='no', help='Remove alignment from SDPfox output: yes/no')

args = vars(parser.parse_args())

def process_sequences(txt_folder, faa_file, output_file):
    # Get a list of all the .txt files in the folder
    txt_files = glob.glob(os.path.join(txt_folder, '*.txt'))
    
    # Read the sequences from the txt files
    sequences = set()
    headers = {}
    for txt_file in txt_files:
        file_name = os.path.splitext(os.path.basename(txt_file))[0]
        with open(txt_file, 'r') as f:
            for line in f:
                sequence = line.strip()
                sequences.add(sequence)
                headers[sequence] = file_name
    
    # Read the sequences from the fasta file
    fasta_sequences = []
    with open(faa_file, 'r') as f:
        for record in SeqIO.parse(f, 'fasta'):
            sequence = str(record.seq)
            fasta_sequences.append((record.id, sequence))
    
    # Check if all sequences from the txt files are present in the fasta file
    missing_sequences = sequences - set([seq[0] for seq in fasta_sequences])
    if missing_sequences:
        print("There are sequences missing in your fasta file.")
        return
    
    # Write the output to the output_file
    with open(output_file, 'w') as f:
        # Write the sequences from the fasta file that are not in the txt files
        for sequence_id, sequence in fasta_sequences:
            if sequence_id not in sequences:
                f.write(f'>{sequence_id}\n{sequence}\n')
        
        # Write the sequences from the txt files
        for txt_file in txt_files:
            file_name = os.path.splitext(os.path.basename(txt_file))[0]
            f.write(f'==={file_name}===\n')
            with open(txt_file, 'r') as txt:
                for line in txt:
                    sequence = line.strip()
                    f.write(f'>{sequence}\n')
                    f.write(f'{fasta_sequences[[seq[0] for seq in fasta_sequences].index(sequence)][1]}\n')

def SDPfoxer(input,ref,sdpfox_output):
    os.system("java -jar SDPfox.jar -o " + str(sdpfox_output) + " -i " + str(input) + " -ref " + str(ref) + " -m sdplight")

arguments = []

faa_file = str(args['i'])
grouped_file = str(args['o'])
sdpfox_output  = str(args['sfo'])
ref = str(args['ref'])
clean = str(args['clean']) 

arguments.append(faa_file)
arguments.append(grouped_file)
arguments.append(sdpfox_output)
arguments.append(ref)
arguments.append(clean)

txt_folder = './'  # Replace with the folder containing your .txt files

process_sequences(txt_folder, faa_file, grouped_file)
SDPfoxer(grouped_file,ref,sdpfox_output)

if clean == 'yes':
   os.system("sed -i '/Alignment:/,$d' " + str(sdpfox_output))
