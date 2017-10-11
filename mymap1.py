import folium
import pandas

#loading dataset into pandas library
data = pandas.read_csv("Volcanoes_USA.txt")

#loading coordinates from dataset into a python native list
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])

#changes color of the marker based on its elevation
def color_producer(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000<= elevation < 2000:
        return 'orange'
    else:
        return 'red'

#create a map object - pass default coordinates
map = folium.Map(location=[38.579729, -121.488093], zoom_start=4, tiles="Mapbox Bright")

#create a volcano Feature Group - and then pass it to the map
fg_volcano = folium.FeatureGroup(name="Volcanoes")

#for loop to loop through multiple coordinates and create markers on the map
for lt, ln, el in zip(lat, lon, elev):

# add_child method to add children to the map - adding a marker to the map
# Marker creates simple stock Leaflet(.js) marker on the map
# Leaflet is js library - the engine that creates the maps on the browser
    fg_volcano.add_child(folium.CircleMarker(location=[lt, ln], radius = 6, popup=str(el)+" m", fill_color=color_producer(el),
    color = 'grey', fill_opacity=0.7, fill=True))
    #to use markers instead of circles use the below statement
    #fg.add_child(folium.Marker(location=[lt, ln], popup=str(el)+" m", icon=folium.Icon(color=color_producer(el))))

# create Feature Group for population - add it to the map as a child
fg_population = folium.FeatureGroup(name="Population")

# To add polygons via folium - use folium.GeoJson() method
# create a new Feature Group to add a GeoJson object as a children
#pass the absolute path/file to the method, open it in read mode and specify encoding
# recent version of folium needs a string instead of a file as input hence pass the read() method
# style_function - access this to change color of polygons on the map based on a condition
# it expects a lambda function
fg_population.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(),
style_function=lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 10000000
else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))

#adding feature groups to the map as a child
map.add_child(fg_volcano)
map.add_child(fg_population)

# layer control class of Folium module - to add a control layer..
# ..to enable disable the layers as required
map.add_child(folium.LayerControl())

map.save("MyMap1.html")
