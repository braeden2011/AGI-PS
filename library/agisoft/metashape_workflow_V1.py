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
        if 'Exports' in dirs:
            dirs.remove('Exports')

        for entry in files:
            if os.path.splitext(entry)[1].lower() in types:
                file_paths.append(os.path.join(root, entry))
    return file_paths



def doPhotogrammetry(gcp_csv, projectName, input_directory, export_directory, camera_cal): 


    # fix to work with gcp_csv (a path from gui)
    if gcp_csv is False:
        print("GCP Flag is off.")
    else:
        print("GCP flag is on. Using GCPs from: " + gcp_csv)


    # Checking compatibility with Agisoft
    compatible_major_version = "2.1"
    found_major_version = ".".join(Metashape.app.version.split('.')[:2])
    if found_major_version != compatible_major_version:
        raise Exception("Incompatible Metashape version: {} != {}".format(found_major_version, compatible_major_version))






    #changed to suing file specified in gui instead of finding the .xml in input_directory / project_folder
    #cameraCalibration = find_files(input_directory, [".xml"])
    camera_cal


    photos = find_files(input_directory, [".jpg", ".jpeg", ".tif", ".tiff"])

    if not photos:
        print("No photos found in input directory. Exiting")
        input()
        exit()

    doc = Metashape.Document()


    if not os.path.exists(export_directory):
        os.makedirs(export_directory)

    try:
        doc.save(input_directory + '/' + projectName + '.psx')
    except:
        print("Unable to save project to export directory, do you have the project open?")
        input()


    chunk = doc.addChunk()


    chunk.addPhotos(photos)

    
    try:
        doc.save()
    except:
        print("Unable to save project to export directory.")


    Metashape.CoordinateSystem.addGeoid("C:\Program Files\Agisoft\Metashape Pro\geoids\AUSGeoid09.tif" )

    coordinateSystem = "COMPD_CS[\"CCMP + Geoid09\",PROJCS[\"GDA94 / MGA zone 55\",GEOGCS[\"GDA94\",DATUM[\"Geocentric Datum of Australia 1994\",SPHEROID[\"GRS 1980\",6378137,298.257222101,AUTHORITY[\"EPSG\",\"7019\"]],TOWGS84[0,0,0,0,0,0,0],AUTHORITY[\"EPSG\",\"6283\"]],PRIMEM[\"Greenwich\",0,AUTHORITY[\"EPSG\",\"8901\"]],UNIT[\"degree\",0.01745329251994328,AUTHORITY[\"EPSG\",\"9102\"]],AUTHORITY[\"EPSG\",\"4283\"]],PROJECTION[\"Transverse_Mercator\",AUTHORITY[\"EPSG\",\"9807\"]],PARAMETER[\"latitude_of_origin\",0],PARAMETER[\"central_meridian\",147],PARAMETER[\"scale_factor\",0.9996],PARAMETER[\"false_easting\",500000],PARAMETER[\"false_northing\",10000000],UNIT[\"metre\",1,AUTHORITY[\"EPSG\",\"9001\"]],AUTHORITY[\"EPSG\",\"28355\"]],VERT_CS[\"AHD height\",VERT_DATUM[\"Australian Height Datum\",2005,AUTHORITY[\"EPSG\",\"5111\"]],UNIT[\"metre\",1,AUTHORITY[\"EPSG\",\"9001\"]],AUTHORITY[\"EPSG\",\"5711\"]]]"



    if camera_cal:
    #load camera calibration .xml from image_folder
        try:
            my_sensor = chunk.sensors[0]
            my_sensor.type = Metashape.Sensor.Type.Frame
            my_calib = Metashape.Calibration()
            my_calib.width = my_sensor.width
            my_calib.height = my_sensor.height
            my_calib.load(str(camera_cal), format=Metashape.CalibrationFormatXML)
            my_sensor.user_calib = my_calib
        except IndexError as e:
                print("Problem loading camera calibration .xml from project folder, press enter to continue anyway")
                input()
    else:
        print("No camera cal loaded. Proceeding without")

    #load the calibrated sensor to be used with each camera (image) / pulls accuracy data from the photos imported. 
    for camera in chunk.cameras:
        if camera_cal:
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

    ##??changed to using gcp_csv (a path from the gui, does it work with the if, and the chunk.importReference?)
    #If using GCP import them, close the project, allow manual selection of GCP in images using the Agisoft program, re-open the project in python
    if gcp_csv:
        print("Attempting to import GCP from: " + gcp_csv)
        chunk.importReference(gcp_csv, delimiter=",", columns="nxyz")
        try:
            doc.save()
        except:
            print("Unable to save project to export directory.")


        doc.close()
        input("Leave this paused here. Open the Agisoft project and check GCP's loaded. Line up GCP's on pictures. Save project. Close Agisoft. Press Enter")
        input("Are you sure you finished selecting the GCPs and CLOSED the project again?")
        try:
            doc.open(input_directory + "/" + projectName + ".psx")
        except:
            print("Unable to open the project after GCPs were selected.")
        



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
        chunk.exportPointCloud(export_directory + '/' + projectName + '.laz', crs = Metashape.CoordinateSystem(coordinateSystem), format = Metashape.PointCloudFormatLAZ, source_data = Metashape.PointCloudData)

    #check for .laz output
    if os.path.isfile(export_directory + "\\" + projectName +".laz"):
        print("Pointcloud has been exported to: " + export_directory + "\\" + projectName + ".laz")
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
        chunk.exportRaster(export_directory + '/' + projectName + ' DEM.tif', source_data = Metashape.ElevationData,projection = d_projection)


    chunk.buildOrthomosaic(progress = progress_print, surface_data=Metashape.ElevationData, blending_mode=Metashape.MosaicBlending, resolution=0.1)

    try:
        doc.save()
    except:
        print("Unable to save project to export directory. Press enter to continue.")
        input()

    chunk.exportRaster(export_directory + '/' + projectName + ' 10cm.tiff', projection = d_projection, source_data = Metashape.OrthomosaicData)
    chunk.exportRaster(export_directory + '/' + projectName + ' 10cm.jpg', source_data = Metashape.OrthomosaicData, projection = d_projection,  resolution=0.1, save_world=True)
    chunk.exportRaster("V:/11 - Vulcan/06_Survey/02 Site Imagery/2024/" + projectName + ' 50cm.jpg', source_data = Metashape.OrthomosaicData, projection = d_projection, resolution=0.5, save_world=True) 



    chunk.exportReport(export_directory + '/' + projectName + '.pdf')

    try:
        doc.save()
    except:
        print("Unable to save project to export directory. Press enter to continue.")
        input()



    return str(export_directory + "\\" + projectName +".laz")