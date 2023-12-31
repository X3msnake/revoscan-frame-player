import os
import cv2
import tkinter as tk
from tkinter import filedialog
from typing import List

class ProgressBar:
    def __init__(self, total_frames: int, progress_bar_width: int):
        self.total_frames = total_frames
        self.progress_bar_width = progress_bar_width
        self.current_frame = 0

    def update(self):
        self.current_frame += 1
        progress = int((self.current_frame / self.total_frames) * self.progress_bar_width)
        progress_bar = '[' + '#' * progress + ' ' * (self.progress_bar_width - progress) + ']'
        print(f'\r\tExporting Frames: {progress_bar} {self.current_frame}/{self.total_frames}', end='')


def display_instructions():
    print("\n\t ..................................................................... ")
    print("\n\t Welcome to Revoscan frame player, to navigate use the following keys: ")
    print("\n\t ESC: quit")
    print("\n\t x: mark frame for deletion")
    print("\n\t Shift+E: export as video")
    print("\n\t Shift+X: export as RGB jpg sequence")
    print("\n\t Shift+O: open new cache folder")
    print("\n\t Space or Numpad 5: play/stop")
    print("\n\t Numpad 4/6: back / forward 1 frame")
    print("\n\t Numpad 7/9: back / forward 10 frame")
    print("\n\t..................................................................... \n")


def select_folder_dialog(title: str) -> str:
    root = tk.Tk()
    root.withdraw()
    return filedialog.askdirectory(title=title)


def get_image_files(folder_path: str) -> List[str]:
    return sorted([file for file in os.listdir(folder_path) if file.endswith('.img')])


def export_frames_to_folder(image_files: List[str], folder_path: str):
    export_folder = filedialog.askdirectory(title="Select export folder")
    if not export_folder:
        print('Export folder does not exist')
        input("Press Enter to exit...")

    progress_bar = ProgressBar(len(image_files), 50)

    for img_file in image_files:
        image_path = os.path.join(folder_path, img_file)
        frame = cv2.imread(image_path)

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        file_name, _ = os.path.splitext(img_file)
        output_path = os.path.join(export_folder, f'{file_name}.jpg')
        cv2.imwrite(output_path, frame_rgb)

        progress_bar.update()

    print("\n\tFrames exported successfully.")


def draw_filename(frame_rgb, filename, x_pressed):
    font = cv2.FONT_HERSHEY_SIMPLEX
    position = (10, 30)
    font_scale = 1
    font_color = (255, 255, 255)
    thickness = 2
    cv2.putText(frame_rgb, filename, position, font, font_scale, font_color, thickness, cv2.LINE_AA)

    if x_pressed:
        frame_height, frame_width = frame_rgb.shape[:2]
        line_color = (0, 0, 255)  # Red color
        line_thickness = 2

        cv2.line(frame_rgb, (0, 0), (frame_width, frame_height), line_color, line_thickness)
        cv2.line(frame_rgb, (frame_width, 0), (0, frame_height), line_color, line_thickness)


def load_x_files(image_files, folder_path):
    x_pressed = [False] * len(image_files)
    x_files_path = os.path.join(folder_path, 'x.files')

    if os.path.exists(x_files_path):
        with open(x_files_path, 'r') as x_files:
            for line in x_files:
                filename = line.strip()
                index = image_files.index(filename + '.img')
                if 0 <= index < len(x_pressed):
                    x_pressed[index] = True

    return x_pressed


def play_image_sequence():
    os.system('cls' if os.name == 'nt' else 'clear')

    display_instructions()

    folder_path = select_folder_dialog("Select revostudio scan cache folder!")

    image_files = get_image_files(folder_path)

    if not image_files:
        print('\t\t No image files found in the folder.')
        input("\t\t Press Enter to try again...")
        play_image_sequence()

    window_name = 'Revoscan FramePlay'
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, 1280, 800)

    current_frame = 0
    is_playing = False

    def on_trackbar(pos):
        nonlocal current_frame
        current_frame = pos

    timeline_name = 'Timeline'
    cv2.createTrackbar(timeline_name, window_name, 0, len(image_files) - 1, on_trackbar)

    output_file, output_width, output_height, fps = None, None, None, 24.0

    x_pressed = load_x_files(image_files, folder_path)

    while cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) >= 1:
        image_path = os.path.join(folder_path, image_files[current_frame])
        frame = cv2.imread(image_path)

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        draw_filename(frame_rgb, image_files[current_frame], x_pressed[current_frame])

        cv2.imshow(window_name, frame_rgb)
        cv2.setTrackbarPos(timeline_name, window_name, current_frame)

        key = cv2.waitKey(1)

        if key == ord('x'):
            x_pressed[current_frame] = not x_pressed[current_frame]

            with open(os.path.join(folder_path, 'x.files'), 'w') as x_files:
                for filename, x_status in zip(image_files, x_pressed):
                    if x_status:
                        x_files.write(filename[:-4] + '\n')

        if key == ord(' ') or key == ord('5'):
            is_playing = not is_playing

        if key == ord('O'):
            cv2.destroyAllWindows()
            play_image_sequence()

        if key == ord('4') and current_frame > 0:
            current_frame -= 1

        elif key == ord('6') and current_frame < len(image_files) - 1:
            current_frame += 1

        if key == ord('7') and current_frame > 0:
            current_frame -= 10

        elif key == ord('9') and current_frame < len(image_files) - 1:
            current_frame += 10

        if key == ord('X'):
            export_frames_to_folder(image_files, folder_path)

        if key == ord('E'):
            output_file = filedialog.asksaveasfilename(
                initialdir="./",
                title="Save Video",
                filetypes=(("MP4 files", "*.mp4"), ("All files", "*.*"))
            )

            if output_file:
                _, file_extension = os.path.splitext(output_file)
                if not file_extension:
                    output_file += ".mp4"

                output_width, output_height = frame_rgb.shape[1], frame_rgb.shape[0]
                fourcc = cv2.VideoWriter_fourcc(*"mp4v")
                output_video = cv2.VideoWriter(output_file, fourcc, fps, (output_width, output_height))

                total_frames = len(image_files)
                progress_bar_width = 50
                progress_bar = ProgressBar(total_frames, progress_bar_width)

                for img_file in image_files:
                    image_path = os.path.join(folder_path, img_file)
                    frame = cv2.imread(image_path)

                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    progress_bar.update()
                    output_video.write(frame_rgb)

                output_video.release()
                print(f"\n\tVideo saved as {output_file}")

        if key == 27:
            break

        if is_playing and current_frame < len(image_files) - 1:
            current_frame += 1

    cv2.destroyAllWindows()


# Run code
try:
    play_image_sequence()

except Exception as e:
    print(f"An error occurred: {e}")
    input("Press Enter to exit...")
