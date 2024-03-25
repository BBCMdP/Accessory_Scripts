import os
import glob

# Get the current working directory
cwd = os.getcwd()

# Find all files that end with 'hits_removed.fsa'
files = glob.glob(os.path.join(cwd, '*hits_removed.fsa'))

# Open the new file in write mode
with open('Removed_Sequences.fsa', 'w') as outfile:
    for fname in files:
        # Open each file in read mode
        with open(fname) as infile:
            # Write the contents of each file to the new file
            for line in infile:
                outfile.write(line)