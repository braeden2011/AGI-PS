#Braeden King 23/12/23
#Process and QA new pickup

import os
from library.pointstudio.Create_Surface import create_surface
from mapteksdk.pointstudio.operations import *
from mapteksdk.project import *
from mapteksdk.data import *
from mapteksdk.workflows import WorkflowArgumentParser, WorkflowSelection
from numpy import genfromtxt

parser = WorkflowArgumentParser(description="Process pickup")

parser.declare_output_connector("output1", WorkflowSelection,
                                connector_name="Output1",
                                description="newSurface")

parser.parse_arguments()

project = Project()

newSurfacesPath = "surfaces/"
topoFilterMetres = 1
trimEdgesMetres = 10.0
simplificationMetres = 0.06

newSurface = create_surface(project, inputScanPath, topoFilterMetres, newSurfacesPath, trimEdgesMetres, simplificationMetres)

parser.set_output("output1", [newSurface])

view = active_view_or_new_view() 
view.add_objects([newSurface])