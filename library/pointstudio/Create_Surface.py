#Braeden King 23/12/23
# Generic surface creation, keep lower points, returns the surface object. Read example usage notes at bottom


from mapteksdk.pointstudio.operations import *
from mapteksdk.project import *
from mapteksdk.data import *

 

 

def create_surface(project, inputPointsPath, topoFilterMetres, outputPath, trimEdgesMetres, simplificationMetres):

    inputPoints = project.find_object(inputPointsPath)


    filter_topography(inputPointsPath, topoFilterMetres, keep_lower_points=True, filter_combination=MaskOperation.AND, treat_scans_separately=False)
    topographic_triangulation(inputPointsPath, trim_edges_to_maximum_length=trimEdgesMetres, output_option=TriangulationOutput.SINGLE_SURFACE, relimit_to_polygon=None, edge_constraints=None, destination= outputPath + inputPoints.name)



    triangulationPath = outputPath + inputPoints.name
    triangulation = project.find_object(triangulationPath)


    despike(triangulation.path)
    simplify_by_distance_error(triangulation.path, simplificationMetres, preserve_boundary_edges=False, avoid_intersections=True)

    return triangulation


##Required edit to: C:\Users\****USER****\AppData\Roaming\Python\Python311\site-packages\mapteksdk\pointstudio\operations.py

#Original code below was throwing     TypeError: can only concatenate str (not "list") to str ON scans + (edge_constraints or []))), 

 # inputs = [
 #   ('selection',
 #    RequestTransactionWithInputs.format_selection(
 #      scans + (edge_constraints or []))),
 # ]


 #edited version below works to just take scans list as input, no edge contraints or []

#   inputs = [
#     ('selection',
#      RequestTransactionWithInputs.format_selection(
#        scans## + (edge_constraints or [])
#        )),
#   ]

##Example usage
""" 
project = Project()
inputPointsPath = "scrapbook/working/new scan/EX02"
topoFilterMetres = 10
outputPath = "scrapbook/working/new surface/"
trimEdgesMetres = 25
simplificationMetres = 0.025

create_surface(project, inputPointsPath, topoFilterMetres, outputPath, trimEdgesMetres, simplificationMetres) """
