from geo.Geoserver import Geoserver
geo = Geoserver('http://localhost:8080/geoserver', username='admin', password='geoserver')


Output_polygon_features = "C:\\ipprojectdemo\\IPProject_files\\GithubIP\\Vector\\finalAreas2.shp"

geo.create_datastore(name="finalAreas2", path=Output_polygon_features, workspace='ipproject')
geo.publish_featurestore(workspace='ipproject', store_name="output", pg_table="output")