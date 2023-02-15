WebMap To Help users select the best apartents based on their accessibility to social facilities.
![Screenshot 2023-02-15 223304](https://user-images.githubusercontent.com/80511315/219173155-4cbabfa1-ffe2-46f2-830f-d617a10dff15.png)

WEBMAP CONTENT
The webapp is made up of a 
•	header file (home button, living conditions form and contact form)
    o	The home button is the (index.php)
    o	The living conditions form is the (livingconditionsform.php): 
    o	The contact form (contact.php)

•	Body (main map)
  o	Leaflet map
      	Overlay (basemaps and service areas as WMS )
      	Legend (for each overlay)
      	Drawing function (polygon, line, point)
      	Find (location search)
      	Markers (apartment locations, with popups showing details and availability(static))

Main function of the Webmap
Users fill in their preferred requirements for each service in a form. Upon filling, results are collected as input into the geoprocessing steps (reclassed and weighted based on their preference to produce a final area map). 
The final areas map is the used to rank the available apartments from best to worst. 
Outputs are published onto geoserver, and then displayed in the webapp as final area and preferred apartments. 

Geoprocessing tools used are;
•	Weighted sum
•	Spatial join: To rank the apartments from best to worst.

Flask is used to incorporate the python geoprocessing steps with the index files (test and index)

THE CODE STRUCTURE
The code files are:
•	index.php (run as default home)
•	test.php (same as index.php but run after each new form submission: Here, the final areas and final apartments visualized; added to the overlay and legend)
•	appsum.py (contains the geoprocessing steps using arcpy package. Using Flask, the rendering of different parts of the code are incorporated with the geoprocessing).

