#Braeden King 23/12/23
#Process and QA new pickup


import os
#from library.splitCSVWithHeaders import split_and_write_csv
from Create_Surface import create_surface
#from library.pointstudio.importlaz import importLaz

from mapteksdk.pointstudio.operations import *
from mapteksdk.project import *
from mapteksdk.data import *

from mapteksdk.workflows import WorkflowArgumentParser, WorkflowSelection

#from mapteksdk.data import PointSet
from numpy import genfromtxt

parser = WorkflowArgumentParser(description="Process pickup")

parser.declare_output_connector("output1", str,
                                connector_name="Output1",
                                description="output1")



 
parser.parse_arguments()

project = Project()

#Set path in Pointstudio of new pickup . laz and topo csv project folders
projectsPath = "working/projects"

projectList = []

for name in project.get_children(projectsPath).names():
    write_report("Project Folder: ", name)
    inputScan = project.find_object(projectsPath + "/" + name + "/" + name)
    write_report("laz path: ", inputScan.path)
    projectList.append(str(inputScan.path))
    write_report("projectList: ", str(projectList))

projectListString = ','.join(projectList)

parser.set_output("output1", [projectList])

write_report("projectListString: ", str(projectListString))


