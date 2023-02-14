#app.py
import arcpy
from arcpy.sa import *
from flask import Flask, redirect, url_for, render_template
from flask_wtf import FlaskForm
from wtforms import StringField
from flask import request
import random


app = Flask(__name__)

@app.route("/",methods=['POST','GET'])
def home():

	return render_template	("index.php")

def eachPercentage(value,total):
	percent = value/total*100
	return percent

def adjustInflueceValues(sumNormalized, NormalizedArray):
	if (sumNormalized<100):
		difference = 100-sumNormalized
		if(difference==1):
			NormalizedArray[0]=NormalizedArray[0]+1
		elif (difference==2):
			NormalizedArray[0]=NormalizedArray[0]+1
			NormalizedArray[1]=NormalizedArray[1]+1
		elif (difference==3):
			NormalizedArray[0]=NormalizedArray[0]+1
			NormalizedArray[1]=NormalizedArray[1]+1
			NormalizedArray[2]=NormalizedArray[2]+1
		else:
			NormalizedArray[0]=NormalizedArray[0]+1
			NormalizedArray[1]=NormalizedArray[1]+1
			NormalizedArray[2]=NormalizedArray[2]+1	
			NormalizedArray[3]=NormalizedArray[3]+1
		return(NormalizedArray)
	elif(sumNormalized>100):	
		difference = sumNormalized-100
		if(difference==1):
			NormalizedArray[0]=NormalizedArray[0]-1
		elif (difference==2):
			NormalizedArray[0]=NormalizedArray[0]-1
			NormalizedArray[1]=NormalizedArray[1]-1
		elif (difference==3):
			NormalizedArray[0]=NormalizedArray[0]-1
			NormalizedArray[1]=NormalizedArray[1]-1
			NormalizedArray[2]=NormalizedArray[2]-1
		else:
			NormalizedArray[0]=NormalizedArray[0]-1
			NormalizedArray[1]=NormalizedArray[1]-1
			NormalizedArray[2]=NormalizedArray[2]-1	
			NormalizedArray[3]=NormalizedArray[3]-1
		return(NormalizedArray)	

startValue = 0
@app.route("/living",methods=['POST','GET'])
def living():
	arcpy.env.overwriteOutput = True
	global startValue
	startValue=startValue+1
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

	totalinfluence = AmbuvalueInt+HospvalueInt+firevalueInt+marketvalueInt+parkvalueInt+schoolvalueInt

	allInfluenceValues = [marketvalueInt,schoolvalueInt,parkvalueInt,HospvalueInt,firevalueInt,AmbuvalueInt]
	editedArrayValues =[]
	sumNormalized = 0
	FinalInfluenceValues =[]

	for i in allInfluenceValues:
		eachNormalized = round(eachPercentage(i, totalinfluence))
		sumNormalized =eachNormalized+sumNormalized
		editedArrayValues.append(eachNormalized)

	if (sumNormalized !=100):
		FinalInfluenceValues=adjustInflueceValues(sumNormalized,editedArrayValues)
	else:
		FinalInfluenceValues = editedArrayValues
	print(FinalInfluenceValues)
	

	
	Raster_Supermarket_tif = "C:\\IPProject\\IPProject_files\\GithubIP\\Rasters\\Raster_Supermarket.tif"
	Raster_School_tif = arcpy.Raster("C:\\IPProject\\IPProject_files\\GithubIP\\Rasters\\Raster_School.tif")
	Raster_Parks_tif = arcpy.Raster("C:\\IPProject\\IPProject_files\\GithubIP\\Rasters\\Raster_Parks.tif")
	Raster_Hospital_tif = arcpy.Raster("C:\\IPProject\\IPProject_files\\GithubIP\\Rasters\\Raster_Hospital.tif")
	Raster_Fire_tif = arcpy.Raster("C:\\IPProject\\IPProject_files\\GithubIP\\Rasters\\Raster_Fire.tif")
	Raster_Ambulance_tif = arcpy.Raster("C:\\IPProject\\IPProject_files\\GithubIP\\Rasters\\Raster_Ambulance.tif")

	# Process: Weighted Overlay (Weighted Overlay) (sa)
	finalRaster_tif = "C:\\IPProject\\IPProject_files\\GithubIP\\Rasters\\finalRaster.tif"
	final_vector = "C:\\IPProject\\IPProject_files\\GithubIP\\Rasters\\finalVector.shp"
	# finalRaster = WeightedOverlay(WOTable(
	# 					[
	# 					[Raster_Supermarket_tif, 0, "VALUE", RemapValue([[1,1],[2,2],[3,3],[4,4],[5,5]])], 
	# 				    [Raster_School_tif, 80, "VALUE", RemapValue([[1,1],[2,2],[3,3],[4,4],[5,5]])], 
	# 				    [Raster_Parks_tif, 0, "VALUE", RemapValue([[1,1],[2,2],[3,3],[4,4],[5,5]])], 
	# 				    [Raster_Hospital_tif, 5, "VALUE", RemapValue([[1,1],[2,2],[3,3],[4,4],[5,5]])], 
	# 				    [Raster_Fire_tif, 10, "VALUE", RemapValue([[1,1],[2,2],[3,3],[4,4],[5,5]])], 
	# 				    [Raster_Ambulance_tif,5, "VALUE", RemapValue([[1,1],[2,2],[3,3],[4,4],[5,5]])]
	# 				    ],[1,9,1]))
	# finalRaster.save(finalRaster_tif)


	WSumTableObj = WSTable([[Raster_Supermarket_tif, "VALUE", 50], 
							[Raster_School_tif, "VALUE", 2],
							[Raster_Parks_tif, "VALUE", 30],
							[Raster_Hospital_tif, "VALUE", 4],
							[Raster_Fire_tif, "VALUE", 5],
							[Raster_Ambulance_tif, "VALUE", 6]])

	outWeightedSum = WeightedSum(WSumTableObj)
	outRescale =RescaleByFunction(in_raster=outWeightedSum, transformation_function=[["MSSMALL", 21, "", 97, "", 1, 1, ""]], from_scale=0, to_scale=5)
	outRasterReclass = arcpy.sa.Reclassify(in_raster=outRescale, reclass_field="VALUE", remap="0 1 0;1 2 1;2 3 2;3 4 3;4 5 4", missing_values="DATA")
	
	Output_polygon_features = "C:\\IPProject\\IPProject_files\\GithubIP\\Vector\\output.shp"
	Output_polygon_features_dissolve = "C:\\IPProject\\IPProject_files\\GithubIP\\Vector\\outputdissolve.shp"
	arcpy.RasterToPolygon_conversion(outRasterReclass, Output_polygon_features, "SIMPLIFY", "VALUE","MULTIPLE_OUTER_PART")

	return render_template	("index.php")

if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0')