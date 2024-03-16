##Write QA CSV
from mapteksdk.workflows import WorkflowArgumentParser, WorkflowSelection
from mapteksdk.project import Project
from mapteksdk.pointstudio.operations import *
from mapteksdk.data import PointSet
from numpy import genfromtxt
import os
import numpy as np
import csv




parser = WorkflowArgumentParser(description="Write pointSet to csv")

#Input for Topo pointSet
parser.declare_input_connector("input1", WorkflowSelection,
                               connector_name="input1",
                               description="input1")

#Input for projected to surface Topo pointSet
parser.declare_input_connector("input2", WorkflowSelection,
                               connector_name="input2",
                               description="input2")



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
            #all_colours = np.vstack((all_colours, obj.point_colours[obj.point_visibility]))

            try:
                #move the topo out of new topo folder
                project.rename_object(oid.path, "scrapbook/" + str(oid.name))
            except:
                write_report("File Already Exists", "Can't move "  + str(oid.name) + " from working/new topo/ to scrapbook." )

for oid in parser["input2"]:
    with project.read(oid) as obj:
        if hasattr(obj, 'points'):
            # Append visible points from obj to buffer object
            # Use .point_selection to get indices for all True values from the selection array
            all_points_projected =  np.vstack((all_points_projected, obj.points[obj.point_visibility]))
            #all_colours = np.vstack((all_colours, obj.point_colours[obj.point_visibility]))


            try:
                #move the topo out of new topo folder
                project.rename_object(oid.path, "scrapbook/" + str(oid.name))

            except:
                write_report("File Already Exists", "Can't move "  + str(oid.name) + " from working/new topo/ to scrapbook." )

#exportDir = os.path.join(r"D:\AGISOFT EXPORTS" + oid.name)
exportDir = "D:/AGI IMPORTS/"


save_as = os.path.join(exportDir, projectName + "/Processed/", CSVName)

if not os.path.exists(os.path.join(exportDir, projectName, "Processed")):
    os.makedirs(os.path.join(exportDir, projectName, "Processed"))
write_report("Save CSV as ", save_as)

#make arrays of just the  z values, index 2 in the point arrays array
projectedZArray = all_points_projected[:, 2]
zArray = all_points[:, 2]

zDiffArray = projectedZArray - zArray

zDiffAvg = np.mean(zDiffArray, axis=0)
stdDev = np.std(zDiffArray)

#print(zDiffAvg)
#make an array of x, y, z, projected z
combinedArray = np.column_stack((all_points, projectedZArray, zDiffArray))

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

if -0.1 <= zDiffAvg <= 0.1 and stdDev < 0.1:
    write_report("QA Status", "QA Passed. Avg: " + str(round(zDiffAvg, 3)) + "   StdDev: " + str(round(stdDev, 3)) + "\n Report written to: " + repr(save_as))
else:
    write_report("QA Status", "QA Failed. Avg: " + str(round(zDiffAvg, 3)) + "   StdDev: " + str(round(stdDev, 3)) + "\n Report written to: " + repr(save_as))
