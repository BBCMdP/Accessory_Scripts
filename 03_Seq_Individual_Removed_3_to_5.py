import os
import glob

# Get the current directory
current_directory = os.getcwd()

# Create a list to store the content of the files
content_list = []

# Loop through the directories that start with 3, 4, or 5
for i in range(3, 6):
    # Use glob to find all .fsa files that end with 'hits_removed' in the directory
    for file in glob.glob(f"{current_directory}/{i}*/**/*hits_removed.fsa", recursive=True):
        # Open each file and append its content to the list
        with open(file, 'r') as f:
            content_list.append(f.read())

# Create a new file with '_removed' at the end and .fsa extension
with open(f"{current_directory}/{os.path.basename(current_directory)}_removed.fsa", 'w') as f:
    # Write the content of the list to the file
    f.write('\n'.join(content_list))