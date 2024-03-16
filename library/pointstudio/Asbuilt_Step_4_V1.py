#Braeden King 23/12/23
#Step four of create asbuilt:
#Create surfaces (one unsimplified, one 0.15m)

from mapteksdk.pointstudio.operations import *
from mapteksdk.project import *
from mapteksdk.data import *

from Create_Surface import create_surface

from mapteksdk.workflows import WorkflowArgumentParser, WorkflowSelection




parser = WorkflowArgumentParser(description="Create asbuilt surface")

parser.declare_input_connector("asbuiltPointsFolder", str,
                                connector_name="asbuiltPointsFolder",
                                description="asbuiltPointsFolder")

parser.declare_input_connector("newSurfaceListStr", str,
                                connector_name="newSurfaceListStr",
                                description="newSurfaceListStr")

parser.parse_arguments()
project = Project() # Connect to default project

asbuiltPointsFolder = parser["asbuiltPointsFolder"]
newSurfaceListStr = parser["newSurfaceListStr"]

#takes the string of new surfacenames and splits by /, then selects the last segment (the most recent pickup name, to extract date/time of the asbuilt from)
splitNewSurfaceName = newSurfaceListStr.split('/')
asbuiltName = splitNewSurfaceName[-1]
asbuiltName = asbuiltName[:6] + " ASBUILT"

newSurfacesPath = "surfaces/"
trimEdgesMetres = 50
simplificationMetres = 0.15




#setup the correct naming and export location for the surface.  may need to pass in the list of new surfaces, then pull the date / time from the most recent. create name from that. another import connector to do.
topographic_triangulation(asbuiltPointsFolder, trim_edges_to_maximum_length=trimEdgesMetres, output_option=TriangulationOutput.SINGLE_SURFACE, relimit_to_polygon=None, edge_constraints=None, destination= newSurfacesPath + asbuiltName)
triangulationPath = newSurfacesPath + asbuiltName
triangulation = project.find_object(triangulationPath)
despike(triangulation.path) 

triangulationSimplified = project.copy_object(triangulation, newSurfacesPath + asbuiltName + " Simplified 0.15m")
#triangulationSimplified = project.find_object(triangulationSimplifiedPath)


simplify_by_distance_error(triangulationSimplified, simplificationMetres, preserve_boundary_edges=False, avoid_intersections=True)

