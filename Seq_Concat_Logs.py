import os
import glob

# Change directory to the one containing the log files
os.chdir('./')

# Get a list of all files that start with 'Seqrutinator_' and end with '.log'
log_files = glob.glob('Seqrutinator_*.log')

try:
    # Open 'All_Sequences.log' in write mode
    with open('../All_Sequences.log', 'w') as outfile:
        # Loop through the list of log files
        for filename in log_files:
            # Open each log file in read mode
            try:
                with open(filename, 'r') as infile:
                    # Read the content of the log file and write it to 'All_Sequences.log'
                    outfile.write(infile.read())
            except IOError:
                print(f"Error reading file {filename}")
except IOError:
    print("Error writing to 'All_Sequences.log'")

# Check if 'All_Sequences.log' was successfully created
if os.path.isfile('../All_Sequences.log'):
    print("'All_Sequences.log' was successfully created.")
else:
    print("'All_Sequences.log' was not created.")