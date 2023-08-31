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
print("\n\t     r: rotates the stream                                                      ")
print("\n\t                                                                                ")
print("\n\t - This script loops trough the dph files in the same folder as this py.        ")
print("\n\t - Video is being saved while you see it run and is output to dph_output.mp4    ")
print("\n\t - The file will be in the same folder as this script                         \n")
print("\n\t..............................................................................\n")

# Define width and height for the output video frames
img = np.fromfile(dph_files[0], dtype=np.uint16)
img_size = img.size

target_sizes = {
    64000: (320, 200),
    256000: (640, 400)
}

if img_size in target_sizes:
    width, height = target_sizes[img_size]
else:
    # Calculate width and height based on the image size
    # You can adjust this calculation according to your requirements
    ratio = img_size / 64000  # Adjust the divisor as needed
    width = int(320 * ratio)   # Adjust the base width as needed
    height = int(200 * ratio)  # Adjust the base height as needed

print(f" \t   Raw depth capture: {width}x{height}")

# Create a VideoWriter object to save the output video
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
output_video = cv2.VideoWriter('dph_output.mp4', fourcc, 10, (width, height))

# Initialize a rotation flag
rotate_flag = False

# Loop to play the "movie" indefinitely
while True:
    for dphfilepath in dph_files:
        # Read the raw file
        with open(dphfilepath, 'rb') as f:
            raw_image = np.fromfile(f, dtype=np.uint16)

        # Reshape the raw image array to the specified width and height
        raw_image = raw_image.reshape(height, width)

        # Normalize the raw image to the range [0, 65535]
        normalized_image = (raw_image / np.max(raw_image) * (65535/256)).astype(np.uint16)

        # Split the normalized grayscale values into red and green channels
        red_channel = (normalized_image / 2).astype(np.uint8)  # Divide by 2 for red channel
        green_channel = (normalized_image).astype(np.uint8)  # Green channel as complement

        # Flip the green channel values
        green_channel = 255 - green_channel
        green_channel[green_channel == 255] = 0  # Replace 255 with 0

        # Normalize the normalized_image array to the range [0, 255]
        normalized_image_8bit = (normalized_image / np.max(normalized_image) * 255).astype(np.uint8)

        # Apply histogram equalization to the normalized image for the blue channel
        equalized_blue = cv2.equalizeHist(normalized_image_8bit)

        # Convert the equalized blue channel back to the range [0, 65535]
        blue_channel = (equalized_blue * 255).astype(np.uint8)
        flipped_blue_channel = 255 - blue_channel
        
        # Create an empty RGB image
        rgb_image = np.zeros((height, width, 3), dtype=np.uint8)

        # Assign red, green, and blue channels to the RGB image
        rgb_image[:,:,0] = red_channel
        rgb_image[:,:,1] = green_channel
        rgb_image[:,:,2] = blue_channel

        # Show separate grayscale windows for each channel
        #cv2.imshow('Red Channel', red_channel)
        #cv2.imshow('Green Channel', green_channel)
        #cv2.imshow('Blue Channel', equalized_blue)
        
        if rotate_flag:
            rotated_image = cv2.rotate(rgb_image, cv2.ROTATE_90_CLOCKWISE)
            cv2.imshow('RGB Image', rotated_image)
        else:
            cv2.imshow('RGB Image', rgb_image)
        
        # Write the current frame to the output video
        output_video.write(rgb_image)

        # Wait for a short duration (e.g., 100 milliseconds)
        key = cv2.waitKey(100)

        # Exit the loop if ESC key is pressed
        if key == 27:
            break
        
        # Rotate the image if the 'r' key is pressed
        if key == ord('r'):
            rotate_flag = not rotate_flag  # Toggle the rotation flag

    # Exit the loop if ESC key is pressed
    if key == 27:
        break

# Release the VideoWriter and close OpenCV windows
output_video.release()
cv2.destroyAllWindows()
