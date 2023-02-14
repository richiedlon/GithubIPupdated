<!DOCTYPE html>

<html>
<head>
    <title>IP Project</title>
    <meta charset="utf-8" />
	
	<link rel="stylesheet" href="static/css/sliders.css"/>

	<!-- Page loading indicator-->
	<link rel="stylesheet" href="static/css/pace-theme-center-atom.css"/>
	<script src="static/js/pace.js"></script>


	<!-- Leaflet libraries-->
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.3/dist/leaflet.css" integrity="sha256-kLaT2GOSpHechhsozzB+flnD+zUyjE2LlfWPgU04xyI=" crossorigin="" />
	<script src="https://unpkg.com/leaflet@1.9.3/dist/leaflet.js" integrity="sha256-WBkoXOwTeyKclOHuWtc+i2uENFpDZ9YPdf5Hf+D7ewM=" crossorigin=""></script>
	<!-- Draw-->
	<script src= "https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/0.2.3/leaflet.draw-src.js"></script>
	<link rel="stylesheet" href= "https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/0.2.3/leaflet.draw.css">
	<script src= "https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/0.2.3/leaflet.draw.js"></script>
	
	<!-- Slide menu-->
	<link rel="stylesheet" href="static/css/SlideMenu.css" />
	<script src="static/js/SlideMenu.js"></script> 
	
	<link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/font-awesome/4.5.0/css/font-awesome.min.css">
	
	<!-- GeoCoder and other-->
	<link rel="stylesheet" href="static/css/Control.OSMGeocoder.css"/>
	<script src="static/js/Control.OSMGeocoder.js"></script> 
	
	<!-- Overview minimap-->
	<link rel="stylesheet" href="static/css/MiniMap.css" />
	<script src="static/js/MiniMap.js"></script>
 
	<!-- Localisation including current location and AOI tools-->
	<link rel="stylesheet" href="static/css/L.Control.Locate.min.css" />
    <script src="static/js/L.Control.Locate.js"></script> 
	
	<!-- Mouse position-->
	<link rel="stylesheet" href="static/css/L.Control.MousePosition.css" />
    <script src="static/js/L.Control.MousePosition.js"></script>
	
	<!-- Navigation Bar-->
    <style>
    	.leaflet-control-navbar-fwd {
		background-image: url("/static/img/arrow-right_000000_14.png");
		}

		.leaflet-control-navbar-back {
		background-image: url("static/img/arrow-left_000000_14.png");
		}

		.leaflet-control-navbar-home {
		background-image: url("static/img/home_000000_14.png");
		}


		.leaflet-control-navbar-fwd-disabled {
		background-image: url("static/img/arrow-right_bbbbbb_14.png");
		}

		.leaflet-control-navbar-back-disabled {
		background-image: url("static/img/arrow-left_bbbbbb_14.png");
		}

		.leaflet-control-navbar-home-disabled {
		background-image: url("static/img/home_bbbbbb_14.png");
		}
    </style>
	<script src="static/js/NavBar.js"></script>
	
	<!-- Font and bootstrap plugin--> 
	<link href="//maxcdn.bootstrapcdn.com/font-awesome/4.5.0/css/font-awesome.min.css" rel="stylesheet">
	<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/popper.js@1.12.9/dist/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
	
	<!-- jquery-->


	<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
	<script src="static/js/map.js"></script>

	
    <style>
        body {
            padding: 0;
            margin: 0;
        }
        html, body, #map {
            height: 97%;
            width: 100%;
        }


	
    </style>
