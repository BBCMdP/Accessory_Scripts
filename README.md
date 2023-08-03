# Accessory_Scripts

## reference_gap_remover
Given a MSA and a ref seq, the script will remove all columns in which the reference has a gap. 
The output will be a trimmed MSA. It's useful to generate trim an MSA with > 5000 columns, which is incompatible with SDPfox.

## seq_renamer
Comes from seq_rename_v2.py. The script renames all the sequences in a fasta file with a 10 digit string. The user can add a key to identify the sequences with argument `-id`, which should be a 3 or 4 letter code for the sequences in the fasta file (for example, `-id ath` to indicate the sequences come from _Arabidopsis thaliana_). The 10 digits will be completed with increasing numbers starting with ath0000001 in the example. An output file (`file_map`) with will be generated, showing the corresponding oringinal sequence name to each new name. It is recommended to remove all spaces in sequences names in the original files before running the script.

## SuperDuPerFOX
