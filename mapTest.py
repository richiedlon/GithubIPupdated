import arcpy
from arcpy.mp import *
from arcpy.management import *

aprx = arcpy.mp.ArcGISProject(r"C:\Users\xeon\Desktop\GIS IP Class\Python Tiede\mapping\project.aprx")
map = aprx.listMaps()[0]

# changing Symbology
# startvalue = ""
# newlayer = map.addDataFromPath(r"C:\IPProject\IPProject_files\GithubIP\Vector\Spatial_Join/apartment" + startvalue + ".shp")
newlayer = map.addDataFromPath(r"C:\IPProject\IPProject_files\GithubIP\Vector\Spatial_Join/apartmentfinalAreas1.shp")
symbolLayer = (r"C:\Users\xeon\Desktop\IP Final Project\GithubIPupdated\Final Apartments.lyrx")
symbologyField= ["VALUE_FIELD", "gridcode", "gridcode"],
ApplySymbologyFromLayer(newlayer, symbolLayer, symbologyField)

# creating the layout
layout = aprx.listLayouts()[0]

outpath= r"C:\IPProject\IPProject_files\GithubIP\Vector\pdfs"
layout.exportToPDF(outpath +"\ newmap.pdf", 300)





# map = aprx.listMaps()[0]
# print(map.name)
# layers = map.listLayers()[0]
# print(layers.name)

# mf = layout.listElements("MAPFRAME_ELEMENT")[0]
# mfmap = mf.map
# mfLayers = mfmap.listLayers()

# for i in mfLayers:
#     print(i.name)


# for i in myLayers:
#     print(myLayers.name)

