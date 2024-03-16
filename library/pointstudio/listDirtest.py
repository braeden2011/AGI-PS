
import os
#from library.splitCSVWithHeaders import split_and_write_csv
#from library.pointstudio.importlaz import importLaz

from mapteksdk.pointstudio.operations import *
from mapteksdk.project import *
from mapteksdk.data import *

from mapteksdk.workflows import WorkflowArgumentParser, WorkflowSelection


project = Project()

#Set path in Pointstudio of new pickup . laz and topo csv
newPickupPath = "working/test"

for name in project.get_children(newPickupPath).names():
    write_report("Project Folder path: ", name)