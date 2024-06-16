import os

# Define the root directory for your project
project_root = '.'

# Define the output file
output_file = 'SPCK.files'

# List of directories to ignore
ignore_dirs = ['.git']

# List of file extensions to ignore
ignore_extensions = [
    '.cflags', '.config', '.creator', '.creator.user',
    '.cxxflags', '.files', '.includes'
]

# Function to list all files while ignoring specified directories and file extensions
def list_files(root):
    with open(output_file, 'w') as f:
        for current_path, directories, files in os.walk(root):
            # Skip ignored directories
            directories[:] = [d for d in directories if d not in ignore_dirs]
            for file in files:
                if any(file.endswith(ext) for ext in ignore_extensions):
                    continue
                file_path = os.path.relpath(os.path.join(current_path, file), project_root)
                f.write(file_path.replace('\\', '/') + '\n')

# Run the function
list_files(project_root)

print(f"All files (excluding ignored directories and file extensions) have been listed in {output_file}.")
