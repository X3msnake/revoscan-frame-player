# ----------------------------------------------------------------------------------------------------------------------
# By: X3msnake, made with the help of ai (chatGPT)
# License: Creative commons Zero
# ----------------------------------------------------------------------------------------------------------------------
# Revoscan - Project from folders generator
#
# Usage:
# 1. Ensure the script is located inside the project folder.
# 2. The project folder should have a 'data' subdirectory containing one or more scans subdirectories.
# 3. Run this script to generate a JSON  project.revo file.
#
# Note:
# - The project name and .revo filename will be based on the folder name where the script is located.
# - The 'size' field in the generated JSON is a placeholder, as size information is not provided in the example.
#
# Example:
# - If the script is placed in 'Project01072024124920' folder the generated Output will be: Project01072024124920.revo
#
# ----------------------------------------------------------------------------------------------------------------------

import os
import json
from datetime import datetime

def get_directory_info(directory_path):
    # Get the list of files and subdirectories in the given directory
    items = os.listdir(directory_path)
    
    # Filter out subdirectories only
    subdirectories = [item for item in items if os.path.isdir(os.path.join(directory_path, item))]
    
    return {
        "directory_path": directory_path,
        "subdirectories": subdirectories
    }

def scan_data_folder(project_path):
    data_folder_path = os.path.join(project_path, "data")

    if not os.path.exists(data_folder_path) or not os.path.isdir(data_folder_path):
        print("Error: 'data' folder not found.")
        return None

    # Get the list of subdirectories in the data folder
    subdirectories = [item for item in os.listdir(data_folder_path) 
                      if os.path.isdir(os.path.join(data_folder_path, item))]

    # Create a dictionary to store information about each subdirectory
    data_info = {}

    for subdir in subdirectories:
        subdir_path = os.path.join(data_folder_path, subdir)
        data_info[subdir] = get_directory_info(subdir_path)

    return data_info

def generate_revo_json(project_name, data_info):
    timestamp = int(datetime.now().timestamp())
    nodes = []

    for subdir, info in data_info.items():
        node = {
            "childs": [],
            "guid": subdir,
            "name": subdir,
            "type": 2
        }
        nodes.append(node)

    revo_json = {
        "edit_time": str(timestamp),
        "guid": project_name,
        "model_mesh_count": len(data_info),
        "model_pointcloud_count": 0,
        "name": project_name,
        "nodes": nodes,
        "scan_scene": {},
        "size": "0",  # Placeholder value, as size information is not provided in the example
        "version": "1.1"
    }

    return revo_json

def save_revo_json(revo_json, output_file_path):
    with open(output_file_path, 'w') as json_file:
        json.dump(revo_json, json_file, indent=2)
    print(f"JSON .revo file saved to: {output_file_path}")

if __name__ == "__main__":
    # Get the current script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Use the current script's directory name as the project name and output filename
    project_name = os.path.basename(script_dir)
    output_file_path = f"{project_name}.revo"

    # Scan the data folder for unique directories
    data_info = scan_data_folder(script_dir)

    if data_info:
        # Generate JSON .revo based on the scanned data
        revo_json = generate_revo_json(project_name, data_info)

        # Save the generated JSON .revo to a file
        save_revo_json(revo_json, output_file_path)
