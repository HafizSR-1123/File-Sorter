# File-Sorter
A desktop file management application built with Python and CustomTkinter that automatically organises files into categorized folders based on their file extensions. The application supports drag and drop file management, recursive folder scanning, duplicate file handling, sorting previews, undo functionality, and persistent destination settings. 

## Features

- Drag and Drop -- Add multiple files directly into the application 

- Folder Import -- Add an entire folder, including files inside subfolders 

- Automatic Catgorisation -- Files are sorted based on their extensions 

- Duplicate Handling -- Existing files are not overwritten. Duplicate filenames are renamed automatically

- Sorting Preview -- Review where files will be placed before sorting

- Undo Last Sort -- Restore files from the most recent sorting operation. 

- Individual File Removal -- Remove unwanted files from the queue

- Clear All -- Quickly empty the current file queue

- Persistent Settings -- The selected destination folder is remembered between sessions. 

- Error Handling -- Failed files remain in the queue instead of stopping the entire sorting operations.

- Standalone Executable -- Packaged into a windows.exe using PyInstaller 

## Interface 

<img width="1000" height="822" alt="image" src="https://github.com/user-attachments/assets/7ec9c7f9-64e2-4f14-81ef-66a2a3b84c5c" />

## Supported File Categories 

The application currently supports the following categories:

### Documents

Supported extensions:

- '.pdf'

- '.doc'

- '.docx'

- '.txt'

### Images

Supported extensions:

- '.jpg'

- '.jpeg'

- '.png'

- '.gif'

### Programming Codes

Supported extensions:

- '.py'

- '.c'

- '.cpp'

- '.h'

### Electronics 

Supported extensions:

- '.kicad_sch'

- '.kicad_pcb'

- '.sch'

- '.brd'

### 3D models 

Supported extensions:

- '.stl'

- '.step'

- '.stp'

- '.obj'

- '.3mf'

### Videos

Supported extensions:

- '.mp4'

- '.mkv'

- '.avi'

- '.mov'

### Other

Any file extension not listed above will be automatically placed into the 'Other' Category 

## How it works

The application follows a simple sorting process 

### 1. File Selection 

Files can be added through drag-and-drop or by selecting a folder.

### 2. Category Detection 

The application checks the file extension and determines the appropriate category.

### 3. File Sorting 

The file is moved into the corresponding category folder 

## Technologies Used 

- Python

- Customtkinter

- TkinterDnD2

- JSON

- PyInstaller

## Download 

The latest Windows Executable can be downloaded from the [Releases] page

# Author 

Programmed by: Muhammad Hafiz Bin Abdul Aziz 
