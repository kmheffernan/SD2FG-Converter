import tkinter as tk
from tkinter import filedialog
from tkinter import PhotoImage
from pathlib import Path
import sys

def select_json_file(selected_file_label, selected_file_dic, button_dic):
    # Open file selection dialog
    file_path = filedialog.askopenfilename(title="Select a JSON file:", filetypes=[("JSON Files", "*.json")])
    if file_path:
        file_path = Path(file_path) #convert the text string to a Path object
        selected_file_dic['file'] = file_path
        selected_file_name = file_path.name
        selected_file_dic['status'] = f"Selected file: {selected_file_name}"
        button_dic['convert'].config(state="normal")  # Enable the convert button
    else:
        selected_file_dic['file'] = None
        selected_file_dic['status'] = 'No file selected.'
    selected_file_label.config(text=selected_file_dic['status'])

def exit_no_save(window, selected_file_dic):
    selected_file_dic['file'] = None
    window.destroy()
    
def get_json_file_window():
    button_dic = {} #put pointers to the gui buttons
    selected_file_dic = {'status': 'No file selected.', 'file': None}
    
    # Create the main window
    window = tk.Tk()
    window.title("Shadowdarklings to Fantasy Grounds Converter")
    window.configure(bg="white")

    # Add a header image
    logo_image = None
    try:
        logo_image = PhotoImage(file="splash.png")
        logo_label = tk.Label(window, image=logo_image, bg="white", highlightbackground="black", highlightthickness=2)
        logo_label.pack(pady=10)
    except Exception as e:
        print(f"Error loading image: {e}")

    # Add a label with a description
    label = tk.Label(window, bg="white", text=
'''This software is an independent product published under the
Shadowdark RPG Third-Party License and is not affiliated with
The Arcane Library, LLC. Shadowdark RPG (c) 2023 The Arcane
Library, LLC. This project is licensed under the Creative Commons
Attribution-NonCommercial 4.0 International License. See the
License file for details.''')
    label.pack(pady=10)

    # Add a label to display the status message
    selected_file_label = tk.Label(window, text=selected_file_dic['status'], bg="white", highlightbackground="black", highlightthickness=2)
    selected_file_label.pack(pady=10)

    # Create a frame to hold the buttons at the bottom
    button_frame = tk.Frame(window, bg="white")
    button_frame.pack(side="bottom", pady=10)

    # Add a button to open the file dialog
    select_file_button = tk.Button(button_frame, text="Open File", command=lambda: select_json_file(selected_file_label, selected_file_dic, button_dic))
    select_file_button.pack(side="left", padx=10)
    button_dic['select'] = select_file_button

    # Add a button to exit the application
    exit_button = tk.Button(button_frame, text="Exit", command=lambda: exit_no_save(window, selected_file_dic))
    exit_button.pack(side="left", padx=10)
    button_dic['exit'] = exit_button

    # Add a button to convert the selected file
    convert_button = tk.Button(button_frame, text="Convert", state="disabled", command=window.destroy)
    convert_button.pack(side="left", padx=10)
    button_dic['convert'] = convert_button

    window.mainloop()
    if selected_file_dic['file']:
        return selected_file_dic['file']
    else:
        return False

def change_save_path(selected_path_label, selected_path_dic):
    # Open file selection dialog
    directory_path = filedialog.askdirectory(title="Select Folder")
    if directory_path:
        save_path = Path(directory_path) #convert the text string to a Path object
        selected_path_dic['path'] = save_path
        selected_path_dic['status'] = f'Save folder: {save_path}'
        selected_path_name = save_path.name
    else:
        selected_path_dic['path'] = None
        selected_path_dic['status'] ='No save folder selected.'
    selected_path_label.config(text=selected_path_dic['status'])

def exit_no_path(window, selected_path_dic):
    selected_path_dic['path'] = None
    window.destroy()

def confirm_save_window(save_path, log_text):
    button_dic = {} #pointers to the gui buttons
    selected_path_dic = {'path': save_path}
    selected_path_dic['status'] = f'Save folder: {save_path}'
    
    # Create the main window
    window = tk.Tk()
    window.title("Shadowdarklings to Fantasy Grounds Converter")
    window.configure(bg="white")

    # Add a label with the log text
    label = tk.Label(window, bg="white", text=log_text)
    label.pack(pady=10)

    # Add a label to display the save path
    selected_path_label = tk.Label(window, text=selected_path_dic['status'], bg="white", highlightbackground="black", highlightthickness=2)
    selected_path_label.pack(pady=10)

    # Create a frame to hold the buttons at the bottom
    button_frame = tk.Frame(window, bg="white")
    button_frame.pack(side="bottom", pady=10)

    # Add a button to change save path
    change_path_button = tk.Button(button_frame, text="Change Save Folder", command=lambda: change_save_path(selected_path_label, selected_path_dic))
    change_path_button.pack(side="left", padx=10)
    button_dic['change'] = change_path_button

    # Add a button to exit the application without saving
    exit_button = tk.Button(button_frame, text="Exit", command=lambda: exit_no_path(window, selected_path_dic))
    exit_button.pack(side="left", padx=10)
    button_dic['exit'] = exit_button

    # Add a button to save the xml file to the selected path
    convert_button = tk.Button(button_frame, text="Save", command=window.destroy)
    convert_button.pack(side="left", padx=10)
    button_dic['save'] = convert_button

    window.mainloop()
    if selected_path_dic['path']:
        return selected_path_dic['path']
    else:
        return False

if __name__ == "__main__":
##    file = get_json_file_window()
##    if file:
##        print(f"File chosen is: {file.name}")
##    else:
##        print("No file chosen.")
##        sys.exit()
    initial_save_path = Path.cwd() / 'out' 
    log_text = "Sample log text."
    save_path = confirm_save_window(initial_save_path, log_text)
    if save_path:
        print(f"Save folder chosen is: {save_path}")
    else:
        print("No save folder chosen.")
        sys.exit()
    
        
