import sys
import os
import cv2
import shutil

# Set the working directory to the script's folder
script_folder = os.path.dirname(sys.argv[0])
os.chdir(script_folder)
# print (script_folder)

class NoJPGFilesError(Exception):
    pass

class ProgressBar:
    def __init__(self, total_frames, progress_bar_width):
        self.total_frames = total_frames
        self.progress_bar_width = progress_bar_width
        self.current_frame = 0

    def update(self):
        self.current_frame += 1
        progress = int((self.current_frame / self.total_frames) * self.progress_bar_width)
        progress_bar = '[' + '#' * progress + ' ' * (self.progress_bar_width - progress) + ']'
        print(f'\r\tConverting Frames: {progress_bar} {self.current_frame}/{self.total_frames}', end='')

def convert_jpg_to_img():
    try:
        # Get the script's root folder
        script_folder = os.path.dirname(sys.argv[0])
        print ("\n\tCurrent JPG folder: " + script_folder + "\n")

        # Specify the input folder (folder containing JPG files)
        input_folder = script_folder

        # Specify the output folder (where IMG files will be saved)
        output_folder = os.path.join(script_folder, "output_imgs")

        # Ensure output folder exists
        os.makedirs(output_folder, exist_ok=True)

        # Get all JPG files in the input folder
        jpg_files = sorted([file for file in os.listdir(input_folder) if file.endswith('.jpg')])

        if not jpg_files:
            raise NoJPGFilesError('No JPG files found in the folder.')

        # Initialize progress bar
        progress_bar = ProgressBar(len(jpg_files), 50)

        for i, jpg_file in enumerate(jpg_files):
            # Read JPG image
            jpg_path = os.path.join(input_folder, jpg_file)
            img = cv2.imread(jpg_path)

            # Convert RGB to BGR
            img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

            # Write to IMG file
            img_output_path = os.path.join(output_folder, f'{os.path.splitext(jpg_file)[0]}.jpg')
            cv2.imwrite(img_output_path, img_bgr)

            # Rename file to have .img extension
            img_new_output_path = os.path.join(output_folder, f'{os.path.splitext(jpg_file)[0]}.img')
            shutil.move(img_output_path, img_new_output_path)

            # Update progress bar
            progress_bar.update()

        print("\n\tConversion from JPG to IMG completed successfully.")
    except NoJPGFilesError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

    input("\nPress Enter to continue...")

# Example usage
if __name__ == "__main__":
    convert_jpg_to_img()
