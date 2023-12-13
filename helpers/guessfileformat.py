import puremagic
import sys

def detect_file_type(file_path):
    magic = puremagic.magic_file(file_path)
    return magic

# Check if a file path is provided as a command-line argument
if len(sys.argv) > 1:
    file_path = sys.argv[1]
    file_type = detect_file_type(file_path)
    print(f"The detected file type is: {file_type}")
else:
    print("Please drop a file onto the script.")

input("Press Enter to continue...")
