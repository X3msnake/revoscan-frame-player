# filename: _frame_to_pc_2.230725.py

import os
import numpy as np
from PIL import Image, ImageChops
import argparse
import struct

def get_file_name(file_path):
    return os.path.splitext(os.path.basename(file_path))[0]

def create_colored_point_cloud(dph_file, output_folder, output_format):
    with open(dph_file, 'rb') as f:
        raw_image = np.fromfile(f, dtype=np.uint16)

    width, height = 640, 400
    raw_image = raw_image.reshape(height, width)
    downsample_factor = 1
    downsampled_image = raw_image[::downsample_factor, ::downsample_factor]
    downsampled_x_coords = np.arange(0, width, downsample_factor)
    downsampled_y_coords = np.arange(0, height, downsample_factor)
    x_coords, y_coords = np.meshgrid(downsampled_x_coords, downsampled_y_coords)
    x = x_coords.flatten()
    y = y_coords.flatten()
    z = downsampled_image.flatten()

    z_scale = 0.5
    scaled_z = z * z_scale
    x_offset = -80
    y_offset = 0

    img_file = get_file_name(dph_file) + '.img'
    if not os.path.exists(img_file):
        r_vals, g_vals, b_vals = 0, 210, 230
    else:
        color_image = Image.open(img_file)
        offset_color_image = ImageChops.offset(color_image, xoffset=x_offset, yoffset=y_offset)
        offset_color_image = offset_color_image.resize((640, 400))
        b, g, r = offset_color_image.split()
        r_vals = np.array(r).flatten()
        g_vals = np.array(g).flatten()
        b_vals = np.array(b).flatten()

    y = height - y
    x = width - x

    point_cloud = np.column_stack((x, y, scaled_z, r_vals, g_vals, b_vals, z))

    if output_format == 'txt':
        save_as_txt(point_cloud, output_folder, dph_file)
    elif output_format == 'npz':
        save_as_npz(point_cloud, output_folder, dph_file)
    elif output_format == 'ply':
        save_as_ply(point_cloud, output_folder, dph_file)

def save_as_txt(point_cloud, output_folder, dph_file):
    output_file = os.path.join(output_folder, 'pframes', '_' + get_file_name(dph_file) + '_with_color.txt')
    np.savetxt(output_file, point_cloud, fmt='%.6f', delimiter=' ')
    print("Point cloud with color saved as " + output_file)

def save_as_npz(point_cloud, output_folder, dph_file):
    output_file = os.path.join(output_folder, 'pframes', '_' + get_file_name(dph_file) + '_with_color.npz')
    np.savez_compressed(output_file, point_cloud=point_cloud)
    print("Point cloud with color saved as " + output_file)

def save_as_ply(point_cloud, output_folder, dph_file):
    header = """ply
format binary_little_endian 1.0
element vertex {}
property float x
property float y
property float z
property uchar red
property uchar green
property uchar blue
property float z_scale
end_header
"""

    vertex_count = len(point_cloud)
    output_file = os.path.join(output_folder, 'pframes', '_' + get_file_name(dph_file) + '_with_color.ply')
    with open(output_file, 'wb') as f:
        f.write(header.format(vertex_count).encode())

        for point in point_cloud:
            x, y, z, r, g, b, z_scale = point
            data = struct.pack('<fffBBBf', x, y, z, int(r), int(g), int(b), z_scale)
            f.write(data)
    
    print("Point cloud with color saved as " + output_file)

def process_dph_files(input_folder, output_folder, output_format):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    dph_files = [file for file in os.listdir(input_folder) if file.endswith(".dph")]

    for dph_file in dph_files:
        create_colored_point_cloud(os.path.join(input_folder, dph_file), output_folder, output_format)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create colored point clouds from DPH and IMG files.")
    parser.add_argument("input_folder", nargs="?", default=".", help="Input folder path containing DPH files.")
    parser.add_argument("output_folder", nargs="?", default=".", help="Output folder path to save point clouds.")
    parser.add_argument("--output_format", default="npz", choices=["txt", "npz", "ply"], help="Output format (txt, npz, ply). Default is ply.")
    args = parser.parse_args()

    process_dph_files(args.input_folder, args.output_folder, args.output_format)

    input("*******************\nPress enter to exit\n*******************")