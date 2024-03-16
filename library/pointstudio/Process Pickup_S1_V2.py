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

parser.declare_output_connector("output1", WorkflowSelection,
                                connector_name="Output1",
                                description="newSurface")

parser.declare_output_connector("output2", WorkflowSelection,
                                connector_name="Output2",
                                description="inputTopo")

 
parser.parse_arguments()

project = Project()

#Set path in Pointstudio of new pickup . laz and topo csv
newPickupPath = "working/new pickup/"
newTopoPath = "working/new topo/"

newSurfacesPath = "surfaces/"
topoFilterMetres = 1
trimEdgesMetres = 10.0
simplificationMetres = 0.06


for name in project.get_children(newPickupPath).names():

    #print("input scan name: {}".format(name))
    inputScan = project.find_object(newPickupPath + name)
    inputScanPath = inputScan.path





for name in project.get_children(newTopoPath).names():
    inputTopo = project.find_object(newTopoPath + name)
    project.rename_object(inputTopo.path, inputScan.name, overwrite=True)
    write_report("topo object path", inputTopo.path)
 


newSurface = create_surface(project, inputScanPath, topoFilterMetres, newSurfacesPath, trimEdgesMetres, simplificationMetres)



    
parser.set_output("output1", [newSurface])
parser.set_output("output2", [inputTopo])


view = active_view_or_new_view() 
view.add_objects([newSurface])