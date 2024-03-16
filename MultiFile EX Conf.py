#Braeden King 23/12/23
#Creates surfaces for each EX (10m topo, despiked, 0.025 simp) from Titan Analytics- On Demand – Advanced Analytics’ > Titan 3330 > Production > [BETA] [Titan 3330] Cycle Data Tables (v1.0.1). "BUCKET CYCLE GPS DATA" Tab csv downloads in users downloads folder called: TitanV1.csv and TitanV2.csv
#new surfaces created in /working/titan/surfaces/
#colours surfaces by distance (Using Pit conformance tolerences and colour legend) to /working/current supplylines/* (must be a single tri file in this folder)


import os
from library.splitCSVWithHeaders import split_and_write_csv
from library.pointstudio.Create_Surface import create_surface
#from library.pointstudio.importlaz import importLaz

from mapteksdk.pointstudio.operations import *
from mapteksdk.project import *
from mapteksdk.data import *

from mapteksdk.project import Project
from mapteksdk.data import PointSet
from numpy import genfromtxt

project = Project()



#Splits both titan (V1 and V2) csv exports (if they exist) in current users downloads folder to individual EX files in 'C:\temp'
try: 
    input_csv_V1 = os.path.join(os.path.expanduser("~"), "Downloads", "TitanV1.csv")
    input_csv_V2 = os.path.join(os.path.expanduser("~"), "Downloads", "TitanV2.csv")

    titanCSVFolder = r'C:\temp\titan'
    column_to_split = 'Machine Name'
    columns_to_write = ['Tooth Start Fill E', 'Tooth Start Fill N', 'Tooth Start Fill Alt']

    #empty the titanCSVFolder of old csv's
    old_csv = os.listdir(titanCSVFolder)
    csv_files = [file for file in old_csv if file.lower().endswith('.csv')]
    for csv_file in csv_files:
        try:
            file_path = os.path.join(titanCSVFolder, csv_file)
            os.remove(file_path)
            print(f"Deleted: {file_path}")
        except Exception as err:
            print(f"Error deleting {csv_file}: {err}")


    split_and_write_csv(input_csv_V1, titanCSVFolder, column_to_split, columns_to_write)
    split_and_write_csv(input_csv_V2, titanCSVFolder, column_to_split, columns_to_write)

except FileNotFoundError as e:
    print(f"Error: {e}")
except Exception as e:
    # Handle other exceptions
    print(f"An unexpected error occurred: {e}")



#Set path in Pointstudio for titan point data csv import
newTitanPointsPath = "working/titan/point data/"

#Reads each split "EX**.csv" into Pointstudio working folder as a new scan, first 3 columns imported only
# Iterate over each EX's CSV file in the titanCSVFolder
for filename in os.listdir(titanCSVFolder):
    if filename.endswith(".csv"):
        file_path = os.path.join(titanCSVFolder, filename)
        file_name = os.path.splitext(filename)[0]  # Extract file name without extension
        
        point_path = newTitanPointsPath + file_name

        with project.new(point_path, PointSet, overwrite=True) as points:
            # Use numpy.getfromtxt to read the csv
            csv_data = genfromtxt(file_path, delimiter=',')
            # Extract columns x,y,z=0,1,2 (0:3) from csv_data and assign to points:
            points.points = csv_data[0:, 0:3]
        


#Makes surfaces out of all of the EX PointSets in scrapbook/working/new scan and colours by distance from surface in /working/current supplylines/
#colour by distance legend to use
legend = project.find_object("legends/PIT CONFORMANCE 2306")
print("legend name: " + legend.name)




newTitanSurfacesPath = "working/titan/surfaces/"
topoFilterMetres = 10
trimEdgesMetres = 25
simplificationMetres = 0.025


for name in project.get_children(newTitanPointsPath).names():

    print("input scan name: {}".format(name))

    inputScan = project.find_object(newTitanPointsPath + name)
    inputScanPath = inputScan.path

    print("input scan path: " + inputScan.path)

    titanTriangulation = create_surface(project, inputScanPath, topoFilterMetres, newTitanSurfacesPath, trimEdgesMetres, simplificationMetres)


#Colours by distance from triangulation in "working/current supplylines/" THIS MUST BE A SINGLE FILE, or it will overwrite the colour by distance command for each previous file.

    for name in project.get_children("working/current supplylines/").names():
        colour_by_distance_from_object(titanTriangulation, "working/current supplylines/" + name, 1, 2, legend)
    
    #Display coloured by dist surfaces in the selected view
        #select active view window to open the coloured by distance surfaces in
    view = active_view_or_new_view() 
    view.add_objects([titanTriangulation])


