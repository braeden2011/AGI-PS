import os
import tkinter as tk
from tkinter import filedialog, messagebox
from agi_and_PS_process import  agisoft_do_photogrammetry

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File Count")
        
        self.project_folder = None
        self.topo_csv = None
        self.camera_cal = None
        self.gcp_csv = None
        
        self.create_widgets()

    def count_jpg_files(self, folder_path):
        jpg_count = 0
        for root, dirs, files in os.walk(folder_path):
            if 'Exports' in dirs:
                dirs.remove('Exports')  # Exclude 'exports' subfolder from traversal
            jpg_count += sum(1 for file in files if file.lower().endswith('.jpg'))
        return jpg_count

    def check_project_folder(self):
        folder_path = self.project_folder_entry.get()
        if folder_path:
            jpg_count = self.count_jpg_files(folder_path)
            self.result_label.config(text=f"Number of .jpg files: {jpg_count}")
            if jpg_count == 0:
                self.warning_label.config(text="Warning: No .jpg files found!")
                self.do_photogrammetry_button.config(state="disabled")
            if not self.topo_csv_entry.get():
                proceed = messagebox.askyesno("Warning", "No topo.csv file selected. Proceed without it?")
                if not proceed:
                    return
            if not self.camera_cal_entry.get():
                proceed = messagebox.askyesno("Warning", "No camera cal.xml file selected. Proceed without it?")
                if not proceed:
                    return
            if not self.gcp_csv_entry.get():
                proceed = messagebox.askyesno("Warning", "No GCP.csv file selected. Proceed without it?")
                if not proceed:
                    return
            self.do_photogrammetry_button.config(state="normal")
            self.check_button.config(state="disabled")
            
            # Set variables usable elsewhere
            self.project_folder = folder_path
            self.topo_csv = self.topo_csv_entry.get() or False
            self.camera_cal = self.camera_cal_entry.get() or False
            self.gcp_csv = self.gcp_csv_entry.get() or False
        else:
            self.result_label.config(text="Please provide a valid Project Folder path.")

    def browse_project_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.project_folder_entry.delete(0, tk.END)
            self.project_folder_entry.insert(0, folder_path)

    def browse_topo_csv(self):
        topo_csv_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if topo_csv_path:
            self.topo_csv_entry.delete(0, tk.END)
            self.topo_csv_entry.insert(0, topo_csv_path)

    def browse_camera_cal_xml(self):
        camera_cal_xml_path = filedialog.askopenfilename(filetypes=[("XML Files", "*.xml")])
        if camera_cal_xml_path:
            self.camera_cal_entry.delete(0, tk.END)
            self.camera_cal_entry.insert(0, camera_cal_xml_path)

    def browse_gcp_csv(self):
        gcp_csv_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if gcp_csv_path:
            self.gcp_csv_entry.delete(0, tk.END)
            self.gcp_csv_entry.insert(0, gcp_csv_path)

    def do_photogrammetry(self):
        agisoft_do_photogrammetry(app.project_folder, app.topo_csv, app.camera_cal, app.gcp_csv)
        self.quit()

        pass

    def create_widgets(self):
        # Create and place input fields
        self.project_folder_label = tk.Label(self, text="Project Folder:")
        self.project_folder_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.project_folder_entry = tk.Entry(self, width=50)
        self.project_folder_entry.grid(row=0, column=1, padx=5, pady=5)
        self.browse_project_button = tk.Button(self, text="Browse", command=self.browse_project_folder)
        self.browse_project_button.grid(row=0, column=2, padx=5, pady=5)

        self.topo_csv_label = tk.Label(self, text="Topo.csv:")
        self.topo_csv_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.topo_csv_entry = tk.Entry(self, width=50)
        self.topo_csv_entry.grid(row=1, column=1, padx=5, pady=5)
        self.browse_topo_csv_button = tk.Button(self, text="Browse", command=self.browse_topo_csv)
        self.browse_topo_csv_button.grid(row=1, column=2, padx=5, pady=5)

        self.camera_cal_label = tk.Label(self, text="Camera cal.xml:")
        self.camera_cal_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.camera_cal_entry = tk.Entry(self, width=50)
        self.camera_cal_entry.grid(row=2, column=1, padx=5, pady=5)
        self.browse_camera_cal_xml_button = tk.Button(self, text="Browse", command=self.browse_camera_cal_xml)
        self.browse_camera_cal_xml_button.grid(row=2, column=2, padx=5, pady=5)

        self.gcp_csv_label = tk.Label(self, text="GCP.csv:")
        self.gcp_csv_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.gcp_csv_entry = tk.Entry(self, width=50)
        self.gcp_csv_entry.grid(row=3, column=1, padx=5, pady=5)
        self.browse_gcp_csv_button = tk.Button(self, text="Browse", command=self.browse_gcp_csv)
        self.browse_gcp_csv_button.grid(row=3, column=2, padx=5, pady=5)

        # Create and place the result label
        self.result_label = tk.Label(self, text="")
        self.result_label.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

        # Create and place the warning label
        self.warning_label = tk.Label(self, text="", fg="red")
        self.warning_label.grid(row=5, column=0, columnspan=3, padx=5, pady=5)

        # Create and place the check button
        self.check_button = tk.Button(self, text="Check", command=self.check_project_folder)
        self.check_button.grid(row=6, column=1, padx=5, pady=5)

        # Create the "Do Photogrammetry" button initially disabled
        self.do_photogrammetry_button = tk.Button(self, text="Do Photogrammetry", command=self.do_photogrammetry, state="disabled")
        self.do_photogrammetry_button.grid(row=7, column=1, padx=5, pady=5)

# Create an instance of the Application class
app = Application()

# Start the main event loop
app.mainloop()


