import os
import tkinter as tk
from tkinter import ttk, filedialog

def filter_files(files):
    # Keep only one file per extension
    unique_extensions = set()
    filtered_files = []

    for file in files:
        _, extension = os.path.splitext(file)
        extension = extension.lower()

        if extension not in unique_extensions:
            unique_extensions.add(extension)
            filtered_files.append(file)

    return filtered_files

def populate_treeview(parent, folder, filter_files_enabled):
    files = []
    folders = []

    for item in os.listdir(folder):
        item_path = os.path.join(folder, item)
        if os.path.isdir(item_path):
            folders.append(item)
        else:
            files.append(item)

    # Apply file filtering if enabled
    if filter_files_enabled and len(files) > 10:
        files = filter_files(files)

    # Insert files first
    for item in sorted(files):
        tree.insert(parent, 'end', text=item)

    # Then insert subfolders
    for item in sorted(folders):
        child = tree.insert(parent, 'end', text=item, open=False)
        populate_treeview(child, os.path.join(folder, item), filter_files_enabled)

def select_folder():
    folder_path = filedialog.askdirectory(title="Select Main Folder")
    if folder_path:
        tree.delete(*tree.get_children())
        filter_files_enabled = filter_checkbox_var.get()
        populate_treeview('', folder_path, filter_files_enabled)

# Create main window
root = tk.Tk()
root.title("TreeView Browser")

# Create Treeview
tree = ttk.Treeview(root)
tree.heading('#0', text='Folder Structure', anchor='w')

# Create Scrollbar
tree_scrollbar = ttk.Scrollbar(root, orient='vertical', command=tree.yview)
tree.configure(yscrollcommand=tree_scrollbar.set)

# Pack Treeview and Scrollbar
tree.pack(side='left', fill='both', expand=True)
tree_scrollbar.pack(side='right', fill='y')

# Create "Select Folder" button
select_folder_button = ttk.Button(root, text="Select Main Folder", command=select_folder)
select_folder_button.pack(pady=10)

# Create Filter Checkbox
filter_checkbox_var = tk.BooleanVar()
filter_checkbox = ttk.Checkbutton(root, text="Filter Files", variable=filter_checkbox_var)
filter_checkbox.pack()

# Run the Tkinter event loop
root.mainloop()
