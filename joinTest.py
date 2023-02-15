import arcpy
from arcpy.sa import *
from flask import Flask, redirect, url_for, render_template
from flask_wtf import FlaskForm
from wtforms import StringField
from flask import request
import random
import json
from geo.Geoserver import Geoserver

geo = Geoserver('http://localhost:8080/geoserver', username='admin', password='geoserver')


#Spatial Join Begins
ApartmentLocations = "C:\\IPProject\\IPProject_files\\GithubIP\\Apartments\\ApartmentLocations.shp"
finalAreas = "C:\\ipproject\\IPProject_files\\GithubIP\\Vector\\finalAreas2.shp"

finalapartment_shp = "C:\\ipproject\\IPProject_files\\GithubIP\\Vector\\Spatial_Join\\"+"Apartments_"+"startValue"+".shp"
arcpy.analysis.SpatialJoin(target_features=ApartmentLocations, join_features=finalAreas, out_feature_class=finalapartment_shp, 
join_operation="JOIN_ONE_TO_ONE", 
join_type="KEEP_ALL", 
field_mapping="Shape_Leng \"Shape_Leng\" true true false 19 Double 0 0,First,#,ApartmentLocations,Shape_Leng,-1,-1;Shape_Area \"Shape_Area\" true true false 19 Double 0 0,First,#,ApartmentLocations,Shape_Area,-1,-1;ORIG_FID \"ORIG_FID\" true true false 10 Long 0 10,First,#,ApartmentLocations,ORIG_FID,-1,-1;Id \"Id\" true true false 10 Long 0 10,First,#,finalAreas1,Id,-1,-1;gridcode \"gridcode\" true true false 10 Long 0 10,First,#,finalAreas1,gridcode,-1,-1",
match_option="INTERSECT", 
search_radius="", 
distance_field_name="")
#Spatial Join Ends