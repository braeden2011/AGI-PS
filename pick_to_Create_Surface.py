#Braeden King 13/12/23
# 1m Topo filter applied to scan selected in view window. Surface created, despiked, 0.025m simplification, "topo of " stripped off surface name.


from mapteksdk.pointstudio.operations import *
from mapteksdk.project import *
from mapteksdk.data import *

 
project = Project()
 
inputScan = object_pick()
 
inputScanPath = inputScan.path
inputScanName = inputScan.name
inputScanType_name = inputScan.type_name
inputScanList = [inputScan] 


filter_topography(inputScanPath, 1, keep_lower_points=True, filter_combination=MaskOperation.AND, treat_scans_separately=False)
topographic_triangulation(inputScan, trim_edges_to_maximum_length=10.0, output_option=TriangulationOutput.SINGLE_SURFACE, relimit_to_polygon=None, edge_constraints=None, destination="surfaces/" + inputScanName)



triangulationPath = "surfaces/" + inputScanName
triangulation = project.find_object(triangulationPath)


despike(triangulation.path)
simplify_by_distance_error(triangulation.path, 0.06, preserve_boundary_edges=False, avoid_intersections=True)


#strip topo of text from surface name
#stripping the t off of PIT ?
#newName = triangulation.name.strip("topo of ")
#project.rename_object(triangulation, newName, overwrite=False)
#write_report("new triangulation name is:", f" {triangulation.name}")
