import os
import cv2
import sys
import tkinter as tk
from tkinter import filedialog
import numpy as np


class ProgressBar:
    def __init__(self, total_frames, progress_bar_width):
        self.total_frames = total_frames
        self.progress_bar_width = progress_bar_width
        self.current_frame = 0

    def update(self):
        self.current_frame += 1
        progress = int((self.current_frame / self.total_frames) * self.progress_bar_width)
        progress_bar = '[' + '#' * progress + ' ' * (self.progress_bar_width - progress) + ']'
        print(f'\r\tExporting Frames: {progress_bar} {self.current_frame}/{self.total_frames}', end='')

def play_image_sequence():
    
    # Clear the console
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("\n\t ..................................................................... ")
    print("\n\t Welcome to Revoscan frame player, to navigate use the following keys: ")
    print("")
    print("\n\t ESC: quit")
    print("\n\t x: mark frame for deletion")
    print("")
    print("\n\t Shift+E: export as video")
    print("\n\t Shift+X: export as RGB jpg sequence")
    print("\n\t Shift+O: open new cache folder")
    print("")
    print("\n\t Space or Numpad 5: play/stop")
    print("\n\t Numpad 4/6: back / forward 1 frame")
    print("\n\t Numpad 7/9: back / forward 10 frame")
    print("\n\t..................................................................... \n")
    
    # Prompt the user to select a folder
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory(title="Select revostudio scan cache folder!")

    # Get all JPG files in the selected folder
    image_files = sorted([file for file in os.listdir(folder_path) if file.endswith('.img')])

    if not image_files:
        print('\t\t No image files found in the folder.')
        input("\t\t Press Enter to try again...")
        play_image_sequence()
        


    # Create an OpenCV window
    window_name = 'Revoscan FramePlay'
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, 1280, 800) # Original BGR is 1280x800

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
    fps = 24.0

    def export_frames_to_folder(folder_path):
        export_folder = filedialog.askdirectory(title="Select export folder")
        if not export_folder:
            print('Export folder does not exist')
            input("Press Enter to exit...")

        progress_bar = ProgressBar(len(image_files), 50)

        for i, img_file in enumerate(image_files):
            image_path = os.path.join(folder_path, img_file)
            frame = cv2.imread(image_path)

            # Convert BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Export frame as JPEG
            file_name, file_extension = os.path.splitext(img_file)
            output_path = os.path.join(export_folder, f'{file_name}.jpg')
            cv2.imwrite(output_path, frame_rgb)

            progress_bar.update()

        print("\n\tFrames exported successfully.")
        
    def draw_filename(frame, filename, x_pressed):
        font = cv2.FONT_HERSHEY_SIMPLEX
        position = (10, 30)
        font_scale = 1
        font_color = (255, 255, 255)
        thickness = 2
        cv2.putText(frame, filename, position, font, font_scale, font_color, thickness, cv2.LINE_AA)

        if x_pressed:
            frame_height, frame_width = frame.shape[:2]
            line_color = (0, 0, 255)  # Red color
            line_thickness = 2

            # Draw the first diagonal line of the X
            cv2.line(frame, (0, 0), (frame_width, frame_height), line_color, line_thickness)

            # Draw the second diagonal line of the X
            cv2.line(frame, (frame_width, 0), (0, frame_height), line_color, line_thickness)
        
    x_pressed = [False] * len(image_files)
    
    # Load the x.files if it exists
    x_files_path = os.path.join(folder_path, 'x.files')
    if os.path.exists(x_files_path):
        with open(x_files_path, 'r') as x_files:
            for line in x_files:
                filename = line.strip()
                index = image_files.index(filename + '.img')  # Convert filename to full filename with extension
                if 0 <= index < len(x_pressed):
                    x_pressed[index] = True


    while cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) >= 1:
        # Load the current frame
        image_path = os.path.join(folder_path, image_files[current_frame])
        frame = cv2.imread(image_path)

        # Convert BGR to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Draw the filename and X overlay on the frame
        draw_filename(frame_rgb, image_files[current_frame], x_pressed[current_frame])

        # Display the current frame
        cv2.imshow(window_name, frame_rgb)

        # Update the trackbar position
        cv2.setTrackbarPos(timeline_name, window_name, current_frame)

        # Wait for user input
        key = cv2.waitKey(1)
        
        # Check if 'x' is pressed
        if key == ord('x'):
            x_pressed[current_frame] = not x_pressed[current_frame]

            # Update x.files
            with open(x_files_path, 'w') as x_files:
                for filename, x_status in zip(image_files, x_pressed):
                    if x_status:
                        x_files.write(filename[:-4] + '\n')  # Remove .img extension and write filename

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

        # Export frames to a folder if Shift+X is pressed
        if key == ord('X'):
            export_frames_to_folder(folder_path)

        # Export to video if Shift+E is pressed
        if key == ord('E'):
            output_file = filedialog.asksaveasfilename(
                initialdir="./",
                title="Save Video",
                filetypes=(("MP4 files", "*.mp4"), ("All files", "*.*"))
            )

            if output_file:
                # Check if the output file has an extension
                _, file_extension = os.path.splitext(output_file)
                if not file_extension:
                    # Append a default extension, such as ".mp4"
                    output_file += ".mp4"

                output_width, output_height = frame.shape[1], frame.shape[0]
                fourcc = cv2.VideoWriter_fourcc(*"mp4v")
                output_video = cv2.VideoWriter(output_file, fourcc, fps, (output_width, output_height))

                # Export frames to video
                total_frames = len(image_files)
                progress_bar_width = 50
                progress_bar = ProgressBar(total_frames, progress_bar_width)

                for i, img_file in enumerate(image_files):
                    image_path = os.path.join(folder_path, img_file)
                    frame = cv2.imread(image_path)

                    # Convert BGR to RGB
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                    # Display progress
                    progress_bar.update()

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
    
#Run code
try:
    play_image_sequence()
    
except Exception as e:
    print(f"An error occurred: {e}")
    input("Press Enter to exit...")
