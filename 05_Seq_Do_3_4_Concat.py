import subprocess
import glob
import shutil

# Execute the '04_Seq_Execute_and_Extract.py' script
subprocess.run(['python3', '04_Seq_Execute_and_Extract.py'], check=True)

# Find all '.fsa' files ending with 'hits_removed'
files = glob.glob('*hits_removed.fsa')

# Concatenate all found files into 'Removed_Sequences.fsa'
with open('Removed_Sequences.fsa', 'wb') as outfile:
    for file in files:
        with open(file, 'rb') as infile:
            shutil.copyfileobj(infile, outfile)