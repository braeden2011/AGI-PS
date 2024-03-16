#Braeden King 16/02/24
#Step three of create asbuilt:
#Accepts iterator of the current PS workflow loop and the list of newSurfaces as inputs
#Uses iterator to identify which list item has just had its polygon crop done, then copies points of the corrosponding surface into AS-BUILT POINTS

from mapteksdk.pointstudio.operations import *
from mapteksdk.project import *
from mapteksdk.data import *

from mapteksdk.workflows import WorkflowArgumentParser, WorkflowSelection

#from mapteksdk.data import PointSet
from numpy import genfromtxt

parser = WorkflowArgumentParser(description="copy points from surface")



parser.declare_input_connector("iterator", str,
                                connector_name="iterator",
                                description="iterator")

parser.parse_arguments()
project = Project() # Connect to default project

currentObj = parser["iterator"]

#takes the path of the PS object (in this case the cropping poly) and splits by /, then selects the last segment (the actual object name, same name as the surface)
splitNewSurfaceName = currentObj.split('/')
surfaceName = splitNewSurfaceName[-1]


# Where you stored the surface:
path = "working/NEW ASBUILT/new surfaces/" + surfaceName
output = "working/NEW ASBUILT/AS-BUILT POINTS/" + surfaceName + " PTS"
found = project.find_object(path)
if found and found.is_a(Surface):
    with project.read(path) as surface:
        with project.new(output, PointSet, overwrite=True) as points:
            points.points, points.point_colours = surface.points, surface.point_colours
else:
    print("Surface not found to copy points from")