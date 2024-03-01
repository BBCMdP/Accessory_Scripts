import os
import shutil
import subprocess

# Get the current working directory
cwd = os.getcwd()

# The script to be copied and executed
script_name = '03_Seq_Individual_Removed_3_to_5.py'

# Iterate over all items in the directory
for item in os.listdir(cwd):
    # If the item is a directory
    if os.path.isdir(item):
        # Copy the script into the directory
        shutil.copy(script_name, item)

        # Change the working directory to the subdirectory
        os.chdir(item)

        # Execute the script
        subprocess.run(['python3', script_name])

        # Iterate over all items in the subdirectory
        for subitem in os.listdir('.'):
            # If the subitem ends with 'hits_removed' and has a .fsa extension
            if subitem.endswith('hits_removed.fsa'):
                # Move the file to the initial directory
                shutil.move(subitem, cwd)

        # Change the working directory back to the initial directory
        os.chdir(cwd)