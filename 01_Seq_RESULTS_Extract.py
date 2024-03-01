import os
import shutil

# Define the parent directory
parent_dir = './'

# Define the target directory
target_dir = os.path.join(parent_dir, 'SEQ_RESULTS')

# Check if the target directory exists, if not, create it
if not os.path.exists(target_dir):
    os.makedirs(target_dir)
else:
    # If the target directory exists, delete all files in it
    for file in os.listdir(target_dir):
        file_path = os.path.join(target_dir, file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Error while deleting file {file_path}. Reason: {e}")

# Get a list of all directories and files in the parent directory
dirs_files = os.listdir(parent_dir)

# Iterate over each item
for item in dirs_files:
    # Construct full item path
    item_path = os.path.join(parent_dir, item)
    # Check if the item is a directory and its name starts with 'Results_'
    if os.path.isdir(item_path) and item.startswith('Results_'):
        # Get a list of all files in the directory
        files = os.listdir(item_path)
        # Iterate over each file
        for file in files:
            # Check if the file name starts with 'RESULT' and ends with '.faa'
            if file.startswith('RESULT') and file.endswith('.faa'):
                # Construct full file paths
                source = os.path.join(item_path, file)
                target = os.path.join(target_dir, file)
                # Handle file name conflicts
                if os.path.exists(target):
                    base, extension = os.path.splitext(file)
                    i = 1
                    while os.path.exists(target):
                        target = os.path.join(target_dir, f"{base}_{i}{extension}")
                        i += 1
                try:
                    # Copy the file
                    shutil.copy2(source, target)
                except IOError as e:
                    print(f"Unable to copy file {source} to {target}. Reason: {e}")
                except:
                    print(f"Unexpected error occurred while copying file {source} to {target}.")
            elif file.endswith('.log'):
                # Construct full file paths
                source = os.path.join(item_path, file)
                target = os.path.join(target_dir, file)
                # Handle file name conflicts
                if os.path.exists(target):
                    base, extension = os.path.splitext(file)
                    i = 1
                    while os.path.exists(target):
                        target = os.path.join(target_dir, f"{base}_{i}{extension}")
                        i += 1
                try:
                    # Open the source file and the target file
                    with open(source, 'r') as src_file, open(target, 'w') as tgt_file:
                        lines = src_file.readlines()
                        # Copy fasta name
                        tgt_file.write(lines[7])
                        # Find the line containing 'INFO - Total Sequences'
                        for line in lines:
                            if 'INFO - Total Sequences' in line:
                                tgt_file.write(line)
                                break
                        # Find the line containing 'INFO - SSR'
                        for line in lines:
                            if 'INFO - SSR' in line:
                                tgt_file.write(line)
                                break
                        # Find the line containing 'INFO - NHHR'
                        for line in lines:
                            if 'INFO - NHHR' in line:
                                tgt_file.write(line)
                                break
                        # Find the line containing 'INFO - GIR'
                        for line in lines:
                            if 'INFO - GIR' in line:
                                tgt_file.write(line)
                                break
                        # Find the line containing 'INFO - CGSR'
                        for line in lines:
                            if 'INFO - CGSR' in line:
                                tgt_file.write(line)
                                break
                        # Find the line containing 'INFO - PR'
                        for line in lines:
                            if 'INFO - PR' in line:
                                tgt_file.write(line)
                                break
                        # Find the line containing 'INFO - RESULT'
                        for line in lines:
                            if 'INFO - RESULT' in line:
                                tgt_file.write(line)
                                break
                except IOError as e:
                    print(f"Unable to copy file {source} to {target}. Reason: {e}")
                except:
                    print(f"Unexpected error occurred while copying file {source} to {target}.")