</head>
<body>
		{% include 'header.php' %}
		<div id="map"></div>
	
    <script>
	
		///// Base map \\\\
		var OpenStreetMap = L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png');
		var WorldImagery = L.tileLayer('http://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}');
			
	

		var wmsRequestURL = "http://localhost:8080/geoserver/wms?";	
		///// Default Base map initialization\\\\\ 	
		var map = L.map('map', {
				layers: [OpenStreetMap], /// Base map
				center: [47.81569, 13.04644],/// Map center
				zoom: 12	//// Zoom level
			});
		

		/////Base map initialization\\\\\
		var baseLayers = {
			"Open Street Map": OpenStreetMap,
			"World Imagery": WorldImagery
		};

		var letters = {{ data|safe}};

		///// layers from Geoserver (format WMS)\\\\
		var market = L.tileLayer.wms(wmsRequestURL, {
			layers: 'ipproject:SupermarketServices',
			format: 'image/png',
			transparent: true,
			version: '1.1.0',
			attribution: "myattribution"
		});
		var schools_service = L.tileLayer.wms(wmsRequestURL, {
			layers: 'ipproject:SchoolsServices',
			format: 'image/png',
			transparent: true,
			version: '1.1.0',
			attribution: "myattribution"
		});
		var Ambulance = L.tileLayer.wms(wmsRequestURL, {
			layers: 'ipproject:AmbulanceService',
			format: 'image/png',
			transparent: true,
			version: '1.1.0',
			attribution: "myattribution"
		});
		var Fire = L.tileLayer.wms(wmsRequestURL, {
			layers: 'ipproject:FireandRescueService',
			format: 'image/png',
			transparent: true,
			version: '1.1.0',
			attribution: "myattribution"
		});
		var parks = L.tileLayer.wms(wmsRequestURL, {
			layers: 'ipproject:ParksServices',
			format: 'image/png',
			transparent: true,
			version: '1.1.0',
			attribution: "myattribution"
		});
		var hospitals_service = L.tileLayer.wms(wmsRequestURL, {
			layers: 'ipproject:HospitalServices',
			format: 'image/png',
			transparent: true,
			version: '1.1.0',
			attribution: "myattribution"
		});
					  
		var finalLayer = 'ipproject:'+letters
		var Finals = L.tileLayer.wms(wmsRequestURL, {
			layers: finalLayer,
			format: 'image/png',
			transparent: true,
			version: '1.1.0',
			attribution: "myattribution"
		});
		
		var properties = L.tileLayer.wms(wmsRequestURL, {
			layers: 'ipproject:ApartmentLocations',
			format: 'image/png',
			transparent: true,
			version: '1.1.0',
			attribution: "myattribution"
		});

						  
		///// Group layers\\\\\
		var overlays = {			
			"Hospital service areas": hospitals_service,
			"Market": market,
			"Schools": schools_service,
			"Ambulance service areas": Ambulance,
			"Fire and Rescue service areas": Fire,
			"Green spaces and Community Parks": parks,
			"Final Areas": Finals,
			"Real estate locations": properties
			
			
		};
		//// Add the Find to the map\\\\\ 
		var osmGeocoder = new L.Control.OSMGeocoder();
        map.addControl(osmGeocoder);
				
		///// Add the Overview to the map\\\\\ 
        var osm2 = L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png');
		var miniMap = new L.Control.MiniMap(osm2, { toggleDisplay: true }).addTo(map);
		
		///// Add the scale control to the map\\\\\
		L.control.scale().addTo(map);
			
		///// Add the Navigation Bar to the map\\\\\\ 
		L.control.navbar({position: 'topleft'}).addTo(map);
			

		
		///// Add the geolocate control to the map\\\\\
		L.control.locate().addTo(map);
		
		///// Add the mouse position to the map - To get the coordinates of the map cursor \\\\\
		L.control.mousePosition().addTo(map);
		
		///// Add the draw feature to the map\\\\\
		var drawnItems = new L.FeatureGroup();
		map.addLayer(drawnItems);

		///// config draw feature\\\\\
		var drawControl = new L.Control.Draw({
			position: 'topleft',
			draw: {
				polygon: {
					shapeOptions: {color: 'purple'},
					allowIntersection: false,
					drawError: {color: 'orange',timeout: 1000},
					showArea: true,
					metric: false,
					repeatMode: true
				},
				polyline: {
					shapeOptions: {color: 'red'},
				},
				rect: {
					shapeOptions: {color: 'green'},
				},
				circle: {
					shapeOptions: {color: 'steelblue'},
				},
				marker: true
				},
						edit: {
						  featureGroup: drawnItems,
						  remove: true
					}
				});
		map.addControl(drawControl);
		map.on('draw:created', function (e) {
			var type = e.layerType,
				layer = e.layer;
			drawnItems.addLayer(layer);
		});
		

		
		///// Layer menu legend \\\\\
		var div = L.DomUtil.create('div', 'info-legend');	
			var title1 = 'Markets and Shopping malls';
			contents1 = div.innerHTML = '<br><img src="'+wmsRequestURL+'REQUEST=GetLegendGraphic&VERSION=1.0.0&FORMAT=image/png&WIDTH=20&HEIGHT=20&LAYER=ipproject:SupermarketServices" </img><br>';
			
			var title2 = 'School service areas';
			contents2 = div.innerHTML = '<br><img src="'+wmsRequestURL+'REQUEST=GetLegendGraphic&VERSION=1.0.0&FORMAT=image/png&WIDTH=20&HEIGHT=20&LAYER=	ipproject:SchoolsServices" </img><br>';

			var title3 = 'Hospital service areas';
			contents3 = div.innerHTML = '<br><img src="'+wmsRequestURL+'REQUEST=GetLegendGraphic&VERSION=1.0.0&FORMAT=image/png&WIDTH=20&HEIGHT=20&LAYER=ipproject:HospitalServices" </img><br>';
			
			var title4 = 'Green spaces and Community Parks';
			contents4 = div.innerHTML = '<br><img src="'+wmsRequestURL+'REQUEST=GetLegendGraphic&VERSION=1.0.0&FORMAT=image/png&WIDTH=20&HEIGHT=20&LAYER=ipproject:ParksServices" </img><br>';
			
			var title5 = 'Fire and Rescue service areas';
			contents5 = div.innerHTML = '<br><img src="'+wmsRequestURL+'REQUEST=GetLegendGraphic&VERSION=1.0.0&FORMAT=image/png&WIDTH=20&HEIGHT=20&LAYER=ipproject:FireandRescueService" </img><br>';
			
			var title6 = 'Ambulance service areas';
			contents6 = div.innerHTML = '<br><img src="'+wmsRequestURL+'REQUEST=GetLegendGraphic&VERSION=1.0.0&FORMAT=image/png&WIDTH=20&HEIGHT=20&LAYER=ipproject:AmbulanceService" </img><br>';
			
			var section1='<br><img src="'+wmsRequestURL+'REQUEST=GetLegendGraphic&VERSION=1.0.0&FORMAT=image/png&WIDTH=20&HEIGHT=20&LAYER=ipproject:'
			var section2='" </img><br>'
						
			
			var title7 = 'Final Livability Conditions';
			contents7 = div.innerHTML = section1+letters+section2;
			console.log(contents7);
			
			var title9 = 'Real estates';
			contents9 = div.innerHTML = '<br><img src="'+wmsRequestURL+'REQUEST=GetLegendGraphic&VERSION=1.0.0&FORMAT=image/png&WIDTH=20&HEIGHT=20&LAYER=ipproject:ApartmentLocations" </img><br>';
			
			
			var slideMenu = L.control.slideMenu('', {position: 'topright',height: '100%',direction: 'horizontal',delay: '5'}).addTo(map);
			slideMenu.setContents(title1 + contents1 + title2 + contents2 + title3 + contents3 + title4 + contents4 + title5 + contents5 + title6 + contents6 + title7 + contents7+ title9 + contents9);
		
		///// Adding base layers + geoserver layers
		L.control.layers(baseLayers,overlays).addTo(map);

		/// Adding geoJSON layer as a popup to show apartment prices \\\
					var layerGroup = L.geoJson(data, {
					  onEachFeature: function (feature, layer) {
					    layer.bindPopup(
					    `<table>
								  <tr>
								    <td><b>Name</td>
								    <td>`+feature.properties.Name+`</td>
								  </tr>
								  <tr>
								    <td><b>Cost</td>
								    <td>`+feature.properties.Cost+`</td>
								  </tr>
								  <tr>
								    <td><b>Status</td>
								    <td>`+feature.properties.Status+`</td>
								  </tr>
								  <tr>
								    <td><b>Telephone</td>
								    <td>+`+feature.properties.Telephone+`</td>
								  </tr>
						</table>`);
					  }
					}).addTo(map);


		
    </script>


</body>
</html>