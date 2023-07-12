#################################################

 # Helper assumes the python code is in the same
 # cache folder as the dph you are trying to 
 # export/view, if your file is in another folder
 # you need to give the full path
 
 # Export will always be to the same folder 
 # where the python is being run from

dphfilepath = "frame_000_0000.dph"

#################################################

# Image byte size checker
# Check your image size and then shape it
# accordingly. Example: 1048576=1024*1024

import numpy as np
import matplotlib.pyplot as plt

img = np.fromfile(dphfilepath, dtype=np.uint16)
print (img.size) 


#################################################

# Revoscan DPH file decoder
import numpy as np
import cv2

width = 640
height = 400

# Read the raw file
with open(dphfilepath, 'rb') as f:
    raw_image = np.fromfile(f, dtype=np.uint16)

# Reshape the raw image array to the specified width and height
raw_image = raw_image.reshape(height, width)

# Perform histogram equalization
equalized_image = cv2.equalizeHist(np.uint8(raw_image / (np.max(raw_image) / 255.0)))

# Get the colormap, check the link for other available templates
# https://docs.opencv.org/4.x/d3/d50/group__imgproc__colormap.html
colormap = cv2.applyColorMap(np.arange(256, dtype=np.uint8), cv2.COLORMAP_SUMMER)

# Reverse the colormap array
flipped_colormap = colormap[::-1]
#flipped_colormap = colormap

# Apply the flipped Jet colormap to the equalized image
colormap_image = cv2.applyColorMap(equalized_image, flipped_colormap)

# Create a window and display the image
cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Image', width, height)
cv2.imshow('Image', colormap_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
