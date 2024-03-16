import os
import numpy as np
import laspy
from mapteksdk.project import Project
from mapteksdk.data import PointSet



def importLaz(project, las_file_path, pointcloud_Path):
    las = laspy.read(las_file_path)

    las_points = np.column_stack((las.x, las.y, las.z))



    # Read colour data and prepare it for storing:
    # If the colours have been stored in 16 bit, we'll need to get the first 8 bits for a proper value
    colours_are_16bit = np.max(las.red) > 255
    red = np.right_shift(las.red, 8).astype(np.uint8) if colours_are_16bit else las.red
    green = np.right_shift(las.green, 8).astype(np.uint8) if colours_are_16bit else las.green
    blue = np.right_shift(las.blue, 8).astype(np.uint8) if colours_are_16bit else las.blue
    # Create rgba array
    las_colours = np.column_stack((red, green, blue))

    
    #get the name / location for the Pointstudio object, strip file extension
    #import_as = pointcloud_Path + format(os.path.basename(las_file_path))
    import_as = f"{pointcloud_Path}{os.path.splitext(os.path.basename(las_file_path))[0]}"

    # Create PointSet object and populate data
    with project.new(import_as, PointSet, overwrite=True) as points:
        points.points, points.point_colours = (las_points, las_colours)


##Example

#project = Project()
#las_file = r"N:\00 - RAW DATA\2312 - December\UAV Survey\231223 0719 ROM 2\231223 0719 ROM 2.laz"
#pointcloud_Path = "scans/"

#importLaz(project, las_file, pointcloud_Path) 
