import customtkinter as ctk 
import os
import json
import shutil
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter import filedialog, messagebox

destination_path = ""
config_file = "config.json"
dropped_files = []
file_rows = []
sort_history = []
empty_label = None

#--------sorting rules--------
file_categories = {
    "Documents": [
        ".pdf",
        ".doc",
        ".docx",
        ".txt",
        ".xlsx",
        ".xls",
        ".pptx",
        ".ppt"
    ],

    "Images": [
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".bmp",
        ".webp"
    ],

    "Programming": [
        ".py",
        ".c",
        ".cpp",
        ".h",
        ".hpp",
        ".ino",
        ".java",
        ".js"
    ],

    "Electronics": [
        ".kicad_sch",
        ".kicad_pcb",
        ".sch",
        ".brd"
    ],

    "3D Models": [
        ".stl",
        ".step",
        ".stp",
        ".obj",
        ".3mf"
    ],

    "Videos": [
        ".mp4",
        ".mkv",
        ".avi",
        ".mov"
    ]
}

#--------base refference-------
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

#-------add folder function-----
def add_folder():
    folder = filedialog.askdirectory(title="Select Folder")

    if not folder:
        return 

    for root, directories, files in os.walk(folder):

        for filename in files:
            file_path = os.path.join(root, filename)

            if os.path.isfile(file_path):
                if file_path not in dropped_files:
                    dropped_files.append(file_path)

    file_count_label.configure(text=f"Files Ready: {len(dropped_files)}")

    update_file_list()

#-------preview function--------
def preview_sort():
    if not dropped_files:
        status_label.configure(text="No files to preview.")
        return 

    if not destination_path:
        status_label.configure(text="No destination folder selected.")
        return

    preview_window = ctk.CTkToplevel(app)
    preview_window.geometry("800x800")
    preview_window.resizable(True,True)

    title_label = ctk.CTkLabel(preview_window, text="Sorting Preview", font=ctk.CTkFont(size=20,weight="bold"))
    title_label.pack(padx=20,pady=(20,10))

    preview_list = ctk.CTkScrollableFrame(preview_window,corner_radius=10)
    preview_list.pack(padx=20,pady=10,fill="both",expand=True)

    for file in dropped_files:
        filename = os.path.basename(file)
        category = get_category(file)

        row = ctk.CTkFrame(preview_list, height=35, corner_radius=8)
        row.pack(fill="x",padx=5,pady=5)

        file_label = ctk.CTkLabel(row, text=filename, anchor="w")
        file_label.pack(side="left",padx=10,fill="x",expand=True)

        category_folder = os.path.join(destination_path,category)

        category_label = ctk.CTkLabel(row,text=category_folder,width=120)
        category_label.pack(side="right",padx=10)

    count_label = ctk.CTkLabel(preview_window,text=f"{len(dropped_files)} files will be sorted.", font=ctk.CTkFont(size=13))
    count_label.pack(pady=(5,10))

    close_button = ctk.CTkButton(preview_window,text="Close",command=preview_window.destroy)
    close_button.pack(pady=(0,20))

#-------duplicate name handler--------
def get_unique_filename(folder,filename):
    base_name, extension = os.path.splitext(filename)

    counter = 1
    new_filename = filename

    while os.path.exists(os.path.join(folder, new_filename)):
        new_filename = f"{base_name} ({counter}){extension}"
        counter += 1

    return new_filename

#-------undo last sort------
def undo_last_sort():
    if not sort_history:
        status_label.configure(text="Nothing to undo")
        return 

    restored_count = 0

    for move in reversed(sort_history):
        try:
            shutil.move(move["destination"], move["original"])
            restored_count += 1

        except Exception as error:
            print(f"Failed to restore {move['destination']}: {error}")

    if restored_count == len(sort_history):
        status_label.configure(text=f"Successfully restored {restored_count} files.")
        sort_history.clear()

    else:
        status_label.configure(text=f"Restored {restored_count} files, but some files could not be restored.")

#-------destination source------
def destination_is_inside_source():
    destination = os.path.abspath(destination_path)

    for file in dropped_files:
        source = os.path.abspath(file)

        if os.path.commonpath([source,destination]) == destination:
            return True 

    return False

