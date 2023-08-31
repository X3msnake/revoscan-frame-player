import os
import numpy as np
import cv2

# Get a list of all DPH files in the current directory
dph_files = [file for file in os.listdir() if file.endswith(".dph")]

# Check for dph files
if not dph_files:
    print("\n\t No dph (depth map) files found in the current script directory.")
    print("\n\t Please paste and run this file from the revoscan cache folder you want to view")
    input("\n\t Press enter to exit;")
    exit()

print("\n\t................................................................................")
print("\n\t                                                                                ")
print("\n\t   ESC: exits the script                                                        ")
print("\n\t                                                                                ")
print("\n\t - This script loops trough the dph files in the same folder as this py.        ")
print("\n\t - Video is being saved while you see the it run and is output to dph_output.mp4")
print("\n\t - File will be in the same folder as this script                               ")
print("\n\t..............................................................................\n")


# Define width and height
width = 640
height = 400

# Create a VideoWriter object to save the output video
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
output_video = cv2.VideoWriter('dph_output.mp4', fourcc, 10, (width, height))

# Loop to play the "movie" indefinitely
while True:
    for dphfilepath in dph_files:
        # Read the raw file
        with open(dphfilepath, 'rb') as f:
            raw_image = np.fromfile(f, dtype=np.uint16)

        # Reshape the raw image array to the specified width and height
        raw_image = raw_image.reshape(height, width)

        # Normalize the raw image to the range [0, 65535]
        normalized_image = (raw_image / np.max(raw_image)) * 65535

        # Convert the normalized image to 8-bit uint
        uint8_image = np.uint8(normalized_image)

        # Create a custom colormap (Rainbow)
        custom_colormap = cv2.applyColorMap(np.arange(256, dtype=np.uint8), cv2.COLORMAP_TWILIGHT)

        # Apply the custom colormap to the image
        colormap_image = cv2.applyColorMap(uint8_image, custom_colormap)

        # Display the colored image
        cv2.namedWindow('Custom Colormap Image', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Custom Colormap Image', width, height)
        cv2.imshow('Custom Colormap Image', colormap_image)

        # Write the current frame to the output video
        output_video.write(colormap_image)

        # Wait for a short duration (e.g., 100 milliseconds)
        key = cv2.waitKey(100)

        # Exit the loop if ESC key is pressed
        if key == 27:
            break

    # Exit the loop if ESC key is pressed
    if key == 27:
        break

# Release the VideoWriter and close OpenCV windows
output_video.release()
cv2.destroyAllWindows()

