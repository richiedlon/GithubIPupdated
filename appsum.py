import arcpy
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
geo = Geoserver('http://localhost:8080/geoserver', username='admin', password='geoserver')


@app.route("/<variable>",methods=['POST','GET'])
def test(variable):
	return render_template	("test.php", data=json.dumps(startValue))

@app.route("/contact",methods=['POST','GET'])
def contact():
	return render_template	("contact.php")



@app.route("/living",methods=['POST','GET'])
def living():
	arcpy.env.overwriteOutput = True
	global tempVal
	global geo
	tempVal=tempVal+1
	global startValue
	startValue = "finalAreas"+str(tempVal)
	variable = startValue
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
	
	geo.create_datastore(name=startValue, path=Output_polygon_features, workspace='ipproject')
	geo.publish_featurestore(workspace='ipproject', store_name=startValue, pg_table=startValue)
	geo.publish_style(layer_name=startValue, style_name='finalstyle', workspace='ipproject')
	
	return redirect(url_for('test',variable = startValue))

if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0')