from library.agisoft.metashape_workflow_V1 import *
from library.pointstudio.importLaz import *

from library.pointstudio.Import_CSV import *
#from library.pointstudio.Import_CSV_V3 import *
import os
import subprocess
from library.spltCSVByCode import *


#the below breaks if run multiple times, attempt to use previous runs exported images as inputs for next run
#export_directory = input_directory


def agisoft_do_photogrammetry(project_folder, topo_csv, camera_cal, gcp_csv):
        
    #Get the name of the project based on the project folder selected in the gui
    try:
        input_folder, projectName =  os.path.split(project_folder)
        print(f"Project name: {projectName}")

    except FileNotFoundError as e:
        print("Error finding project folder. Looking in: " + project_folder + ". Exiting.")
        input()
        exit()


    #set output folder to a subfolder of the project folder called "Exports" 
    try:
        output_folder = os.path.join(project_folder, "Exports")
    except NameError as e:
        print("Import or Export folder not found. D:\AGI IMPORTS and D:\AGISOFT EXPORTS.")
        input()
        exit()



    ###This is all nice to have stuff for splitting a single CSV into SH and GCP files. maybe later do in the GUI?
    """ # Get the list of files in the project input directory to check for topo and gcp CSV's
    files = [f for f in os.listdir(os.path.join(input_directory, projectName)) if os.path.isfile(os.path.join(os.path.join(input_directory, projectName), f))]

    #check for CSVs
    #csv_files = [f for f in files if f.lower() != 'gcp.csv'.lower() and f.endswith('.csv')]
    csv_files = [f for f in files if f.lower().endswith('.csv')]

    gcpPath = None

    # Check if there is only one CSV file, checks for GCP coded rows in csv and splits GCP out to seperate file
    if len(csv_files) == 1:
        # Get the full path to the topo CSV file
        csvPath = os.path.join(os.path.join(input_directory, projectName), csv_files[0])
        print("No GCP.csv found. Checking topo CSV for GCPs")
        print("CSV topo path: " + csvPath)
        #filter topo csv for GCP's and write to GCP.csv
        filter_and_write_csv(csvPath, project_folder, "GCP", ['gcp', 'pgcp', 'GCP', 'PGCP'], 4)
        filter_and_write_csv(csvPath, project_folder, projectName + " topo", ['sh', 'SH', 'PSHT', 'psht'], 4)
        topoCSVPath = os.path.join(input_directory, projectName, projectName + " topo.csv")
        files = [f for f in os.listdir(os.path.join(input_directory, projectName)) if os.path.isfile(os.path.join(os.path.join(input_directory, projectName), f))]
        gcp_file = next((f for f in files if f.lower().endswith('gcp.csv')), None)
        gcpPath = False
        if gcp_file:


            print("GCP's found in csv and GCP.csv written.")
            #Do you want to use these GCP prompt? set GCP use FLAG here
            if input("Do you want to use the GCPs found? (yes/y) ").strip().lower() in ["yes", "y"]:
                gcpPath = os.path.join(os.path.join(input_directory, projectName), gcp_file)

        else:
            print("Still no GCPs Found. Press enter to continue without GCPs.")
            input()



    #checks if there are 2 CSVs, and one ends in gcp.csv
    elif len(csv_files) == 2 and any(file.lower().endswith('gcp.csv') for file in csv_files):
        csvPath = os.path.join(input_directory ,projectName, next(f for f in csv_files if not f.lower().endswith('gcp.csv')))
        filter_and_write_csv(csvPath, project_folder, projectName + " topo", ['sh', 'SH', 'PSHT', 'psht'], 4)
        topoCSVPath = os.path.join(input_directory, projectName, projectName + " topo.csv")
        gcp_file = next((f for f in files if f.lower().endswith('gcp.csv')), None)
        print("GCP.csv found.")
        #Do you want to use these GCP prompt? set GCP use FLAG here
        if input("Do you want to use the GCPs found? (yes/y) ").strip().lower() in ["yes", "y"]:
            gcpPath = os.path.join(os.path.join(input_directory, projectName), gcp_file)

    elif len(csv_files) == 2 and not any(file.lower().endswith('gcp.csv') for file in csv_files):
        print("Too many CSVs in input folder. Press enter to continue without topo for QA or GCP.")
        gcpPath = False
        input()

    elif len(csv_files) == 0:
        print("No topo or GCP CSV found in input folder. Press enter to continue without topo for QA or GCP.")
        gcpPath = False
        input()

    elif len(csv_files) >= 3:  
        print("Too many CSVs in input folder. Press enter to continue without topo for QA or GCP.")
        gcpPath = False
        input()
 """

    
    lazPath = doPhotogrammetry(gcp_csv, projectName, project_folder, output_folder, camera_cal) 
    #lazPath = str(os.path.join(export_directory, projectName) + "\\" + projectName +".laz")


    
    # Get a list of running maptek applications.
    try:
        applications = Project.find_running_applications()
    except:
        print("Could not connect to Pointstudio, photogrammetry done, surface creation not done. Make sure you have a Pointstudio database open.")
    
    for i, application in enumerate(applications):
        print(f"{i} - {application.bin_path}")
    
    if len(applications) == 1 and "PointStudio" in ''.join(map(str, applications)):
    
        print("Only one PointStudio application running - Press enter to continue surface creation and QA.")
        input()
    else:
        print("Surface creation and QA will be attempted in the most recently opened Pointstudio / Vulcan instance, please make sure the most recently opened is the desired POINTSTUDIO database and press enter.")
    input()
    



    project = Project()
    pointcloud_Path = "working/new pickup/"
    PS_topo_Path = "working/new topo/"


    try:
        import_csv(project, topo_csv, PS_topo_Path)
    except:
        print("CSV failed to import into PaintStudio")
        
    try:    
        importLaz(project, lazPath, pointcloud_Path) 
    except:
        print("Laz failed to import into PointStudio") 



    command = "\"C:\Program Files\Common Files\Maptek\Workbench\Shell\WbCommand.exe\" -c Maptek.Workbench.Workflow.Commands.WorkflowDefaultRun -f \"C:\scripts\Process_Scan_with_PythonV2.wfd\""

    try:
        # Run the  command to exectue the PointStudio workflow
        result = subprocess.run(command)

        # Print the output of the PowerShell command
        print("cmd Output:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        # Print any error that occurred
        print("Error:", e)

