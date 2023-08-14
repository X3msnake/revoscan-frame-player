import os

# Read the list of filenames from the text file
with open("x.files", "r") as file:
    filenames = file.read().splitlines()

# Iterate through the filenames and rename the files
for filename in filenames:
    for extension in [".inf", ".img", ".dph"]:
        original_filename = filename + extension
        new_filename = original_filename + ".x"
        
        if not os.path.exists(new_filename):
            os.rename(original_filename, new_filename)
            print(f"Renamed {original_filename} to {new_filename}")
        else:
            print(f"{new_filename} already exists, skipping")

print("File renaming completed.")
