import os
import tkinter as tk
from tkinter import filedialog, messagebox

def count_jpg_files(folder_path):
    jpg_count = 0
    for root, dirs, files in os.walk(folder_path):
        if 'Exports' in dirs:
            dirs.remove('Exports')  # Exclude 'exports' subfolder from traversal
        jpg_count += sum(1 for file in files if file.lower().endswith('.jpg'))
    return jpg_count

def check_project_folder():
    folder_path = project_folder_entry.get()
    if folder_path:
        jpg_count = count_jpg_files(folder_path)
        result_label.config(text=f"Number of .jpg files: {jpg_count}")
        if jpg_count == 0:
            warning_label.config(text="Warning: No .jpg files found!")
            do_photogrammetry_button.config(state="disabled")
        if not topo_csv_entry.get():
            proceed = messagebox.askyesno("Warning", "No topo.csv file selected. Proceed without it?")
            if not proceed:
                return
        if not camera_cal_entry.get():
            proceed = messagebox.askyesno("Warning", "No camera cal.xml file selected. Proceed without it?")
            if not proceed:
                return
        if not gcp_csv_entry.get():
            proceed = messagebox.askyesno("Warning", "No GCP.csv file selected. Proceed without it?")
            if not proceed:
                return
        do_photogrammetry_button.config(state="normal")
        check_button.config(state="disabled")

    else:
        result_label.config(text="Please provide a valid Project Folder path.")

def browse_project_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        project_folder_entry.delete(0, tk.END)
        project_folder_entry.insert(0, folder_path)

def browse_topo_csv():
    topo_csv_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if topo_csv_path:
        topo_csv_entry.delete(0, tk.END)
        topo_csv_entry.insert(0, topo_csv_path)

def browse_camera_cal_xml():
    camera_cal_xml_path = filedialog.askopenfilename(filetypes=[("XML Files", "*.xml")])
    if camera_cal_xml_path:
        camera_cal_entry.delete(0, tk.END)
        camera_cal_entry.insert(0, camera_cal_xml_path)

def browse_gcp_csv():
    gcp_csv_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if gcp_csv_path:
        gcp_csv_entry.delete(0, tk.END)
        gcp_csv_entry.insert(0, gcp_csv_path)

def do_photogrammetry():
    # Perform photogrammetry operations here
    pass

# Create the main window
root = tk.Tk()
root.title("File Count")

# Create and place input fields
project_folder_label = tk.Label(root, text="Project Folder:")
project_folder_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
project_folder_entry = tk.Entry(root, width=50)
project_folder_entry.grid(row=0, column=1, padx=5, pady=5)
browse_project_button = tk.Button(root, text="Browse", command=browse_project_folder)
browse_project_button.grid(row=0, column=2, padx=5, pady=5)

topo_csv_label = tk.Label(root, text="Topo.csv:")
topo_csv_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
topo_csv_entry = tk.Entry(root, width=50)
topo_csv_entry.grid(row=1, column=1, padx=5, pady=5)
browse_topo_csv_button = tk.Button(root, text="Browse", command=browse_topo_csv)
browse_topo_csv_button.grid(row=1, column=2, padx=5, pady=5)

camera_cal_label = tk.Label(root, text="Camera cal.xml:")
camera_cal_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
camera_cal_entry = tk.Entry(root, width=50)
camera_cal_entry.grid(row=2, column=1, padx=5, pady=5)
browse_camera_cal_xml_button = tk.Button(root, text="Browse", command=browse_camera_cal_xml)
browse_camera_cal_xml_button.grid(row=2, column=2, padx=5, pady=5)

gcp_csv_label = tk.Label(root, text="GCP.csv:")
gcp_csv_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
gcp_csv_entry = tk.Entry(root, width=50)
gcp_csv_entry.grid(row=3, column=1, padx=5, pady=5)
browse_gcp_csv_button = tk.Button(root, text="Browse", command=browse_gcp_csv)
browse_gcp_csv_button.grid(row=3, column=2, padx=5, pady=5)

# Create and place the result label
result_label = tk.Label(root, text="")
result_label.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

# Create and place the warning label
warning_label = tk.Label(root, text="", fg="red")
warning_label.grid(row=5, column=0, columnspan=3, padx=5, pady=5)

# Create and place the check button
check_button = tk.Button(root, text="Check", command=check_project_folder)
check_button.grid(row=6, column=1, padx=5, pady=5)

# Create the "Do Photogrammetry" button initially disabled
do_photogrammetry_button = tk.Button(root, text="Do Photogrammetry", command=do_photogrammetry, state="disabled")
do_photogrammetry_button.grid(row=7, column=1, padx=5, pady=5)

# Start the main event loop
root.mainloop()