#-------sorting files-------
def sort_files():
    if not dropped_files:
        status_label.configure(text="No files to sort.")
        return 

    if not destination_path:
        status_label.configure(text="No destination folder selected.")
        return 

    if destination_is_inside_source():
        messagebox.showwarning("Invalid Destination", "The destination folder cannot be inside a folder containing files being sorted")
        return

    confirm = messagebox.askyesno("Confirm Sort", f"Are you sure you want to sort {len(dropped_files)} files?")

    if not confirm:
        status_label.configure(text="Sorting Cancelled.")
        return 

    sort_history.clear() #clear previous history logs 

    sorted_count = 0
    failed_count = 0
    failed_files = []

    for file in dropped_files:
        try:
            
            category = get_category(file)
            category_folder = os.path.join(destination_path, category)

            #create directory if folder does not exist
            os.makedirs(category_folder, exist_ok=True)
            filename = os.path.basename(file)

            filename = get_unique_filename(category_folder, filename) #tackle duplicate names 

            #create final destination path 
            destination_file = os.path.join(category_folder, filename)
            shutil.move(file,destination_file)

            sort_history.append({
                "original": file,
                "destination": destination_file
            })

            print(f"{filename} -> {category}")
            sorted_count += 1

        except Exception as e:
            failed_count += 1
            failed_files.append(file)
            print(f"Failed to sort {file}: {str(e)}")

    if failed_count == 0:
        status_label.configure(text=f"Sorted {sorted_count} files successfully.")

    else:
        status_label.configure(text=f"{sorted_count} files sorted successfully, {failed_count} files failed to sort.")

    dropped_files.clear()
    dropped_files.extend(failed_files) #keep failed files 

    file_count_label.configure(text=f"Files Ready: {len(dropped_files)}")

    update_file_list()

    
#-------get category--------
def get_category(file):
    extension = os.path.splitext(file)[1].lower()

    for category,extensions in file_categories.items():
        if extension in extensions:
            return category

    return "Others"

#-------load config--------
def load_config():
    global destination_path

    if os.path.exists(config_file):
        with open(config_file, "r") as file:
            config = json.load(file)
            destination_path = config.get("destination", "")

#-------save config--------
def save_config():
    config = {"destination": destination_path}

    with open(config_file, "w") as file:
        json.dump(config, file)

#-------browse destination folder--------
def browse_destination():
    global destination_path

    folder = filedialog.askdirectory(title="Select Destination Folder")

    if folder:
        destination_path = folder
        destination_label.configure(text=f"Destination: {destination_path}")
        save_config()

#-------clear all----------
def clear_all():
    dropped_files.clear()

    file_count_label.configure(text=f"Files Ready: 0")
    update_file_list()

#-------remove file function--------
def remove_file(file):
    if file in dropped_files:
        dropped_files.remove(file)

    file_count_label.configure(text=f"Files Ready: {len(dropped_files)}")
    update_file_list()

#-------update file list--------
def update_file_list():
    global empty_label

    #remove existing rows
    for row in file_rows:
        row.destroy()

    file_rows.clear()

    #remove empty label if it exists
    if  empty_label is not None:
        empty_label.destroy()
        empty_label = None

    #if no files are dropped, show empty label
    if len(dropped_files) == 0:
        empty_label = ctk.CTkLabel(file_list_frame, text="No Files dropped", font=ctk.CTkFont(size=14))
        empty_label.pack(padx=30, pady=(10, 0))
        return

    #create new rows for each dropped file 
    for file in dropped_files:
        row = ctk.CTkFrame(file_list_frame, width=400, height=30, corner_radius=8)
        row.pack(fill="x",padx=5,pady=3)

        file_label = ctk.CTkLabel(row, text=os.path.basename(file), anchor="w",font=ctk.CTkFont(size=12))
        file_label.pack(side="left", padx=10, fill="x",expand=True)

        remove_button = ctk.CTkButton(row,text="x", width=35, height=25, bg_color="transparent", fg_color="transparent", hover_color="red",
                                      font=ctk.CTkFont(size=14), command=lambda f=file: remove_file(f))
        remove_button.pack(padx=30, pady=(0,10))

        file_rows.append(row)

#--------file drop function--------
def on_drop(event):
    files = app.tk.splitlist(event.data)

    for file in files:
        if file not in dropped_files:
            dropped_files.append(file)

    file_count_label.configure(text=f"Files Ready: {len(dropped_files)}")
    print("Dropped files:")

    update_file_list()

    for file in dropped_files:
        print(file)

#--------main window--------
app = ctk.CTk()
TkinterDnD._require(app)

app.title("File Sorter")
app.geometry("1000x800")
app.minsize(700,600)

#--------main title--------
title = ctk.CTkLabel(app, text="File Sorter", font=ctk.CTkFont(size=28, weight="bold",family="Times New Roman"))
title.pack(padx = 30, pady=(30,5))

