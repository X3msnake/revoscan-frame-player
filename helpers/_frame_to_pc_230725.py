import os
import numpy as np
from PIL import Image, ImageChops

# Function to get filename from path
def get_file_name(file_path):
    return os.path.splitext(os.path.basename(file_path))[0]

# Function to read a DPH file and create a colored point cloud
def create_colored_point_cloud(dph_file, output_folder):
    # Read the raw file
    with open(dph_file, 'rb') as f:
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
    img_file = get_file_name(dph_file) + '.img'

    if not os.path.exists(img_file):
        # If the corresponding img file does not exist, use standard color (R0B210G230) for all points
        r_vals, g_vals, b_vals = 0, 210, 230
    else:
        color_image = Image.open(img_file)

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
    output_file = os.path.join(output_folder, 'pframes', '_' + get_file_name(dph_file) + '_with_color.txt')
    point_cloud = np.column_stack((x, y, scaled_z, r_vals, g_vals, b_vals, z))
    np.savetxt(output_file, point_cloud, fmt='%.6f', delimiter=' ')
    print("Point cloud with color saved as " + output_file)
    
    # Save the point cloud with color information as a compressed NumPy .npz file
    #output_file = os.path.join(output_folder, 'pframes', '_' + get_file_name(dph_file) + '_with_color.npz')
    #point_cloud = np.column_stack((x, y, scaled_z, r_vals, g_vals, b_vals, z))
    #np.savez_compressed(output_file, point_cloud=point_cloud)
    #print("Point cloud with color saved as " + output_file)
    
# Function to process all DPH files in the input folder and create colored point clouds
def process_dph_files(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    dph_files = [file for file in os.listdir(input_folder) if file.endswith(".dph")]

    for dph_file in dph_files:
        create_colored_point_cloud(os.path.join(input_folder, dph_file), output_folder)

# Main function
if __name__ == "__main__":
    input_folder = "."  # Replace with the path to the folder containing the DPH files
    output_folder = "."  # Replace with the desired output folder

    process_dph_files(input_folder, output_folder)

    input("*******************\nPress enter to exit\n*******************")
