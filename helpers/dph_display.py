dphfilepath = "frame_000_0338.dph"

# Image byte size checker
import numpy as np
import matplotlib.pyplot as plt

img = np.fromfile(dphfilepath, dtype=np.uint16)
print (img.size) #check your image size, say 1048576
#shape it accordingly, that is, 1048576=1024*1024


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

# Get the Jet colormap
# https://docs.opencv.org/4.x/d3/d50/group__imgproc__colormap.html
jet_colormap = cv2.applyColorMap(np.arange(256, dtype=np.uint8), cv2.COLORMAP_SUMMER)

# Reverse the colormap array
flipped_jet_colormap = jet_colormap[::-1]
#flipped_jet_colormap = jet_colormap

# Apply the flipped Jet colormap to the equalized image
colormap_image = cv2.applyColorMap(equalized_image, flipped_jet_colormap)

# Create a window and display the image
cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
cv2.imshow('Image', colormap_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
