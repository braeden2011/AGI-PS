#Braeden King 16/02/24
#Step one of create asbuilt: 
#Orders list of surfaces in new surfaces folder based on YYMMDD HHMM at start of surface names. (can we order the objects in the database?)
#For each new surface creates boundary poly


import os

from mapteksdk.pointstudio.operations import *
from mapteksdk.project import *
from mapteksdk.data import *

from mapteksdk.workflows import WorkflowArgumentParser, WorkflowSelection

#from mapteksdk.data import PointSet
from numpy import genfromtxt

parser = WorkflowArgumentParser(description="Create BDY polys for cropping")


parser.declare_output_connector("newSurfaceList", WorkflowSelection,
                                connector_name="newSurfaceList",
                                description="newSurfaceList")

parser.declare_output_connector("newSurfaceListStr", str,
                                connector_name="newSurfaceListStr",
                                description="newSurfaceListStr")
 
parser.parse_arguments()
project = Project()
newSurfacesPath = "working/NEW ASBUILT/new surfaces/"


newSurfaceList = project.get_children(newSurfacesPath).names()

# Sort based on YYMMDD and HHMM, oldest fisrt
sorted_list = sorted(newSurfaceList, key=lambda x: (x[:6], x[7:11]))  
#prefix each surface in the list with the folder name its in to pass to PS
sorted_list = [newSurfacesPath + entry for entry in sorted_list]
sorted_list_str = ",".join(sorted_list)

parser.set_output("newSurfaceList", sorted_list)
parser.set_output("newSurfaceListStr", sorted_list_str)

