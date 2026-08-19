# File-Sorter
A desktop file management application built with Python and CustomTkinter that automatically organises files into categorized folders based on their file extensions. The application supports drag and drop file management, recursive folder scanning, duplicate file handling, sorting previews, undo functionality, and persistent destination settings. 

Features
->Drag and Drop -- Add multiple files directly into the application 
->Folder Import -- Add an entire folder, including files inside subfolders 
->Automatic Catgorisation -- Files are sorted based on their extensions 
->Duplicate Handling -- Existing files are not overwritten. Duplicate filenames are renamed automatically
->Sorting Preview -- Review where files will be placed before sorting
->Undo Last Sort -- Restore files from the most recent sorting operation. 
->Individual File Removal -- Remove unwanted files from the queue
->Clear All -- Quickly empty the current file queue
->Persistent Settings -- The selected destination folder is remembered between sessions. 
->Error Handling -- Failed files remain in the queue instead of stopping the entire sorting operations.
->Standalone Executable -- Packaged into a windows.exe using PyInstaller 

