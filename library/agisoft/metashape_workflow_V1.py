#Generic pointcloud creation using Agisoft, by Breaden King 19/01/24
#inputs(file / folder paths): gcp_csv, input_directory, export_directory, camera_cal
#inputs cont.: projectName
#inside the input_directory there should be .jpgs to process, in subfolders is ok.

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


#Iterate through all subfolders of folder and return all files of types
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

    if gcp_csv is False:
        print("GCP Flag is off.")
    else:
        print("GCP flag is on. Using GCPs from: " + gcp_csv)


    # Checking compatibility with Agisoft
    compatible_major_version = "2.1"
    found_major_version = ".".join(Metashape.app.version.split('.')[:2])
    if found_major_version != compatible_major_version:
        raise Exception("Incompatible Metashape version: {} != {}".format(found_major_version, compatible_major_version))






    #changed to using file specified in gui instead of finding the .xml in input_directory / project_folder
    #cameraCalibration = find_files(input_directory, [".xml"])


    photos = find_files(input_directory, [".jpg"])

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
    #I should maaaybe do 
    #coordinateSystem = Metashape.CoordinateSystem("COMPD_CS[\"CCMP + Geoid09\",PROJCS[\"GDA94 / MGA zone 55\",GEOGCS[\"GDA94\",DATUM[\"Geocentric Datum of Australia 1994\",SPHEROID[\"GRS 1980\",6378137,298.257222101,AUTHORITY[\"EPSG\",\"7019\"]],TOWGS84[0,0,0,0,0,0,0],AUTHORITY[\"EPSG\",\"6283\"]],PRIMEM[\"Greenwich\",0,AUTHORITY[\"EPSG\",\"8901\"]],UNIT[\"degree\",0.01745329251994328,AUTHORITY[\"EPSG\",\"9102\"]],AUTHORITY[\"EPSG\",\"4283\"]],PROJECTION[\"Transverse_Mercator\",AUTHORITY[\"EPSG\",\"9807\"]],PARAMETER[\"latitude_of_origin\",0],PARAMETER[\"central_meridian\",147],PARAMETER[\"scale_factor\",0.9996],PARAMETER[\"false_easting\",500000],PARAMETER[\"false_northing\",10000000],UNIT[\"metre\",1,AUTHORITY[\"EPSG\",\"9001\"]],AUTHORITY[\"EPSG\",\"28355\"]],VERT_CS[\"AHD height\",VERT_DATUM[\"Australian Height Datum\",2005,AUTHORITY[\"EPSG\",\"5111\"]],UNIT[\"metre\",1,AUTHORITY[\"EPSG\",\"9001\"]],AUTHORITY[\"EPSG\",\"5711\"]]]")
    #then replace crs = Metashape.CoordinateSystem(coordinateSystem)
    #in all the exports etc?
    coordinateSystem = "COMPD_CS[\"CCMP + Geoid09\",PROJCS[\"GDA94 / MGA zone 55\",GEOGCS[\"GDA94\",DATUM[\"Geocentric Datum of Australia 1994\",SPHEROID[\"GRS 1980\",6378137,298.257222101,AUTHORITY[\"EPSG\",\"7019\"]],TOWGS84[0,0,0,0,0,0,0],AUTHORITY[\"EPSG\",\"6283\"]],PRIMEM[\"Greenwich\",0,AUTHORITY[\"EPSG\",\"8901\"]],UNIT[\"degree\",0.01745329251994328,AUTHORITY[\"EPSG\",\"9102\"]],AUTHORITY[\"EPSG\",\"4283\"]],PROJECTION[\"Transverse_Mercator\",AUTHORITY[\"EPSG\",\"9807\"]],PARAMETER[\"latitude_of_origin\",0],PARAMETER[\"central_meridian\",147],PARAMETER[\"scale_factor\",0.9996],PARAMETER[\"false_easting\",500000],PARAMETER[\"false_northing\",10000000],UNIT[\"metre\",1,AUTHORITY[\"EPSG\",\"9001\"]],AUTHORITY[\"EPSG\",\"28355\"]],VERT_CS[\"AHD height\",VERT_DATUM[\"Australian Height Datum\",2005,AUTHORITY[\"EPSG\",\"5111\"]],UNIT[\"metre\",1,AUTHORITY[\"EPSG\",\"9001\"]],AUTHORITY[\"EPSG\",\"5711\"]]]"


    #load camera cal if provided
    if camera_cal:
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

    #load the calibrated sensor to be used with each image if cam cal used
    for camera in chunk.cameras:
        if camera_cal:
            camera.sensor = my_sensor
        #pulls accuracy data for each camera from the photos imported. (residuals)
        ##Needs a try catch 
        camera.reference.location_accuracy = Metashape.Vector((float(camera.photo.meta['DJI/RtkStdLon']),float(camera.photo.meta['DJI/RtkStdLat']),float(camera.photo.meta['DJI/RtkStdHgt'])))




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



    #If using GCP, import them, make project writtable, allow manual selection of GCP in images using the Agisoft program, re-open the project in python
    if gcp_csv:
        print("Attempting to import GCP from: " + gcp_csv)
        #adding crs = Metashape.CoordinateSystem(coordinateSystem) argument causes it to change whole project to GDA94/Z55, we want pics / cameras in WGS84 and markers in GDA94/Z55

        chunk.importReference(gcp_csv, delimiter=",", columns="nxyz", create_markers = True, items = Metashape.ReferenceItemsMarkers)

        #for now, users to open the References pane settings and set themselves before lining up GCP
        #maybe able to use to set marker / GCP coords to GDA94/Z55 while leaving chunk / cameras alone? code from 2018
        #alternatively, set crs argument chunk.importReference to crs = Metashape.CoordinateSystem(coordinateSystem), the set the chunk / cameras back to WGS84 after?
        #change coord system for GCP from chunk.crs(WGS84) to (GDA94/Z55)

        for marker in chunk.markers:
            if marker.reference.location:
                marker.reference.location = Metashape.CoordinateSystem.transform(marker.reference.location, chunk.crs, Metashape.CoordinateSystem(coordinateSystem))

        try:
            doc.save()
        except:
            print("Unable to save project to export directory.")
            
        #to allow editing in GUI / remove the lockfile.
        doc.read_only = False
        doc = Metashape.app.document

        #setting read only off, then ommitting next line? will that let me save again after GCP?
        #this is failing to then open the saved project. all subsequent saves fail.

        input("Leave this paused here. Open the Agisoft project and check GCP's loaded. Line up GCP's on pictures. Save project. Close Agisoft. Press Enter")
        input("Are you sure you finished selecting the GCPs, saved and CLOSED the project again?")

        # #this fails to open. Do I even need to re-open. Can I just save over it? No. still fails to save
        # try:
        #     print("Path im trying to open: " + os.path.join(input_directory, projectName + '.psx'))
        #     doc.open(os.path.join(input_directory, projectName + '.psx'))
        #     input()
        # except:
        #     print("Unable to open the project after GCPs were selected.")

        #Leave the project open in Agisoft after picking GCP until after this next bit runs and saves at least once?
        doc = Metashape.app.document #gets currently opened document in actual Metashape window
        #lets try print(str(doc))
        doc.open(projectName)

        try:
            doc.save()
            print("Saved")
        except:
            print("Unable to save project to export directory.")
        
        input()
        
    if gcp_csv:
        chunk.optimizeCameras(progress = progress_print, fit_f=True, fit_cx=True, fit_cy=True, fit_b1=False, fit_b2=False, fit_k1=True, fit_k2=True, fit_k3=True, fit_k4=False, fit_p1=True, fit_p2=True, fit_corrections=False, adaptive_fitting=True, tiepoint_covariance=False)

    #Do we want to pause here and let peopel check error values?

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