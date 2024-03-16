#Generic pointcloud creation using Agisoft, by Breaden King 19/01/24
#input taken: A single folder called the flight name in  D:\AGI IMPORTS' (only one fodler allowed in D:\AGI IMPORTS' currently)
#inside the folder there should be a  topo.csv (format: point ID, x, y, z), the camera calibration .XML, and the photos to be used. Photos in subfolders are ok.

import Metashape
import os, sys, time


def get_subfolder_name(directory):
    subfolders = [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]
    
    if len(subfolders) == 1:
        return subfolders[0]
    elif len(subfolders) > 1:
        raise ValueError(f"Error: More than one subfolder found in {directory}")
    else:
        raise ValueError(f"Error: No subfolders found in {directory}")


def progress_print(p):
        print('Current task progress: {:.2f}%'.format(p))


#Iterate through all subfolders of folder and return all files of type
def find_files(folder, types):
    file_paths = []
    for root, dirs, files in os.walk(folder):
        if 'processed' in dirs:
            dirs.remove('Processed')

        for entry in files:
            if os.path.splitext(entry)[1].lower() in types:
                file_paths.append(os.path.join(root, entry))
    return file_paths

def doPhotogrammetry(gcpFlag, input_directory, export_directory): 

    if gcpFlag is not None and isinstance(gcpFlag, str):
        print("GCP Flag is on.")
    else:
        print("GCP flag is off")


    # Checking compatibility with Agisoft
    compatible_major_version = "2.0"
    found_major_version = ".".join(Metashape.app.version.split('.')[:2])
    if found_major_version != compatible_major_version:
        raise Exception("Incompatible Metashape version: {} != {}".format(found_major_version, compatible_major_version))





    #get the name of the single project folder allowed in D:\AGI IMPORTS'
    try:
        projectName = get_subfolder_name(input_directory)
        print(f"Project name: {projectName}")
    except FileNotFoundError as e:
        print("Import folder not found. Looking for: " + input_directory)
        input()
        exit()


    #get the names of the input and export folders to be used based on the projectName derived from the input folder
    try:
        image_folder = os.path.join(input_directory, projectName)
        output_folder = os.path.join(image_folder, "Processed")
    except NameError as e:
        print("Import or Export folder not found. D:\AGI IMPORTS and D:\AGISOFT EXPORTS.")
        input()
        exit()



    cameraCalibration = find_files(image_folder, [".xml"])


    photos = find_files(image_folder, [".jpg", ".jpeg", ".tif", ".tiff"])

    if not photos:
        print("No photos found in input directory. Exiting")
        input()
        exit()

    doc = Metashape.Document()


    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    try:
        doc.save(output_folder + '/' + projectName + '.psx')
    except:
        print("Unable to save project to export directory, do you have the project open?")
        input()


    chunk = doc.addChunk()


    chunk.addPhotos(photos)

    
    try:
        doc.save()
    except:
        print("Unable to save project to export directory.")

    Metashape.CoordinateSystem.addGeoid(input_directory + "\\AUSGeoid09.tif" )

    coordinateSystem = "COMPD_CS[\"CCMP + Geoid09\",PROJCS[\"GDA94 / MGA zone 55\",GEOGCS[\"GDA94\",DATUM[\"Geocentric Datum of Australia 1994\",SPHEROID[\"GRS 1980\",6378137,298.257222101,AUTHORITY[\"EPSG\",\"7019\"]],TOWGS84[0,0,0,0,0,0,0],AUTHORITY[\"EPSG\",\"6283\"]],PRIMEM[\"Greenwich\",0,AUTHORITY[\"EPSG\",\"8901\"]],UNIT[\"degree\",0.01745329251994328,AUTHORITY[\"EPSG\",\"9102\"]],AUTHORITY[\"EPSG\",\"4283\"]],PROJECTION[\"Transverse_Mercator\",AUTHORITY[\"EPSG\",\"9807\"]],PARAMETER[\"latitude_of_origin\",0],PARAMETER[\"central_meridian\",147],PARAMETER[\"scale_factor\",0.9996],PARAMETER[\"false_easting\",500000],PARAMETER[\"false_northing\",10000000],UNIT[\"metre\",1,AUTHORITY[\"EPSG\",\"9001\"]],AUTHORITY[\"EPSG\",\"28355\"]],VERT_CS[\"AHD height\",VERT_DATUM[\"Australian Height Datum\",2005,AUTHORITY[\"EPSG\",\"5111\"]],UNIT[\"metre\",1,AUTHORITY[\"EPSG\",\"9001\"]],AUTHORITY[\"EPSG\",\"5711\"]]]"




    #load camera calibration .xml from image_folder
    try:
        my_sensor = chunk.sensors[0]
        my_sensor.type = Metashape.Sensor.Type.Frame
        my_calib = Metashape.Calibration()
        my_calib.width = my_sensor.width
        my_calib.height = my_sensor.height
        my_calib.load(str(cameraCalibration[0]), format=Metashape.CalibrationFormatXML)
        my_sensor.user_calib = my_calib
    except IndexError as e:
            print("Problem loading camera calibration .xml from project folder, press enter to continue anyway")
            input()

    #load the calibrated sensor to be used with each camera (image) / pulls accuracy data from the photos imported. 
    for camera in chunk.cameras:
        camera.sensor = my_sensor
        camera.reference.location_accuracy = Metashape.Vector((float(camera.photo.meta['DJI/RtkStdLon']),float(camera.photo.meta['DJI/RtkStdLat']),float(camera.photo.meta['DJI/RtkStdHgt'])))
        print(camera)



    try:
        doc.save()
    except:
        print("Unable to save project to export directory.")

    # downscale=0 is highest accuracy
    chunk.matchPhotos(progress = progress_print, keypoint_limit = 70000, tiepoint_limit = 7000, downscale=0, generic_preselection = True, reference_preselection = True, reference_preselection_mode=Metashape.ReferencePreselectionSource, filter_mask=False, filter_stationary_points=True, keypoint_limit_per_mpx=1000, guided_matching=False,   )

    try:
        doc.save()
    except:
        print("Unable to save project to export directory.")

    chunk.alignCameras(progress = progress_print, adaptive_fitting = False, reset_alignment = False)

    try:
        doc.save()
    except:
        print("Unable to save project to export directory.")

    ##Do GCP here. Doesnt work yet
    if gcpFlag:
        print("Attempting to import GCP from: " + gcpFlag)
        chunk.importReference(gcpFlag, delimiter=",", columns="nxyz")
        try:
            doc.save()
        except:
            print("Unable to save project to export directory.")
        input("Leave this paused here. Open the Agisoft project and check GCP's loaded. Line up GCP's on pictures. Save project. Close Agisoft. Press Enter")



    chunk.buildDepthMaps(progress = progress_print, downscale = 8, filter_mode = Metashape.NoFiltering)

    chunk.buildPointCloud(progress = progress_print, source_data=Metashape.DepthMapsData, point_colors=True, point_confidence=False,
    keep_depth=True, uniform_sampling=True, points_spacing=0.05)


    try:
        doc.save()
    except:
        print("Unable to save project to export directory.")


    #chunk.crs = Metashape.CoordinateSystem(coordinateSystem)
    #chunk.updateTransform()



    if chunk.point_cloud:
        chunk.exportPointCloud(output_folder + '/' + projectName + '.laz', crs = Metashape.CoordinateSystem(coordinateSystem), format = Metashape.PointCloudFormatLAZ, source_data = Metashape.PointCloudData)

    #check for .laz output
    if os.path.isfile(output_folder + "\\" + projectName +".laz"):
        print("Pointcloud has been exported to: " + output_folder + "\\" + projectName + ".laz")
    else:
        print("Something went wrong. No Pointcloud for you!")



    chunk.buildDem(source_data=Metashape.PointCloudData)

    try:
        doc.save()
    except:
        print("Unable to save project to export directory.")

