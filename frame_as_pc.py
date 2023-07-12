import numpy as np
import matplotlib.pyplot as plt

# Read the raw file
with open('frame_000_0338.dph', 'rb') as f:
    raw_image = np.fromfile(f, dtype=np.uint16)

# Set the width and height of the image
width = 640
height = 400

# Reshape the raw image array to the specified width and height
raw_image = raw_image.reshape(height, width)

# Define downsampling factor
downsample_factor = 1

# Downsample the image and coordinates
downsampled_image = raw_image[::downsample_factor, ::downsample_factor]
downsampled_x_coords = np.arange(0, width, downsample_factor)
downsampled_y_coords = np.arange(0, height, downsample_factor)

# Invert the intensity values
inverted_image = np.max(raw_image) - downsampled_image

# Create x and y coordinates for the downsampled point cloud
x_coords, y_coords = np.meshgrid(downsampled_x_coords, downsampled_y_coords)

# Flatten the x and y coordinates and the downsampled image values
x = x_coords.flatten()
y = y_coords.flatten()
z = inverted_image.flatten()

# Set the dot size
dot_size = .1

# Set the scaling factor for the Z-axis
z_scale = 0.30

# Scale the Z-axis values
scaled_z = z * z_scale

# Plot the inverted point cloud with scaled Z-axis
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x, y, scaled_z, c=z, cmap='jet', s=dot_size)

# Set labels and title
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Intensity (Scaled)')
ax.set_title('Inverted DPH Point Cloud with Scaled Z-axis')

# Save the point cloud as an ASCII file
output_file = 'point_cloud.txt'
point_cloud = np.column_stack((x, y, scaled_z, z))
np.savetxt(output_file, point_cloud, fmt='%.6f', delimiter=' ')
print("Pointcloud saved as point_cloud.txt")

# Display the plot
plt.show()
