import os
import time
import numpy as np
import polyscope as ps
import polyscope.imgui as psim

def next_frame():
    # ... do something important here ...
    print("executing function")
    pc_path = '_frame_000_0350_with_color.txt'
    point_cloud = np.loadtxt(pc_path, delimiter=' ')
    # Separate the point array into point positions and colors. The colors need to be between 0-1, so we cast the ints to floats and divide by 255
    points = point_cloud[:,:3]
    colors = point_cloud[:,3:6].astype(np.float32)/255
    ps_cloud = ps.register_point_cloud("frame", points)
    ps_cloud.set_radius(0.0005, relative=True)
    ps_cloud.add_color_quantity("frame colors", colors)
    
def prev_frame():
    # ... do something important here ...
    print("executing function")
    pc_path = '_frame_000_0332_with_color.txt'
    point_cloud = np.loadtxt(pc_path, delimiter=' ')
    # Separate the point array into point positions and colors. The colors need to be between 0-1, so we cast the ints to floats and divide by 255
    points = point_cloud[:,:3]
    colors = point_cloud[:,3:6].astype(np.float32)/255
    ps_cloud = ps.register_point_cloud("frame", points)
    ps_cloud.set_radius(0.0005, relative=True)
    ps_cloud.add_color_quantity("frame colors", colors)

# Callback function called every update iteration.  The same functions can be used for GUI functionality and interactivity
def callback():
    
    if(psim.Button("Prev Frame")):
        # This code is executed when the button is pressed
        prev_frame()
        
    if(psim.Button("Next Frame")):
        # This code is executed when the button is pressed
        next_frame()
        
    # # Get the delta time
    # delta_change = time.time()

    # # Calculate the center of the point cloud
    # center = np.nanmean(points, axis=0)
    # #print(center)
    
    # # Create a 4x4 matrix for the frame statue rotation
    # matrix = np.eye(4)

    # # Create a rotation in Y direction using the delta_change
    # rotation = np.array([[np.cos(delta_change), 0, np.sin(delta_change)],
                         # [0, 1, 0],
                         # [-np.sin(delta_change), 0, np.cos(delta_change)]])

    # # Translate the point cloud so that its center is at the origin (pivot point)
    # translated_points = points - center

    # # Multiply the rotation with the translated points of the point cloud
    # new_points = np.dot(translated_points, rotation.T)

    # # Translate the point cloud back to its original position
    # new_points += center

    # # Update the point positions in the renderer
    # ps_cloud.update_point_positions(new_points)

    # # Compute the X and Z position of the sphere point
    # xpos = np.sin(-delta_change * 2)
    # zpos = np.cos(-delta_change * 2)

    # # Update the point position with the new X, Y, and Z positions (rotational center)
    # ps_sphere.update_point_positions(np.array([[center[0] + xpos, center[1], center[2] + zpos]]))


# Load the frame point cloud
#pc_path = os.path.join('point_cloud','_frame_000_0332_with_color.txt')
pc_path = '_frame_000_0332_with_color.txt'
point_cloud = np.loadtxt(pc_path, delimiter=' ')

#print (point_cloud[:,:3])
#print (point_cloud[:,3:6])

# Separate the point array into point positions and colors. The colors need to be between 0-1, so we cast the ints to floats and divide by 255
points = point_cloud[:,:3]
colors = point_cloud[:,3:6].astype(np.float32)/255
#colors = point_cloud[:,3:6]

# Initialize the polyscope environment. Calling this is required before the show method can be invoked
#print("Initialize the polyscope environment.")
ps.init()

# Initialize a polyscope point cloud with a specific name, point positions and material. We need a material that supports blending so the colors can be visualized - 'clay', 'wax', 'candy', 'flat'
#print("Initialize a polyscope point cloud with a specific name")
ps_cloud = ps.register_point_cloud("frame", points, enabled=True, material = 'clay')
ps_cloud.set_radius(0.0005, relative=True)


# Add the color information to the point cloud and enable it
#print("Add the color information to the point cloud and enable it.")
ps_cloud.add_color_quantity("frame colors", colors, enabled = True)

# create a point cloud of one point for the 'sphere' that rotates around the frame
#print(" create a point cloud of one point for the 'sphere' that rotates around the frame")
point = np.array([[0,0,0]])

# Initialize the "sphere" point and render it as a sphere. We give it an interesting material that does not need to be blended
#print("Initialize the sphere point and render it as a sphere.")
ps_sphere = ps.register_point_cloud("point", point, point_render_mode='sphere', enabled=False, material='clay')

# Set the radius of the sphere
#print("Set the radius of the sphere")
#ps_sphere.set_radius(10, relative=False)

# Set the callback function for the animation
ps.set_user_callback(callback)

# Configure Scene
ps.set_ground_plane_mode("shadow_only")

# Show the scene
ps.show()