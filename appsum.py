import arcpy # Import arcpy module
from arcpy.sa import *
from flask import Flask, redirect, url_for, render_template
from flask_wtf import FlaskForm
from wtforms import StringField
from flask import request
import random
import json
import time
from geo.Geoserver import Geoserver
from celery import Celery
from flask_celery import make_celery  
from flask_mail import Mail, Message
import shutil
import os

app = Flask(__name__)

# Start - Flaks SMTP configuration settings to send an email to user
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']='winteripcourse'
app.config['MAIL_PASSWORD']='pnmkysaozarmtett'
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True
# End - Flaks SMTP configuration settings to send an email to user

mail = Mail(app)  #Initialize a flask mail application

rootDirectory = "C:\\IPProject\\IPProject_files\\GithubIP\\"   ##### Define root directory #####

# Start - Celery configuration for Asyncronous task execution
app.config['CELERY_BROKER_URL'] = 'amqps://apcshbwa:CSR0XprhltThgK3KAbrbEIfW2QO6deYM@stingray.rmq.cloudamqp.com/apcshbwa' # Rabbitmq message que to send Async tasks
app.config['CELERY_BACKEND'] = 'db+sqlite:///messages.db' # Save information about asynctasks 
# End - Celery configuration for Asyncronous task execution

celery = make_celery(app) #Initialize a Celery application

@app.route("/",methods=['POST','GET'])
def home():
	return render_template	("index.php")  #Flask route to the homepage

tempVal = 0
startValue = 0
geo = Geoserver('http://localhost:8080/geoserver', username='admin', password='geoserver')  # Geoserver connection


@app.route("/<variable>",methods=['POST','GET'])
def test(variable):								# data=json.dumps(startValue) - startValue to the test.php page
	return render_template	("test.php", data=json.dumps(startValue)) # Once the form is submitted this test.php page will load

@app.route("/contact",methods=['POST','GET'])
def contact():
	return render_template	("contact.php") # Load contact us page

@celery.task(name='deletefiles') # Initialize an asynchronous task to delete files
def deleteAsync(FinalArea,FinalApartment,GeoApart, Geoareas):  
	time.sleep(20)   # Given a 20sec timeout before executing following commands
	geo.delete_layer(layer_name=GeoApart, workspace='ipproject')  # Delete Geoserver apartment layer
	geo.delete_layer(layer_name=Geoareas, workspace='ipproject')	# Delete Geoserver weighted sum layer layer
	geo.delete_featurestore(featurestore_name=GeoApart, workspace='ipproject') # Delete Geoserver featurestore connections
	geo.delete_featurestore(featurestore_name=Geoareas, workspace='ipproject') # Delete Geoserver featurestore connections
	time.sleep(20) # Given a 20sec timeout before executing following commands
	arcpy.management.Delete(FinalArea) # Delete final weighted sum shp file from server
	arcpy.management.Delete(FinalApartment) # Delete final apartment file from server

	return "Files have been successfully deleted"

