import tkinter as tk
from tkinter import filedialog, scrolledtext, Button, Checkbutton, IntVar
import os
import nbformat
from datetime import datetime

# Default directory set to the Documents folder
default_directory = os.path.expanduser('~/Documents')

def select_directory():
    """ Opens a dialog to select a directory and updates the directory label. """
    directory = filedialog.askdirectory(initialdir=default_directory)
    directory_label.config(text=directory)

def show_in_finder(file_path):
    """ Open the file in Finder """
    os.system(f"open -R '{file_path}'")

def search_string_in_files():

    directory = directory_label.cget("text")
    search_str = search_entry.get()
    result_text.delete('1.0', tk.END)

    include_py = py_var.get()
    include_ipynb = ipynb_var.get()

    search_results = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if (include_py and file.endswith(".py")) or (include_ipynb and file.endswith(".ipynb")):
                file_path = os.path.join(root, file)
                try:
                    if file.endswith(".py"):
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                        except UnicodeDecodeError:
                            with open(file_path, 'r', encoding='latin-1') as f:
                                content = f.read()

                        if search_str in content:
                            mod_time = os.path.getmtime(file_path)
                            search_results.append((file_path, mod_time))
                    elif file.endswith(".ipynb"):
                        with open(file_path, 'r', encoding='utf-8') as f:
                            nb = nbformat.read(f, as_version=4)
                            for cell in nb.cells:
                                if cell.cell_type == 'code' and search_str in cell.source:
                                    result_text.insert(tk.END, file_path + '\n')
                                    break
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")  # Debug log
                    result_text.insert(tk.END, f"Error reading {file_path}: {e}\n")

               
    # Debug print
    print(f"Found {len(search_results)} results")

    # Sort results by date modified
    search_results.sort(key=lambda x: x[1], reverse=True)

    # Display results with date modified
    for file_path, mod_time in search_results:
        mod_time_str = datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d %H:%M:%S')
        result_text.insert(tk.END, f"{mod_time_str} - {file_path}\n")

        # Add button to show in Finder
        finder_button = Button(root, text="Show in Finder", command=lambda fp=file_path: show_in_finder(fp))
        finder_button.pack()

    # Debug print
    print("Displayed results and added buttons")

# Create the main window
root = tk.Tk()
root.title("Code Search Tool")

# Add GUI elements
select_button = tk.Button(root, text="Select Directory", command=select_directory)
select_button.pack()

directory_label = tk.Label(root, text="No directory selected")
directory_label.pack()

search_label = tk.Label(root, text="Enter string to search:")
search_label.pack()

search_entry = tk.Entry(root)
search_entry.pack()

search_button = tk.Button(root, text="Search", command=search_string_in_files)
search_button.pack()

result_text = scrolledtext.ScrolledText(root, wrap=tk.WORD)
result_text.pack(expand=True, fill='both')

# Variables for checkboxes
py_var = IntVar(value=1)  # Default checked
ipynb_var = IntVar(value=1)  # Default checked

# Add checkboxes for file types
py_checkbox = Checkbutton(root, text=".py files", variable=py_var)
ipynb_checkbox = Checkbutton(root, text=".ipynb files", variable=ipynb_var)
py_checkbox.pack()
ipynb_checkbox.pack()



# Set default directory
directory_label.config(text=default_directory)


# Run the application
root.mainloop()
