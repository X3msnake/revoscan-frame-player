import os
import numpy as np
import polyscope as ps

# Function to get filename from path
def get_file_name(file_path):
    return os.path.splitext(os.path.basename(file_path))[0]

# Load the point cloud data with color information from the ASCII file
file_path = "_frame_000_0332_with_color.txt"
point_cloud_data = np.loadtxt(file_path)

# Separate the x, y, z coordinates and color information
x, y, z, r, g, b = point_cloud_data[:, 0], point_cloud_data[:, 1], point_cloud_data[:, 2], point_cloud_data[:, 3], point_cloud_data[:, 4], point_cloud_data[:, 5]

# Initialize Polyscope
ps.init()

# Create a new point cloud visualization using the imported points
ps_cloud = ps.register_point_cloud("my points", np.column_stack((x, y, z)))

# Generate the RGB color values per-point
vals = np.column_stack((r, g, b))

# Add the color quantity to the point cloud visualization
ps_cloud.add_color_quantity("color", vals)

# Show the point cloud in the Polyscope viewer
ps.show()