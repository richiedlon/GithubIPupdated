import arcpy
from arcpy.mp import *
from arcpy.management import *

aprx = arcpy.mp.ArcGISProject(r"C:\IPProject\IPProject_files\GithubIP\Vector\Spatial_Join\project.aprx")
map = aprx.listMaps("First")[0]

# startvalue = ""
# newlayer = map.addDataFromPath(r"C:\IPProject\IPProject_files\GithubIP\Vector\Spatial_Join/apartment" + startvalue + ".shp")
newlayer = map.addDataFromPath(r"C:\IPProject\IPProject_files\GithubIP\Vector\Spatial_Join\apartmentfinalAreas2.shp")

#Adding Symbology
symbolLayer = (r"C:\IPProject\IPProject_files\GithubIP\Vector\Spatial_Join\Final Apartments.lyrx")
symbologyField= ["VALUE_FIELD", "gridcode", "gridcode"],
ApplySymbologyFromLayer(newlayer, symbolLayer, symbologyField)

#Creating the layout
layout = aprx.listLayouts()[1]
outpath= r"C:\IPProject\IPProject_files\GithubIP\Vector\pdfs"
layout.exportToPDF(outpath +"\ newmap.pdf")

#Sanitation - remonve file no longer needed
map.removeLayer(map.listLayers('apartmentfinalAreas2')[0])
