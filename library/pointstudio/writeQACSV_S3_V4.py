##Write QA CSV
from mapteksdk.workflows import WorkflowArgumentParser, WorkflowSelection
from mapteksdk.project import Project
from mapteksdk.pointstudio.operations import *
from mapteksdk.data import PointSet
from numpy import genfromtxt
import os
import numpy as np
import csv
import tkinter as tk
from tkinter import filedialog

parser = WorkflowArgumentParser(description="Write pointSet to csv")

#Input for Topo pointSet
parser.declare_input_connector("input1", WorkflowSelection,
                               connector_name="input1",
                               description="input1")

#Input for projected to surface Topo pointSet
parser.declare_input_connector("input2", WorkflowSelection,
                               connector_name="input2",
                               description="input2")

#Input for output folder for QA CSV
parser.declare_input_connector("outputFolder", str,
                               connector_name="outputFolder",
                               description="outputFolder")

parser.parse_arguments()

project = Project() # Connect to default project


# Temporarily store points in these arrays
all_points = np.empty([0,3], dtype=np.float_)
all_points_projected = np.empty([0,3], dtype=np.float_)


for oid in parser["input1"]:
    with project.read(oid) as obj:

        view = active_view_or_new_view() 
        view.add_objects([obj])

        CSVName = oid.path.split("/")[-1] + " QA.csv"
        projectName = oid.path.split("/")[-1]

        if hasattr(obj, 'points'):
            # Append visible points from obj to buffer object
            # Use .point_selection to get indices for all True values from the selection array
            all_points =  np.vstack((all_points, obj.points[obj.point_visibility]))


for oid in parser["input2"]:
    with project.read(oid) as obj:
        if hasattr(obj, 'points'):
            # Append visible points from obj to buffer object
            # Use .point_selection to get indices for all True values from the selection array
            all_points_projected =  np.vstack((all_points_projected, obj.points[obj.point_visibility]))


#make arrays of just the  z values, index 2 in the point arrays array
projectedZArray = all_points_projected[:, 2]
zArray = all_points[:, 2]

zDiffArray = projectedZArray - zArray

zDiffAvg = np.mean(zDiffArray, axis=0)
stdDev = np.std(zDiffArray)

if -0.1 <= zDiffAvg <= 0.1 and stdDev < 0.1:
    write_report("QA Status", "QA Passed. Avg: " + str(round(zDiffAvg, 3)) + "   StdDev: " + str(round(stdDev, 3)))
else:
    write_report("QA Status", "QA Failed. Avg: " + str(round(zDiffAvg, 3)) + "   StdDev: " + str(round(stdDev, 3)))


#print(zDiffAvg)
#make an array of x, y, z, projected z
combinedArray = np.column_stack((all_points, projectedZArray, zDiffArray))



filepath = parser["outputFolder"]
write_report("outputFolder", filepath)

filepath = filepath.replace('\\\\', '\\')
  
save_as = filepath + "\\" + CSVName
tk.messagebox.showinfo("Info", f"QA CSV will be saved as: {save_as}")
if len(combinedArray) > 0:
    #print("Writing {} points to {}".format(len(all_points), save_as))
    if os.path.exists(save_as):
        os.remove(save_as)
    # https://laspy.readthedocs.io/en/latest/tut_background.html

    np.savetxt(save_as, combinedArray, delimiter=',', fmt='%f')

with open(save_as, 'a', newline='') as csvfile:
    # Create a CSV writer object
    csv_writer = csv.writer(csvfile)


    # Write the data to the CSV file
    csv_writer.writerow(["Avg"])
    csv_writer.writerow([zDiffAvg])
    csv_writer.writerow(["StdDev"])
    csv_writer.writerow([stdDev])








