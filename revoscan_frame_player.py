# If you are running this code from the command line don't forget to install the following libraries:
# pip install opencv-python numpy

import os
import cv2
import tkinter as tk
from tkinter import filedialog
import numpy as np


print("\n\t ..................................................................... ")
print("\n\t Welcome to Revoscan frame player, to navigate use the following keys: ")
print("\n\t ESC: quit")
print("\n\t Shift+E: export")
print("\n\t Shift+O: open new cache folder")
print("\n\t Space or Numpad 5: play/stop")
print("\n\t Numpad 4/6: back / forward 1 frame")
print("\n\t Numpad 7/9: back / forward 10 frame")
print("\n\t..................................................................... \n")

def play_image_sequence():
    # Prompt the user to select a folder
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory(title="Select revostudio scan cache folder!")

    # Get all JPG files in the selected folder
    image_files = sorted([file for file in os.listdir(folder_path) if file.endswith('.img')])

    if not image_files:
        print('No image files found in the folder.')
        return

    # Create an OpenCV window
    window_name = 'Revoscan FramePlay'
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, 800, 600)

    current_frame = 0
    is_playing = False

    def on_trackbar(pos):
        nonlocal current_frame
        current_frame = pos

    # Create a trackbar timeline
    timeline_name = 'Timeline'
    cv2.createTrackbar(timeline_name, window_name, 0, len(image_files) - 1, on_trackbar)

    # Initialize video writer
    output_file = None
    output_width, output_height = None, None
    fps = 30.0

    while cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) >= 1:
        # Load the current frame
        image_path = os.path.join(folder_path, image_files[current_frame])
        frame = cv2.imread(image_path)

        # Convert BGR to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Display the current frame
        cv2.imshow(window_name, frame_rgb)

        # Update the trackbar position
        cv2.setTrackbarPos(timeline_name, window_name, current_frame)

        # Wait for user input
        key = cv2.waitKey(1)

        # Play/Pause controls
        if key == ord(' ') or key == ord('5'):
            is_playing = not is_playing
        
        if key == ord('O'):
            cv2.destroyAllWindows()
            play_image_sequence()
            
        # Scrub controls
        # Right cursor key with numpad active
        if key == ord('4') and current_frame > 0:
            current_frame -= 1
        
        # Left cursor key with numpad active
        elif key == ord('6') and current_frame < len(image_files) - 1:
            current_frame += 1
        
        # +-10 frames
        if key == ord('7') and current_frame > 0:
            current_frame -= 10
        
        # Left cursor key with numpad active
        elif key == ord('9') and current_frame < len(image_files) - 1:
            current_frame += 10

        # Export to video if Shift+E is pressed
        if key == ord('E'):
            output_file = filedialog.asksaveasfilename(
                initialdir="./",
                title="Save Video",
                filetypes=(("MP4 files", "*.mp4"), ("All files", "*.*"))
            )

            if output_file:
                output_width, output_height = frame.shape[1], frame.shape[0]
                fourcc = cv2.VideoWriter_fourcc(*"mp4v")
                output_video = cv2.VideoWriter(output_file, fourcc, fps, (output_width, output_height))

                # Export frames to video
                total_frames = len(image_files)
                progress_bar_width = 50

                for i, img_file in enumerate(image_files):
                    image_path = os.path.join(folder_path, img_file)
                    frame = cv2.imread(image_path)

                    # Convert BGR to RGB
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                    # Display progress
                    progress = int((i + 1) / total_frames * progress_bar_width)
                    progress_bar = '[' + '#' * progress + ' ' * (progress_bar_width - progress) + ']'
                    print(f'\r\tExporting Frames: {progress_bar} {i + 1}/{total_frames}', end='')

                    output_video.write(frame_rgb)

                output_video.release()
                print(f"\n\tVideo saved as {output_file}")

        # Exit the loop if ESC key is pressed
        if key == 27:
            break

        # Increment the frame if playing
        if is_playing and current_frame < len(image_files) - 1:
            current_frame += 1

    # Close the OpenCV window
    cv2.destroyAllWindows()

# Example usage
play_image_sequence()
