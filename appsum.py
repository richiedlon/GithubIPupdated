#import modulesimport arcpy
from arcpy.sa import *
from flask import Flask, redirect, url_for, render_template
from flask_wtf import FlaskForm
from wtforms import StringField
from flask import request
import random
import json
from geo.Geoserver import Geoserver


app = Flask(__name__)

@app.route("/",methods=['POST','GET'])
def home():

	return render_template	("index.php")

tempVal = 0
startValue = 0

#Geoserver
geo = Geoserver('http://localhost:8080/geoserver', username='admin', password='geoserver')

#Rendered after every new form is filled
@app.route("/<variable>",methods=['POST','GET'])
def test(variable):
	return render_template	("test.php", data=json.dumps(startValue))

#Rendered after contact us is clicked
@app.route("/contact",methods=['POST','GET'])
def contact():
	return render_template	("contact.php")

#Geoprocessing to be done after the Living Conditons form is filled
@app.route("/living",methods=['POST','GET'])
def living():

	#Geoprocessing begins: enviroment is set and global variables decleared
	arcpy.env.overwriteOutput = True
	global tempVal
	global geo
	tempVal=tempVal+1
	global startValue
	startValue = "finalAreas"+str(tempVal)
	variable = startValue

	#User input from Living conditions form is converted to integer: Arguments are from the form(livingconditionform.php)
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

	
	print (startValue)

	#Weighted Sum Begins
	Raster_Supermarket_tif = "C:\\IPProject\\IPProject_files\\GithubIP\\Rasters\\Raster_Supermarket.tif"
	Raster_School_tif = arcpy.Raster("C:\\IPProject\\IPProject_files\\GithubIP\\Rasters\\Raster_School.tif")
	Raster_Parks_tif = arcpy.Raster("C:\\IPProject\\IPProject_files\\GithubIP\\Rasters\\Raster_Parks.tif")
	Raster_Hospital_tif = arcpy.Raster("C:\\IPProject\\IPProject_files\\GithubIP\\Rasters\\Raster_Hospital.tif")
	Raster_Fire_tif = arcpy.Raster("C:\\IPProject\\IPProject_files\\GithubIP\\Rasters\\Raster_Fire.tif")
	Raster_Ambulance_tif = arcpy.Raster("C:\\IPProject\\IPProject_files\\GithubIP\\Rasters\\Raster_Ambulance.tif")

	WSumTableObj = WSTable([[Raster_Supermarket_tif, "VALUE", marketvalueInt], 
							[Raster_School_tif, "VALUE", schoolvalueInt],
							[Raster_Parks_tif, "VALUE", parkvalueInt],
							[Raster_Hospital_tif, "VALUE", HospvalueInt],
							[Raster_Fire_tif, "VALUE", firevalueInt],
							[Raster_Ambulance_tif, "VALUE", AmbuvalueInt]])

	outWeightedSum = WeightedSum(WSumTableObj)
	outRescale =RescaleByFunction(in_raster=outWeightedSum, transformation_function=[["MSSMALL", 21, "", 97, "", 1, 1, ""]], from_scale=0, to_scale=5)
	outRasterReclass = arcpy.sa.Reclassify(in_raster=outRescale, reclass_field="VALUE", remap="0 1 0;1 2 1;2 3 2;3 4 3;4 5 4", missing_values="DATA")
	
	Output_polygon_features = "C:\\ipproject\\IPProject_files\\GithubIP\\Vector\\"+startValue+".shp"
	arcpy.RasterToPolygon_conversion(outRasterReclass, Output_polygon_features, "SIMPLIFY", "VALUE","MULTIPLE_OUTER_PART")
	#Weighted Sum ends

	#Spatial Join Begins
	ApartmentLocations = "C:\\IPProject\\IPProject_files\\GithubIP\\Apartments\\ApartmentLocations.shp"
	finalapartment_shp = "C:\\Ipproject\\IPProject_files\\GithubIP\\Vector\\Spatial_Join\\apartment"+startValue+".shp"
	arcpy.analysis.SpatialJoin(target_features=ApartmentLocations, join_features=Output_polygon_features, out_feature_class=finalapartment_shp, 
	join_operation="JOIN_ONE_TO_ONE", 
	join_type="KEEP_ALL", 
	field_mapping="Shape_Leng \"Shape_Leng\" true true false 19 Double 0 0,First,#,ApartmentLocations,Shape_Leng,-1,-1;Shape_Area \"Shape_Area\" true true false 19 Double 0 0,First,#,ApartmentLocations,Shape_Area,-1,-1;ORIG_FID \"ORIG_FID\" true true false 10 Long 0 10,First,#,ApartmentLocations,ORIG_FID,-1,-1;Id \"Id\" true true false 10 Long 0 10,First,#,finalAreas1,Id,-1,-1;gridcode \"gridcode\" true true false 10 Long 0 10,First,#,finalAreas1,gridcode,-1,-1",
	match_option="INTERSECT", 
	search_radius="", 
	distance_field_name="")
	#Spatial Join Ends


	#Weighted sum output (Final Areas vector) pushed to geoserver
	geo.create_datastore(name=startValue, path=Output_polygon_features, workspace='ipproject')
	geo.publish_featurestore(workspace='ipproject', store_name=startValue, pg_table=startValue)
	geo.publish_style(layer_name=startValue, style_name='finalAreas_ope', workspace='ipproject')


	#Spatial join output (Final Apartments vector) pushed to geoserver
	apartmentsDataStore = "apartment"+startValue
	geo.create_datastore(name=apartmentsDataStore, path=finalapartment_shp, workspace='ipproject')
	geo.publish_featurestore(workspace='ipproject', store_name=apartmentsDataStore, pg_table=apartmentsDataStore)
	geo.publish_style(layer_name=apartmentsDataStore, style_name='finalAparts', workspace='ipproject')
	

	#Geoprocessing ends
	
	return redirect(url_for('test',variable = startValue))

if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0')