@celery.task(name='generatefile')  # Generate asynchronous task to create a csv file with apartment details and their suitability
def generateApartmentLocationCSV(finalapartment_shp,finalapartment_table):
		#Field to store Suitablity of each apartment
	arcpy.management.AddField(in_table=finalapartment_shp, field_name="suitab", field_type="TEXT", field_precision=None, field_scale=None, field_length=None, field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
		
		#Field to store latitude and longitude of each apartment
	arcpy.management.AddField(in_table=finalapartment_shp, field_name="Lat", field_type="DOUBLE", field_precision=None, field_scale=None, field_length=None, field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
	arcpy.management.AddField(in_table=finalapartment_shp, field_name="Lon", field_type="DOUBLE", field_precision=None, field_scale=None, field_length=None, field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
	
		#Semantic representation of suitability of each apartment according to the user requirement
	arcpy.management.CalculateField(in_table=finalapartment_shp, field="suitab", expression="fieldCal(!gridcode!)", expression_type="PYTHON3", code_block="""def fieldCal(gridcode):
	if gridcode==0:
	    return \"Best\"
	elif gridcode==1:
	    return \"Good\"
	elif gridcode==2:
	    return \"Moderate\"
	elif gridcode==3:
	    return \"Bad\"
	elif gridcode==4:
	    return \"Worst\"""", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")

	
	fields = ['Lat','Lon'] # Define two fields of the feature layer to use with cursor
	saveLat =[]  # Create a list to store Latitude of the feature
	saveLon =[]	 # Create a list to store Longitude of the feature
	curGetxy = arcpy.da.SearchCursor(finalapartment_shp,["SHAPE@XY"]) #Initiate a Search cursor to access geometry of feature
	curUpdatexy = arcpy.da.UpdateCursor(finalapartment_shp, fields)  #Initiate a Update cursor to fill LAT and LON of the point feature

	i=0 # i variable use to access each element of LAT and LON arrays
	for row in curGetxy:
		x,y = row[0]	# get X, Y coordinates of each feature
		saveLat.append(y)  # Save Y value into the array
		saveLon.append(x)	# Save X value into the array
	
	for row in curUpdatexy: # Update newly created Lat and Lon fields with array values
		row[0]=saveLat[i]
		row[1]=saveLon[i]
		i+=1  
		curUpdatexy.updateRow(row)
	
	del curGetxy  # Terminate cursor initializations
	del curUpdatexy

	arcpy.conversion.ExportTable(finalapartment_shp, finalapartment_table) # Export the attribute table into a CSV file

@celery.task(name='generatemap') # Generate final location map
def compileMap(pdfName, finalapartment_shp):
	newDirectoryLocation = rootDirectory+'Project\\'+pdfName
	newProjectFileLocation = newDirectoryLocation+"\\"+pdfName+".aprx"
	newLayerFileLocation = newDirectoryLocation+"\\"+pdfName+".lyrx"
	newPDFLocation = newDirectoryLocation+"\\"+pdfName+".pdf"
	
	isExist = os.path.exists(newDirectoryLocation)
	if not isExist:
		os.makedirs(newDirectoryLocation)

	shutil.copy(rootDirectory+"FinalApartments.lyrx",newLayerFileLocation)
	shutil.copy(rootDirectory+"project.aprx",newProjectFileLocation)

	aprx = arcpy.mp.ArcGISProject(newProjectFileLocation) # Open ArcGIS Pro project file
	aprxMap = aprx.listMaps("First")[0]		# Selection of first map of the project
	aprxMap.addDataFromPath(finalapartment_shp) # Add final areas feature into the map

	Layout = aprx.listLayouts()[1]	# Selection of first layer of the project
	arcpy.ApplySymbologyFromLayer_management(aprxMap.listLayers()[0], newLayerFileLocation) # Apply symbology to the Map layer
	Layout.exportToPDF(newPDFLocation) # Export file as a PDF
	aprxMap.removeLayer(aprxMap.listLayers()[0]) # Remove the feature from the project document
	aprx.save()		# Save the ArcGIS project

@celery.task(name='emailfiles')  # Initialize an asynchronous task to email the csv file 
def emailDocs(finalapartment_map,finalapartment_table,recipient):
	msg=Message(subject='Best locations for your requirements',
	 			sender='noreply@ipcourse.at',
	 			body='This is the best locations based on you requirements', 
	 			recipients=[recipient])
	with app.open_resource(finalapartment_table) as fp: msg.attach("locations.csv", "text/csv", fp.read()) # Attachment - CSV table
	with app.open_resource(finalapartment_map) as fp: msg.attach("map.pdf", "application/pdf", fp.read()) # Attachment - PDF map
	mail.send(msg)
	os.remove(finalapartment_table)  # Remove the csv from server (localhost)

@app.route("/living",methods=['POST','GET']) #Once user submit this route will be executed
def living():
	arcpy.env.overwriteOutput = True
	global tempVal     # Access global variable 
	global geo 		   # Access geoserver connection
	tempVal=tempVal+1  # Increment value each time function execute (Use to create a unique value)
	global startValue  
	startValue = "finalAreas"+str(tempVal) # Create a unique name for the final wegihted some output
	variable = startValue
													#### Start - Get values from the form ####
	Ambuvalue=request.form.get("Ambuvalue")  
	AmbuvalueInt = int(Ambuvalue)

	Hospvalue=request.form.get("Hospvalue")
	HospvalueInt= int(Hospvalue)

	firevalue=request.form.get("firevalue")
	firevalueInt= int(firevalue)

	marketvalue=request.form.get("marketvalue")
	marketvalueInt= int(marketvalue)

	parkvalue=request.form.get("parkvalue")
	parkvalueInt= int(parkvalue)

	schoolvalue=request.form.get("schoolvalue")
	schoolvalueInt= int(schoolvalue)

	recipientEmail=request.form.get("emailRecipient")      #### End - Get values from the form ####

	print (startValue)
	
			#----Locations of the raster files to conduct the Weighted Sum Analysis----#
	Raster_Supermarket_tif = arcpy.Raster(rootDirectory+"Rasters\\Raster_Supermarket.tif")
	Raster_School_tif = arcpy.Raster(rootDirectory+"Rasters\\Raster_School.tif")
	Raster_Parks_tif = arcpy.Raster(rootDirectory+"Rasters\\Raster_Parks.tif")
	Raster_Hospital_tif = arcpy.Raster(rootDirectory+"Rasters\\Raster_Hospital.tif")
	Raster_Fire_tif = arcpy.Raster(rootDirectory+"Rasters\\Raster_Fire.tif")
	Raster_Ambulance_tif = arcpy.Raster(rootDirectory+"Rasters\\Raster_Ambulance.tif")
			#----Locations of the raster files to conduct the Weighted Sum Analysis----#

			# Start - Weighted Sum Table #
	WSumTableObj = WSTable([[Raster_Supermarket_tif, "VALUE", marketvalueInt], 
							[Raster_School_tif, "VALUE", schoolvalueInt],
							[Raster_Parks_tif, "VALUE", parkvalueInt],
							[Raster_Hospital_tif, "VALUE", HospvalueInt],
							[Raster_Fire_tif, "VALUE", firevalueInt],
							[Raster_Ambulance_tif, "VALUE", AmbuvalueInt]])
			# End - Weighted Sum Table #

	outWeightedSum = WeightedSum(WSumTableObj) # Condute Wighted Sum

	# Rescale the Weighted Sum output pixel values between 0 and 5
	outRescale =RescaleByFunction(in_raster=outWeightedSum, 
								  transformation_function=[["MSSMALL", 21, "", 97, "", 1, 1, ""]], 
								  from_scale=0, to_scale=5)

	# Rescale the Weighted Sum output pixel values between 0 and 5
	outRasterReclass = arcpy.sa.Reclassify(in_raster=outRescale, 
										   reclass_field="VALUE", 
										   remap="0 1 0;1 2 1;2 3 2;3 4 3;4 5 4", 
										   missing_values="DATA")
	
	Output_polygon_features = rootDirectory+"Vector\\"+startValue+".shp"

	# Convert the rescaled weighted sum result as a shapefile
	arcpy.RasterToPolygon_conversion(outRasterReclass, Output_polygon_features, "SIMPLIFY", "VALUE","MULTIPLE_OUTER_PART")
	

	#Apartment - filelocation on the server
	ApartmentLocations = rootDirectory+"Apartments\\ApartmentLocations.shp"
	
	#Updated Apartment shapefile - save location in the server
	finalapartment_shp = rootDirectory+"Vector\\Spatial_Join\\apartment"+startValue+".shp"
	
	#Updated Apartment CSV file save location in the server
	finalapartment_table = rootDirectory+"Vector\\Spatial_Join\\apartment"+startValue+".csv"

	# Map PDF location and directory
	finalapartment_map = rootDirectory+"Project\\"+startValue+"\\"+startValue+".pdf"

	# conduct spatial join between apartment shapefile and weightedsum output 
	arcpy.analysis.SpatialJoin(	target_features=ApartmentLocations, 
								join_features=Output_polygon_features, 
								out_feature_class=finalapartment_shp, 
								join_operation="JOIN_ONE_TO_ONE", 
								join_type="KEEP_ALL", 
								field_mapping="FID_ \"FID_\" true true false 19 Double 0 0,First,#,ApartmentLocations,FID_,-1,-1;ORIG_FID \"ORIG_FID\" true true false 19 Double 0 0,First,#,ApartmentLocations,ORIG_FID,-1,-1;Telephone \"Telephone\" true true false 19 Double 0 0,First,#,ApartmentLocations,Telephone,-1,-1;Cost \"Cost\" true true false 19 Double 0 0,First,#,ApartmentLocations,Cost,-1,-1;Status \"Status\" true true false 254 Text 0 0,First,#,ApartmentLocations,Status,0,254;Name \"Name\" true true false 254 Text 0 0,First,#,ApartmentLocations,Name,0,254;Id \"Id\" true true false 10 Long 0 10,First,#,finalAreas4,Id,-1,-1;gridcode \"gridcode\" true true false 10 Long 0 10,First,#,finalAreas4,gridcode,-1,-1", 
								match_option="INTERSECT", 
								search_radius="", distance_field_name="")


	# Call Celery asynchronous task - Generate apartment location CSV
	generateApartmentLocationCSV.delay(finalapartment_shp,finalapartment_table)
	compileMap.delay(startValue, finalapartment_shp)


	# Call Celery asynchronous task - Email the CSV and Map PDF to the recipient if email address is entered
	if recipientEmail != None:
		emailDocs.delay(finalapartment_map,finalapartment_table,recipientEmail)

	# Create a Datastore for final areas in geoserver
	geo.create_datastore(name=startValue, path=Output_polygon_features, workspace='ipproject')
	# Publish final areas shapefile in geoserver
	geo.publish_featurestore(workspace='ipproject', store_name=startValue, pg_table=startValue)
	# Apply style to the final areas shapefile in geoserver
	geo.publish_style(layer_name=startValue, style_name='finalAreas_ope', workspace='ipproject')

	# Start - Data store for final apartments
	apartmentsDataStore = "apartment"+startValue
	# Create a Datastore for apartment locations in geoserver
	geo.create_datastore(name=apartmentsDataStore, path=finalapartment_shp, workspace='ipproject')
	# Publish apartment locations shapefile in geoserver
	geo.publish_featurestore(workspace='ipproject', store_name=apartmentsDataStore, pg_table=apartmentsDataStore)
	# Apply style to the apartment locations shapefile in geoserver
	geo.publish_style(layer_name=apartmentsDataStore, style_name='finalAparts', workspace='ipproject')

	# Call Celery asynchronous task - Generate apartment location CSV
	deleteAsync.delay(Output_polygon_features, finalapartment_shp,startValue,apartmentsDataStore)  #New additions



	return redirect(url_for('test',variable = startValue)) # Redirect to the test.php

if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0')