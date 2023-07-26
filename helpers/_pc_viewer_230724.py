import os
import time
import numpy as np
import polyscope as ps
import polyscope.imgui as psim

# Global variables to keep track of the current frame index, file list, ps_cloud, points, colors, and is_turntable_active
current_frame_idx = 0
file_list = []
ps_cloud = None
points = None
colors = None
is_turntable_active = False  # Initialize is_turntable_active
current_frame_filename = ""  # Initialize current_frame_filename

def load_file_list():
    global file_list
    # Get the list of files in the pframes folder ending with ".txt"
    file_list = [f for f in os.listdir('pframes') if f.endswith('.txt')]
    file_list.sort()

def load_frame(frame_idx):
    # Get the filename based on the index from the file list
    pc_path = os.path.join('pframes', file_list[frame_idx])
    
    # Load point cloud data from the file
    point_cloud = np.loadtxt(pc_path, delimiter=' ')
    global points, colors  # Set the global points and colors variables
    points = point_cloud[:, :3]
    colors = point_cloud[:, 3:6].astype(np.float32) / 255
    return points, colors

def show_frame(frame_idx):
    global ps_cloud, points, colors, current_frame_filename  # Use the global ps_cloud, points, colors, and current_frame_filename variables
    # Load and visualize the specified frame
    points, colors = load_frame(frame_idx)
    current_frame_filename = file_list[frame_idx]  # Set the current_frame_filename to the filename of the current frame
    if ps_cloud is None:
        # If ps_cloud is not registered, register it
        ps_cloud = ps.register_point_cloud("frame", points, enabled=True, material='clay')
        ps_cloud.set_radius(0.0005, relative=True)
        ps_cloud.add_color_quantity("frame colors", colors, enabled=True)
    else:
        # If ps_cloud is already registered, update the point positions and colors
        ps_cloud.update_point_positions(points)
        ps_cloud.add_color_quantity("frame colors", colors)

def next_frame():
    global current_frame_idx, points, colors  # Use the global points and colors variables
    # Increment the frame index and handle cycling if needed
    current_frame_idx += 1
    if current_frame_idx >= len(file_list):
        current_frame_idx = 0
    show_frame(current_frame_idx)

def prev_frame():
    global current_frame_idx, points, colors  # Use the global points and colors variables
    # Decrement the frame index and handle cycling if needed
    current_frame_idx -= 1
    if current_frame_idx < 0:
        current_frame_idx = len(file_list) - 1
    show_frame(current_frame_idx)

def toggle_turntable():
    global is_turntable_active  # Use the global is_turntable_active variable
    is_turntable_active = not is_turntable_active

def turntable_state_text():
    return "Active" if is_turntable_active else "Inactive"

def turntable_callback():
    global ps_cloud, points  # Use the global ps_cloud and points variables
    # The turntable rotation logic
    if is_turntable_active:
        # Get the delta time
        delta_change = time.time()

        # Calculate the center of the point cloud
        center = np.nanmean(points, axis=0)
        
        # Create a 4x4 matrix for the frame statue rotation
        matrix = np.eye(4)

        # Create a rotation in Y direction using the delta_change
        rotation = np.array([[np.cos(delta_change), 0, np.sin(delta_change)],
                             [0, 1, 0],
                             [-np.sin(delta_change), 0, np.cos(delta_change)]])

        # Translate the point cloud so that its center is at the origin (pivot point)
        translated_points = points - center

        # Multiply the rotation with the translated points of the point cloud
        new_points = np.dot(translated_points, rotation.T)

        # Translate the point cloud back to its original position
        new_points += center

        # Update the point positions in the renderer
        ps_cloud.update_point_positions(new_points)

        # Compute the X and Z position of the sphere point
        xpos = np.sin(-delta_change * 2)
        zpos = np.cos(-delta_change * 2)

        # Update the point position with the new X, Y, and Z positions (rotational center)
        ps_sphere.update_point_positions(np.array([[center[0] + xpos, center[1], center[2] + zpos]]))

def callback():
    # Button for navigating to the previous frame
    if psim.Button("Prev Frame"):
        prev_frame()

    # Button for navigating to the next frame
    if psim.Button("Next Frame"):
        next_frame()

    # Button for toggling the turntable rotation
    if psim.Button("Play"):
        toggle_turntable()

    # Display the turntable state
    psim.LabelText("", turntable_state_text())
    
    # Display the current frame filename
    psim.LabelText("--> Current Frame", current_frame_filename)
    
    if is_turntable_active:
        next_frame()

# Initialize the polyscope environment
ps.init()

# Load the file list
load_file_list()

# Load the initial frame (frame 0)
show_frame(current_frame_idx)

# Register the point cloud and sphere
ps_cloud = ps.register_point_cloud("frame", points, enabled=True, material='clay')
ps_cloud.set_radius(0.0005, relative=True)
ps_cloud.add_color_quantity("frame colors", colors, enabled=True)

# create a point cloud of one point for the 'sphere' that rotates around the frame
point = np.array([[0, 0, 0]])
ps_sphere = ps.register_point_cloud("point", point, point_render_mode='sphere', enabled=False, material='clay')

# Set the callback function for the animation
ps.set_user_callback(callback)

# Configure Scene
ps.set_ground_plane_mode("shadow_only")

# Show the scene
ps.show()
