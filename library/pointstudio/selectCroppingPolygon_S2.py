#Braeden King 23/12/23
#Process and QA new pickup. 
#Step 2 select surface bdy for polygon crop of topo points and output back to workflow

import os

from mapteksdk.pointstudio.operations import *
from mapteksdk.project import *
from mapteksdk.data import *

from mapteksdk.workflows import WorkflowArgumentParser, WorkflowSelection

#from mapteksdk.data import PointSet
from numpy import genfromtxt

parser = WorkflowArgumentParser(description="Filter to desired cropping bdy")


# parser.declare_input_connector("input", WorkflowSelection,
#                                connector_name="input",
#                                description="input")

parser.declare_output_connector("polygon", WorkflowSelection,
                                connector_name="Output1",
                                description="polygon")
 
parser.parse_arguments()

project = Project()

newPickupPath = "working/new pickup/"
project.delete("working/cropping poly/croppingPoly")
project.delete("cad/offset of croppingPoly")



for name in project.get_children(newPickupPath).names():

    inputScan = project.find_object(newPickupPath + name)
    newScanName = inputScan.path.split("/")[-1]

    try:
        #move the scan out of new pickup folder
        project.rename_object(inputScan.path, "scans/" + str(name))
    except:
        write_report("File Already Exists", "Can't move "  + newScanName + " from working/new pickup/ to scans." )

bdyPolygonPath = "cad/boundary of " + newScanName

boundaryPolygon = project.find_object(bdyPolygonPath)



#if boundaryPolygon.type_name == "Polygon":
if boundaryPolygon:

    write_report("path to created bdy", boundaryPolygon.path)
    project.rename_object(boundaryPolygon.path, "working/cropping poly/croppingPoly")

else:
    croppingBdyPath = "cad/boundaries of " + newScanName + "/boundary 1"
    write_report("filtered bdy path", croppingBdyPath)
    project.rename_object(croppingBdyPath, "working/cropping poly/croppingPoly")
    project.delete("cad/boundaries of " + newScanName)


bdyToOffset = project.find_object("working/cropping poly/croppingPoly")

write_report("path to cropping bdy", bdyToOffset.path)
parser.set_output("output", [bdyToOffset])