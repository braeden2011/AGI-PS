#Braeden King 16/02/24
#Step two of create asbuilt:
#Accepts string input of list of new surfaces 
#Deals with if the new surface has multiple boundaries created, uses the largest one and names approppriately

import os

from mapteksdk.pointstudio.operations import *
from mapteksdk.project import *
from mapteksdk.data import *

from mapteksdk.workflows import WorkflowArgumentParser, WorkflowSelection

#from mapteksdk.data import PointSet
from numpy import genfromtxt

parser = WorkflowArgumentParser(description="Deal with multiple BDY per surface")

parser.declare_input_connector("input", str,
                                connector_name="input",
                                description="input")

parser.declare_output_connector("croppingPolyList", WorkflowSelection,
                                connector_name="croppingPolyList",
                                description="croppingPolyList")



parser.declare_output_connector("asbuiltPointsFolder", str,
                               connector_name="asbuiltPointsFolder",
                               description="asbuiltPointsFolder")
 
parser.parse_arguments()
project = Project() # Connect to default project

asbuiltPointsFolder = "/working/NEW ASBUILT/AS-BUILT POINTS"

#takes the input from PS parser, strips prefixed and appended ", splits it from a csv string to a python list of object paths
tempString = parser["input"]



tempString = tempString.strip('"')
newSurfaceList = tempString.split(',')

croppingPolyList = []



for entry in newSurfaceList:

    #takes the path of the PS object and splits by /, then selects the last segment (the actual object name)
    splitNewSurfaceName = entry.split('/')
    newSurfaceName = splitNewSurfaceName[-1]


    # try:
    #     #move the scan out of new pickup folder
    #     project.rename_object(inputScan.path, "scans/" + str(name))
    # except:
    #     write_report("File Already Exists", "Can't move "  + newScanName + " from working/new pickup/ to scans." )


    bdyPolygonPath = "cad/boundary of " + str(newSurfaceName)
    boundaryPolygon = project.find_object(bdyPolygonPath)


    if boundaryPolygon:
        project.rename_object(boundaryPolygon.path, "/working/NEW ASBUILT/BDY/" + str(newSurfaceName))

    else:
        croppingBdyPath = "cad/boundaries of " + str(newSurfaceName) + "/boundary 1"
        project.rename_object(croppingBdyPath, "/working/NEW ASBUILT/BDY/" + str(newSurfaceName))
        project.delete("cad/boundaries of " + str(newSurfaceName))

    croppingPolyList.append("/working/NEW ASBUILT/BDY/" + str(newSurfaceName))


    # write_report("path to cropping bdy", bdyToOffset.path)
    # parser.set_output("output", [bdyToOffset])
# for entity in croppingPolyList:
#     print(entity)        

parser.set_output("croppingPolyList", croppingPolyList)
parser.set_output("asbuiltPointsFolder", asbuiltPointsFolder)

