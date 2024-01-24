# Take GPX file
# Convert to GeoJson
# Create FeatureCollection from all points
# Create FeatureCollection from first 10 points
# Create FeatureCollection from last 10 points
# Get centre for first 10 points 
# Get centre for last 10 points 
# Create bearing between first and last points
# Do +/- 

import gpxpy
from turfpy.measurement import center, bearing
from turfpy.transformation import line_offset
from geojson import Feature, FeatureCollection, Point, LineString, MultiLineString
from ipyleaflet import Map, GeoJSON, LayersControl, LayerGroup
from ipywidgets import Layout
import os

directory = "activities"
offset = 15
m = Map(center=((51.5095, -0.1245)), zoom=4)
m.layout.height = "100vh"
for path in os.listdir(directory):
    with open(directory + "/" + path, "r") as gpx_file:
        gpx = gpxpy.parse(gpx_file)
        gpx_points = gpx.tracks[0].segments[0].points
        line_string = LineString([(x.longitude, x.latitude) for x in gpx_points])
        first_five_center = center(LineString(line_string["coordinates"][:30]))
        last_five_center = center(LineString(line_string["coordinates"][-30:]))
        line = LineString([first_five_center["geometry"]["coordinates"], last_five_center["geometry"]["coordinates"]])
        pos_offset = line_offset(line, offset, unit="m")
        neg_offset = line_offset(line, offset * -1, unit="m")

        layers = [
            GeoJSON(data=line_string, style={"color": "blue"}, name=path),
            GeoJSON(data=pos_offset, style={"color": "red"}),
            GeoJSON(data=neg_offset, style={"color": "red"})
        ]

        m.add(LayerGroup(layers=layers, name=path))

layers_control = LayersControl(title="Legend", position="bottomright")
m.add(layers_control)
m.save("map/index.html")



    
