import arcpy
import re
from arcpy.sa import WeightedOverlay,WOTable,RemapValue
arcpy.env.overwriteOutput = True

Raster_Supermarket_tif = arcpy.Raster("C:\\IPProject\\IPProject_files\\GithubIP\\Rasters\\Raster_Supermarket.tif")
Raster_School_tif = arcpy.Raster("C:\\IPProject\\IPProject_files\\GithubIP\\Rasters\\Raster_School.tif")
Raster_Parks_tif = arcpy.Raster("C:\\IPProject\\IPProject_files\\GithubIP\\Rasters\\Raster_Parks.tif")
Raster_Hospital_tif = arcpy.Raster("C:\\IPProject\\IPProject_files\\GithubIP\\Rasters\\Raster_Hospital.tif")
Raster_Fire_tif = arcpy.Raster("C:\\IPProject\\IPProject_files\\GithubIP\\Rasters\\Raster_Fire.tif")
Raster_Ambulance_tif = arcpy.Raster("C:\\IPProject\\IPProject_files\\GithubIP\\Rasters\\Raster_Ambulance.tif")

# Process: Weighted Overlay (Weighted Overlay) (sa)
finalRaster_tif = "C:\\IPProject\\IPProject_files\\GithubIP\\Rasters\\finalRaster1.tif"
final_vector = "C:\\IPProject\\IPProject_files\\GithubIP\\Rasters\\finalVector.shp"
finalRaster = WeightedOverlay(WOTable(
					[
					[Raster_Supermarket_tif, 0, "VALUE", RemapValue([[1,1],[2,2],[3,3],[4,4],[5,5]])], 
				    [Raster_School_tif, 80, "VALUE", RemapValue([[1,1],[2,2],[3,3],[4,4],[5,5]])], 
				    [Raster_Parks_tif, 0, "VALUE", RemapValue([[1,1],[2,2],[3,3],[4,4],[5,5]])], 
				    [Raster_Hospital_tif, 5, "VALUE", RemapValue([[1,1],[2,2],[3,3],[4,4],[5,5]])], 
				    [Raster_Fire_tif, 10, "VALUE", RemapValue([[1,1],[2,2],[3,3],[4,4],[5,5]])], 
				    [Raster_Ambulance_tif,5, "VALUE", RemapValue([[1,1],[2,2],[3,3],[4,4],[5,5]])]
				    ],[1,9,1]))
    
finalRaster.save(finalRaster_tif)
arcpy.RasterToPolygon_conversion(finalRaster_tif, final_vector, "NO_SIMPLIFY","VALUE")