#setting coordinate system for the image exports 
    d_projection = Metashape.OrthoProjection()
    d_projection.crs = Metashape.CoordinateSystem(coordinateSystem)


    if chunk.elevation:
        chunk.exportRaster(output_folder + '/' + projectName + ' DEM.tif', source_data = Metashape.ElevationData,projection = d_projection)


    chunk.buildOrthomosaic(progress = progress_print, surface_data=Metashape.ElevationData, blending_mode=Metashape.MosaicBlending, resolution=0.1)

    try:
        doc.save()
    except:
        print("Unable to save project to export directory. Press enter to continue.")
        input()

    chunk.exportRaster(output_folder + '/' + projectName + ' 10cm.tiff', projection = d_projection, source_data = Metashape.OrthomosaicData)
    chunk.exportRaster(output_folder + '/' + projectName + ' 10cm.jpg', source_data = Metashape.OrthomosaicData, projection = d_projection,  resolution=0.1, save_world=True)
    chunk.exportRaster("V:/11 - Vulcan/06_Survey/02 Site Imagery/2024/" + projectName + ' 50cm.jpg', source_data = Metashape.OrthomosaicData, projection = d_projection, resolution=0.5, save_world=True) 



    chunk.exportReport(output_folder + '/' + projectName + '.pdf')

    try:
        doc.save()
    except:
        print("Unable to save project to export directory. Press enter to continue.")
        input()



    return str(output_folder + "\\" + projectName +".laz")