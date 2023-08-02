# Code by: GPT-CHAT
# Prompting: X3msnake
# https://chat.openai.com/share/99b0cea6-53be-43c0-bf8d-7741d92a5db2
# https://chat.openai.com/share/406c317a-766f-46a2-89b4-5df2a5cee4ab

import tkinter as tk
from tkinter import filedialog
import json

# Define a global variable to store the loaded JSON data
data = []
file_path = ""

def open_json_file():
    global data, file_path
    file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
    if file_path:
        with open(file_path, "r") as json_file:
            data = json.load(json_file)
            models = [item["model"] for item in data]
            populate_dropdown(models)
            # Automatically select and show parameters for the first model
            if models:
                dropdown.set(models[0])
                show_selected_params()

def populate_dropdown(models):
    dropdown.set("")  # Clear the current value
    dropdown_menu["menu"].delete(0, "end")  # Clear the current menu options
    for model in models:
        dropdown_menu["menu"].add_command(label=model, command=lambda model=model: dropdown.set(model))

def show_selected_params(*args):
    selected_model = dropdown.get()
    if selected_model:
        for item in data:
            if item["model"] == selected_model:
                model_params = json.dumps(item, indent=4)
                text_box.delete("1.0", "end")
                text_box.insert("1.0", model_params)
                break

def save_changes():
    global data, file_path
    selected_model = dropdown.get()
    if selected_model:
        updated_params = text_box.get("1.0", "end-1c")  # Get the text content (excluding the newline character)
        try:
            updated_data = json.loads(updated_params)
            for item in data:
                if item["model"] == selected_model:
                    item.update(updated_data)  # Update the model's parameters with the edited data
                    break
            with open(file_path, "w") as json_file:  # Write changes to the originally opened file
                json.dump(data, json_file, indent=4)
            print("Changes saved successfully.")
        except json.JSONDecodeError as e:
            print("Invalid JSON format. Changes not saved.")
            print(str(e))

            # Reload JSON data and refresh dropdown list
            open_json_file()

# Create the main window
root = tk.Tk()
root.title("JSON File Parser")

# Create a button to open the JSON file
open_button = tk.Button(root, text="Open JSON File", command=open_json_file)
open_button.pack(fill=tk.BOTH, padx=10, pady=10)

# Create the dropdown list
dropdown = tk.StringVar(root)
dropdown_label = tk.Label(root, text="Models:")
dropdown_label.pack(fill=tk.BOTH, padx=10)
dropdown_menu = tk.OptionMenu(root, dropdown, "")
dropdown_menu.pack(fill=tk.BOTH, padx=10)

# Create a Text widget to display selected model parameters
text_box = tk.Text(root, wrap="word")
text_box.pack(fill=tk.BOTH, padx=10, pady=10)

# Create a "Save" button to save changes
save_button = tk.Button(root, text="Save Changes", command=save_changes)
save_button.pack(fill=tk.BOTH, padx=10, pady=10)

# Bind the show_selected_params function to the dropdown's value change
dropdown.trace("w", show_selected_params)

# Start the main loop
root.mainloop()
