import os
import numpy as np
from PIL import Image, ImageChops

# Function to get filename from path
def get_file_name(file_path):
    return os.path.splitext(os.path.basename(file_path))[0]

# Read the raw file
dphfilepath = "frame_000_0332.dph"
with open(dphfilepath, 'rb') as f:
    raw_image = np.fromfile(f, dtype=np.uint16)

# Set the width and height of the image
width, height = 640, 400

# Reshape the raw image array to the specified width and height
raw_image = raw_image.reshape(height, width)

# Define downsampling factor
downsample_factor = 1

# Downsample the image and coordinates
downsampled_image = raw_image[::downsample_factor, ::downsample_factor]
downsampled_x_coords = np.arange(0, width, downsample_factor)
downsampled_y_coords = np.arange(0, height, downsample_factor)

# Create x and y coordinates for the downsampled point cloud
x_coords, y_coords = np.meshgrid(downsampled_x_coords, downsampled_y_coords)

# Flatten the x and y coordinates and the downsampled image values
x = x_coords.flatten()
y = y_coords.flatten()
z = downsampled_image.flatten()

# Set the scaling factor for the Z-axis
z_scale = 0.5

# Scale the Z-axis values
scaled_z = z * z_scale

# Define pixel offsets for the x and y directions
x_offset = -80
y_offset = 0

# Read the color image (1280x800) from the .img file with the same name as the DPH file
imgfilepath = get_file_name(dphfilepath) + '.img'
color_image = Image.open(imgfilepath)

# Apply the pixel offset to the color image
offset_color_image = ImageChops.offset(color_image, xoffset=x_offset, yoffset=y_offset)

# Downsample the offset color image to 640x400
offset_color_image = offset_color_image.resize((640, 400))

# Extract RGB values from the downscaled color image
b, g, r = offset_color_image.split()
r_vals = np.array(r).flatten()
g_vals = np.array(g).flatten()
b_vals = np.array(b).flatten()

# Flip the y-coordinates vertically
y = height - y
x = width - x

# Save the point cloud with color information as an ASCII file
output_file = '_'+get_file_name(dphfilepath) + '_with_color.txt'
point_cloud = np.column_stack((x, y, scaled_z, r_vals, g_vals, b_vals))
np.savetxt(output_file, point_cloud, fmt='%.6f', delimiter=' ')
print("Point cloud with color saved as " + output_file)

input("*******************\nPress enter to exit\n*******************")
