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


parser.declare_input_connector("scanPoints", WorkflowSelection,
                               connector_name="scanPoints",
                               description="scanPoints")

parser.declare_output_connector("polygon", WorkflowSelection,
                                connector_name="Output1",
                                description="polygon")
 
parser.parse_arguments()

project = Project()


project.delete("working/cropping poly/croppingPoly")
project.delete("cad/offset of croppingPoly")



#add an input connector and give it the scan?
for oid in parser["scanPoints"]:
        newScanName = oid.path.split("/")[-1]


bdyPolygonPath = "cad/boundary of " + newScanName


boundaryPolygon = project.find_object(bdyPolygonPath)

#if else to deal with surfaces that have multiple distinct boundaries.
if boundaryPolygon:
    write_report("path to created bdy", boundaryPolygon.path)
else:
    boundaryPolygon = project.find_object("cad/boundaries of " + newScanName + "/boundary 1")
    write_report("filtered bdy path", boundaryPolygon.path)

parser.set_output("polygon", [boundaryPolygon])

