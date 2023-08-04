# Accessory_Scripts

## reference_gap_remover
Given a MSA and a ref seq, the script will remove all columns in which the reference has a gap. 
The output will be a trimmed MSA. It's useful to generate trim an MSA with > 5000 columns, which is incompatible with SDPfox.

## seq_renamer
Comes from seq_rename_v2.py. The script renames all the sequences in a fasta file with a 10 digit string. The user can add a key to identify the sequences with argument `-id`, which should be a 3 or 4 letter code for the sequences in the fasta file (for example, `-id ath` to indicate the sequences come from _Arabidopsis thaliana_). The 10 digits will be completed with increasing numbers starting with ath0000001 in the example. An output file (`file_map`) with will be generated, showing the corresponding oringinal sequence name to each new name. It is recommended to remove all spaces in sequences names in the original files before running the script.

## SuperDuPerFOX
A script that allows to automatize the preparation of files for SDPfox, and executes SDPfox (mode: sdplight). 
The script takes a list of files (.txt) with sequences IDs (endline-separated), and an aligned fasta file (`-i`).
A grouped file to be used as SDPfox input (-o) is automatically prepared, in a way that the sequences in a filename.txt
will be put together, tagged with ===filename===, the same for filename2.txt (tagged ===filename2===, and so on. 
If there are sequences in the .txt absent in the fasta file, the script will stop and print a warning. 
If there are sequencess in the fasta file but not in neither of the .txt files, they will be placed first in the output as ungrouped.
Finally, the script will execute SDPfox (`-m sdplight`) with a reference sequence indicated by `-ref`, generating an output file (`-sfo`).
The SDPfox output file prints the full alignment at the end: to remove it use `-clean yes`. This is useful if the file will be used
for MICS script later on.

## bad_seqs_remover
comes from bad_seqs_v03.py.
Allows to parse a fasta file (aligned or not) and remove sequences with non-IUPAC characters. 

