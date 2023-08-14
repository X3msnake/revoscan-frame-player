import os

# Get the current directory
current_directory = os.getcwd()

# Iterate over the files in the directory
for file_name in os.listdir(current_directory):
    if file_name.endswith(".x"):
        # Remove the ".x" extension from the file name
        new_file_name = file_name[:-2]
        os.rename(file_name, new_file_name)
        print(f"File {file_name} renamed to {new_file_name}.")

print("Script execution completed.")
