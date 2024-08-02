import tkinter as tk
import customtkinter as ctk
import shutil
import os

from detect import detect_result, batch_detection

ctk.set_appearance_mode("System");
ctk.set_default_color_theme("blue")

#setup app
app = ctk.CTk()
app.geometry("720x400")
app.title("Detect Animals")

#setup UI
title = ctk.CTkLabel(app, text="Detect Animals", font=("Arial", 24))
title.pack()

#Create Environment Variables
photoFolder = tk.StringVar();
threshold = tk.DoubleVar();
destinationFolder = tk.StringVar();
files = []

def select_folder(folder_entry):
    folder_path = ctk.filedialog.askdirectory()
    folder_entry.delete(0, tk.END)
    folder_entry.insert(0, folder_path)

def folderSelectCommand(folder_entry):
    return lambda: select_folder(folder_entry)

def handleDetect(photoFolderPath, threshold, destinationFolderPath):
    result_message.configure(text="Running...")
    result_message.update()
    result, message = batch_detection(photoFolderPath, threshold) 
    truncated_res = ""
    truncated_res += message + "\n"
    for i in range(len(result)):
        if i < 4:
            truncated_res += result[i] + "\n"
    result_message.configure(text=truncated_res)
    result_message.update()
    global files
    files = result
    
    copy_button.pack(padx=10, pady=10)
    

def copyfiles():
    print(files)
    for photo in files:
        shutil.copy(photo, destinationFolder.get())
        print("Copied " + photo + " to " + destinationFolder.get())

def runApp():
    return lambda: handleDetect(photoFolder.get(), threshold.get(), destinationFolder.get())

#setup threshold selection
threshold_frame = ctk.CTkFrame(app)
threshold_frame.pack(padx=10, pady=10)
threshold_label = ctk.CTkLabel(threshold_frame, text="Threshold: ")
threshold_label.pack(side="left")
threshold_entry = ctk.CTkEntry(threshold_frame, width=200, textvariable=threshold)
threshold_entry.pack(side="left", padx=10)


#setup folder selection
folder_frame_orgs = ctk.CTkFrame(app)
folder_frame_orgs.pack(padx=10, pady=10)
folder_label = ctk.CTkLabel(folder_frame_orgs, text="Photo Folder Path: ")
folder_label.pack(side="left")
folder_entry_photos = ctk.CTkEntry(folder_frame_orgs, width=200, textvariable=photoFolder)
folder_entry_photos.pack(side="left", padx=10)
folder_button = ctk.CTkButton(folder_frame_orgs, text="Select Folder", command=folderSelectCommand(folder_entry_photos))
folder_button.pack(side="left")

#setup folder selection
folder_frame_dest = ctk.CTkFrame(app)
folder_frame_dest.pack(padx=10, pady=10)
folder_label = ctk.CTkLabel(folder_frame_dest, text="Destination Folder Path: ")
folder_label.pack(side="left")
folder_entry_dest = ctk.CTkEntry(folder_frame_dest, width=200, textvariable=destinationFolder)
folder_entry_dest.pack(side="left", padx=10)
folder_button = ctk.CTkButton(folder_frame_dest, text="Select Folder", command=folderSelectCommand(folder_entry_dest))
folder_button.pack(side="left")


#setup submit button
submit_button = ctk.CTkButton(app, text="Run", command=runApp())
submit_button.pack(padx=10, pady=10)

#setup result message
result_message = ctk.CTkLabel(app, text="")
result_message.pack()

#setup copy files button
copy_button = ctk.CTkButton(app, text="Copy Files", command=copyfiles)
copy_button.pack_forget()









#run app
app.mainloop()