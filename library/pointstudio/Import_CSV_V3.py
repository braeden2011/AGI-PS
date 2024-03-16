
from mapteksdk.data import PointSet
from numpy import genfromtxt
import os

def import_csv(project, csv_file_path, PS_csv_Path):
    file_name_without_extension, _ = os.path.splitext(os.path.basename(csv_file_path))# Extract file name without extension

    point_path = PS_csv_Path + file_name_without_extension + " topo"


    with project.new(point_path, PointSet, overwrite=True) as points:
        # Use numpy.getfromtxt to read the csv
        csv_data = genfromtxt(csv_file_path, delimiter=',')
        # Extract columns x,y,z=0,1,2 (0:3) from csv_data and assign to points:
        points.points = csv_data[0:, 1:4]