#--------sub title--------
subtitle = ctk.CTkLabel(app, text="Organise your files automatically", font=ctk.CTkFont(size=14,family="Times New Roman"))
subtitle.pack(padx = 30, pady=1)

author_subtitle = ctk.CTkLabel(app, text="Created by: Muhammad Hafiz Bin Abdul Aziz", font=ctk.CTkFont(size=13,family="Times New Roman"))
author_subtitle.pack(padx=30,pady=3)

#--------drop area--------
drop_area = ctk.CTkFrame(app, width=400, height=250, corner_radius=12)
drop_area.pack(padx=30, pady=20, fill="both", expand=True)

drop_area.drop_target_register(DND_FILES)
drop_area.dnd_bind("<<Drop>>", on_drop)

drop_label = ctk.CTkLabel(drop_area, text="Drag and drop files here\nor use Add Folder below", font=ctk.CTkFont(size=15,family="Times New Roman"))
drop_label.pack(padx=30, pady=(0,10))

file_count_label = ctk.CTkLabel(drop_area, text="Files Ready: 0", font=ctk.CTkFont(size=14,family="Times New Roman"))
file_count_label.pack(padx=30, pady=(10, 0))

buttons_frame = ctk.CTkFrame(app,fg_color="transparent", corner_radius=10)
buttons_frame.pack(padx=30, pady=(5, 20), fill="x")

top_buttons_frame = ctk.CTkFrame(buttons_frame, fg_color="transparent", corner_radius=10)
top_buttons_frame.pack(fill="x",pady=(0,8))

middle_buttons_frame = ctk.CTkFrame(buttons_frame, fg_color="transparent", corner_radius=10)
middle_buttons_frame.pack(fill="x",pady=(0,8))

add_folder_button = ctk.CTkButton(top_buttons_frame,width=140,height=55,text="Add Folder",font=ctk.CTkFont(size=20,family="Times New Roman"),command=add_folder)
add_folder_button.pack(side="left",fill="x",expand=True,padx=(0,5))

clear_button = ctk.CTkButton(top_buttons_frame, width=140, height=55, text="Clear All", hover_color="red", font=ctk.CTkFont(size=20,family="Times New Roman"), command=clear_all)
clear_button.pack(side="right",fill="x",expand=True,padx=(0,5))

preview_button = ctk.CTkButton(middle_buttons_frame, width=140, height=55, text="Preview Sort", font=ctk.CTkFont(size=20,family="Times New Roman"), command=preview_sort)
preview_button.pack(side="left",fill="x",expand=True,padx=(0,5))

undo_button = ctk.CTkButton(middle_buttons_frame, width=140, height=55, text="Undo Last Sort", hover_color="red",font=ctk.CTkFont(size=20,family="Times New Roman"), command=undo_last_sort)
undo_button.pack(side="right",fill="x",expand=True,padx=(0,5))

sort_button = ctk.CTkButton(buttons_frame, width=180, height=55, text="Sort Files", font=ctk.CTkFont(size=28,family="Times New Roman"), command=sort_files)
sort_button.pack(fill="x")

status_label = ctk.CTkLabel(app, text="Ready", font=ctk.CTkFont(size=14))
status_label.pack(padx=30, pady=(0,20))

#-------destination folder selection--------
destination_frame = ctk.CTkFrame(app, fg_color="transparent")
destination_frame.pack(padx=30, pady=(0,20), fill="x")

destination_title = ctk.CTkLabel(destination_frame, text="Destination Folder:", font=ctk.CTkFont(size=14, weight="bold",family="Times New Roman"))
destination_title.pack(anchor="w")

destination_label = ctk.CTkLabel(destination_frame, bg_color="gray",text="No Destination Selected", font=ctk.CTkFont(size=14,family="Times New Roman"))
destination_label.pack(anchor="w", padx=10, pady=(0,5), fill="x", expand=True)

load_config()

if destination_path:
    destination_label.configure(text=destination_path)

browse_button = ctk.CTkButton(destination_frame, width=180, height=28, text="Browse", font=ctk.CTkFont(size=14,family="Times New Roman"), command=browse_destination)
browse_button.pack(anchor="e", padx=10, pady=(0,5))

#-------file list---------
file_list_frame = ctk.CTkScrollableFrame(app, width=400, height=200, corner_radius=10)
file_list_frame.pack(padx=30, pady=(0,40), fill="x")

#---------main loops---------
app.mainloop()