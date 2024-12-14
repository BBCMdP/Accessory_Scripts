import os
import glob

# Get a list of all .faa files in the current directory
faa_files = glob.glob('./*.faa')

output_file = 'concatenated.faa'

# Open the output file in write mode
with open(output_file, 'w') as outfile:
    for filename in faa_files:
        # Open each .faa file read mode
        with open(filename, 'r') as infile:
            # Write the contents of the .faa file to the output file
            outfile.write(infile.read())

# Check if the file was created successfully
if os.path.exists(output_file):
    print(f"The file {output_file} was created successfully.")
else:
    print(f"Failed to create the file {output_file}.")