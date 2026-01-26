import folium, folium.features
from flask import Blueprint, render_template, request, flash

bp = Blueprint('advanced_maps', __name__)

@bp.route('/am/map_op1')
def map_op1():
    return render_template('maps/page_with_museums_paris.html', 
        name="Map with OSM data found with Overpass: museums in Paris", 
        city="Paris",
        wikipedia_city="fr:Paris",
        loc=[48.857481, 2.347425])

@bp.route('/am/map_op2')
def map_op2():
    import requests
    from osm2geojson import json2geojson
      
    try:
        query = """
            [out:json][timeout:25];
            area[name="Galway"]->.searchArea; 
            node[amenity="restaurant"](area.searchArea); 
            out;
        """
  
        overpass_url = "https://overpass-api.de/api/interpreter"
        response = requests.post(overpass_url, data={'data': query})
  
        if response.status_code == 200:
            data = response.json()
        else:
            flash("Error retrieving data with Overpass API", category="error")
            return render_template('maps/page_with_map.html', name="No map to display")
          
        geojson_data = json2geojson(data)
          
        m = folium.Map(location=[53.27340, -9.05080], zoom_start=17)
  
        for feature in geojson_data['features']:
            tags = feature['properties'].get('tags', {})
            if 'name' in tags and 'cuisine' in tags:
                feature['properties']['desc'] = tags['name'] + ' (' + tags['cuisine'] + ')'
            elif 'name' in tags:
                feature['properties']['desc'] = tags['name']

        folium.GeoJson(
            geojson_data,
            name='Restaurants',
            marker = folium.Marker(icon=folium.Icon(icon='cutlery', prefix='fa', markerColor='orange')),
            tooltip=folium.GeoJsonTooltip(fields=['desc'], labels=False)
        ).add_to(m)

        folium.LayerControl().add_to(m)

        return render_template('maps/page_with_map.html', 
            name="Map with OpenStreetMap data: restaurants in Galway", 
            map_html=m._repr_html_())
  
    except Exception as e:
        flash("An error has been encountered:<br/>" + str(e), category="error")
        return render_template('maps/page_with_map.html', name="No map to display")

@bp.route('/am/map_op3')
def map_op3():
    import requests, json
    from osm2geojson import json2geojson
        
    try:
        query = """
            [out:json][timeout:25];
            area[name="Sedona"][wikipedia="en:Sedona, Arizona"]->.searchArea; 
            way[highway~"^(motorway|motorway_link|trunk|trunk_link|primary|secondary|tertiary|unclassified|residential|living_street|service|track)$"](area.searchArea);
            out geom;
        """
   
        overpass_url = "https://overpass-api.de/api/interpreter"
        response = requests.post(overpass_url, data={'data': query})
   
        if response.status_code == 200:
            data = response.json()
        else:
            flash("Error retrieving data with Overpass API", category="error")
            return render_template('maps/page_with_map.html', name="No map to display")
           
        geojson_data = json2geojson(data)
   
        return render_template('maps/page_with_roads_sedona.html', 
            name="Map with OpenStreetMap data: carriageways in Sedona", 
            geojson_data=geojson_data,
            loc=[34.8589, -111.7714])
   
    except Exception as e:
        flash("An error has been encountered:<br/>" + str(e), category="error")
        return render_template('maps/page_with_map.html', name="No map to display")

@bp.route('/am/map_op4')
def map_op4():
    import requests, re
    from osm2geojson import json2geojson
   
    city_raw = request.args.get('city', 'Paris')
    city = re.sub(r'[^a-zA-Z0-9\s\-]', '', city_raw)
    popmin = request.args.get('popmin', '0')
   
    try:
        if isInt(popmin) != True:
            popmin = "0"

        query = '''
            [out:json][timeout:25];
            node[~"^(name|name:en)$"~"^''' + city + '''$"][place~"^(city|town|village)$"]
                (if:(is_number(t["population"]) && 
                number(t["population"])>=''' + popmin + '''));
            out;
        '''
          
        overpass_url = "https://overpass-api.de/api/interpreter"
        response = requests.post(overpass_url, data={'data': query})
  
        if response.status_code == 200:
            data = response.json()
        else:
            flash("Error retrieving data with Overpass API", category="error")
            return render_template('maps/page_with_map.html', name="No map to display")
          
        geojson_data = json2geojson(data)
        #print(geojson_data)
          
        maps_with_names = []
        for feature in geojson_data["features"]:
            lat = feature["geometry"]["coordinates"][1]
            lon = feature["geometry"]["coordinates"][0]
            tags = feature["properties"].get("tags", {})
            pop = int(tags.get("population", 0))
  
            m = folium.Map(location=[lat, lon], zoom_start= get_zoom_from_population(pop), control_scale=True)
 
            geojson_data_copy = geojson_data.copy()
            geojson_data_copy["features"] = [feature]
              
            folium.GeoJson(
                geojson_data_copy,
                name='City',
                marker=folium.Marker(icon=folium.Icon(color='red', icon='info-sign'))
            ).add_to(m)
  
            folium.LayerControl().add_to(m)
  
            maps_with_names.append([city + ", " + str(pop) + " inhabitants", m._repr_html_()])
  
        return render_template('maps/page_with_several_maps.html', 
            name="Maps of cities with the name of " + city + " and more than " + popmin + " inhabitants", 
            maps_with_names=maps_with_names)
  
    except Exception as e:
        flash("An error has been encountered:<br/>" + str(e), category="error")
        return render_template('maps/page_with_map.html', name="No map to display")

def isInt(var):
    try:
        int(var)
        return True
    except ValueError:
        return False

def get_zoom_from_population(pop):
    if pop < 1000:
        return(16) 
    elif pop < 10000:
        return(14)
    elif pop < 100000:
        return(13)
    elif pop < 1000000:
        return(12)
    elif pop < 5000000:
        return(11)
    else:
        return(10)

@bp.route('/am/map_nom')
def map_nom():
    import requests, re, copy
   
    city = re.sub(r'[^a-zA-Z0-9\s\-]', '', request.args.get('city', 'Paris'))
        
    try:
        user_agent = {'User-Agent': 'CartoOSM/1.0 (patrick@carto-osm.fr)'}
        params = {
            "city": city,
            "format": "geojson",
            "polygon_geojson": 1,
            "dedupe": 1,
            "extratags": 1
        }
        response = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params=params,
            headers = user_agent)
           
        if response.status_code == 200:
            data = response.json()
        else:
            flash("Error retrieving data with Nominatim API", category="error")
            return render_template('maps/page_with_map.html', name="No map to display")
        #print(response)
           
        geojson_data_with_names_and_locs = []
        for feature in data["features"]:
            if "addresstype" in feature["properties"] and \
            (feature["properties"]["addresstype"] == "city" or \
            feature["properties"]["addresstype"] == "town" or \
            feature["properties"]["addresstype"] == "village") and \
            "bbox" in feature and "display_name" in feature["properties"]:
                lat1 = feature["bbox"][1]
                lon1 = feature["bbox"][0]
                lat2 = feature["bbox"][3]
                lon2 = feature["bbox"][2]
                bbox = [[lat1, lon1], [lat2, lon2]]
               
                lat_med = (float(lat1) + float(lat2))/2
                lon_med = (float(lon1) + float(lon2))/2
                loc = [lat_med, lon_med]
                   
                disp_name = feature["properties"]["display_name"]
                   
                single_feature_data = copy.deepcopy(data)
                single_feature_data["features"] = [feature]
               
                geojson_data_with_names_and_locs.append([disp_name, loc, bbox, single_feature_data])

        return render_template('maps/page_with_several_maps_ll.html', 
            name="Maps of cities with the name " + city, 
            geojson_data_with_names_and_locs=geojson_data_with_names_and_locs)
   
    except Exception as e:
        flash("An error has been encountered:<br/>" + str(e), category="error")
        return render_template('maps/page_with_map.html', name="No map to display")

@bp.route('/am/map_nom_rev1')
def map_nom_rev1():
    import requests

    lat = request.args.get('lat', None)
    lon = request.args.get('lon', None)
       
    try:
        if (lat != None and lon != None and isFloat(lat) and isFloat(lon)):
            user_agent = {'User-Agent': 'CartoOSM/1.0 (patrick@carto-osm.fr)'}
            params = {
                "lat": float(lat),
                "lon": float(lon),
                "zoom": 16,
                "format": "json"
            }
            response = requests.get(
                "https://nominatim.openstreetmap.org/reverse",
                params=params,
                headers = user_agent)
  
            if response.status_code == 200:
                data = response.json()
                address = data.get("display_name", "In the middle of nowhere")
            else:
                flash("Error retrieving data with Nominatim API", category="error")
                return render_template('maps/page_with_map.html', name="No map to display")
  
            m = folium.Map(location=[float(lat), float(lon)], zoom_start=8)
  
            folium.Marker(
                location=[float(lat), float(lon)],
                popup=folium.Popup(address + "<br/>[" + lat + ", " + lon + "]", show=True)
            ).add_to(m)
  
            return render_template('maps/page_with_map.html', 
                name="Address of the point with latitude " + lat + " and longitude " + lon, 
                map_html=m._repr_html_())
  
        else:
            m = folium.Map(location=[45, -90], zoom_start=4)
 
            return render_template('maps/page_with_map.html', 
                name="No coordinates provided", 
                map_html=m._repr_html_())

    except Exception as e:
        flash("An error has been encountered:<br/>" + str(e), category="error")
        return render_template('maps/page_with_map.html', name="No map to display")

def isFloat(var):
    try:
        float(var)
        return True
    except ValueError:
        return False

@bp.route('/am/map_nom_rev2')
def map_nom_rev2():
    import requests

    lat = request.args.get('lat', None)
    lon = request.args.get('lon', None)
    click_event_script = """
        <script>
        document.addEventListener("DOMContentLoaded", function() {
            const map = Object.values(window).find(obj => obj instanceof L.Map);
  
            if (map) {
                map.on('click', function(e) {
                    const lat = e.latlng.lat.toFixed(6);
                    const lng = e.latlng.lng.toFixed(6);
  
                    window.top.location.href = '/am/map_nom_rev2?lat=' + lat + '&lon=' + lng;
                });
            }                  
        });
        </script>
    """
       
    try:
        if (lat != None and lon != None and isFloat(lat) and isFloat(lon)):
            user_agent = {'User-Agent': 'CartoOSM/1.0 (patrick@carto-osm.fr)'}
            params = {
                "lat": float(lat),
                "lon": float(lon),
                "zoom": 16,
                "format": "json"
            }
            response = requests.get(
                "https://nominatim.openstreetmap.org/reverse",
                params=params,
                headers = user_agent)
  
            if response.status_code == 200:
                data = response.json()
                address = data.get("display_name", "In the middle of nowhere")
            else:
                flash("Error retrieving data with Nominatim API", category="error")
                return render_template('maps/page_with_map.html', name="No map to display")
  
            m = folium.Map(location=[float(lat), float(lon)], zoom_start=8)
  
            #folium.features.LatLngPopup().add_to(m)
            
            folium.Marker(
                location=[float(lat), float(lon)],
                popup=folium.Popup(address + "<br/>[" + lat + ", " + lon + "]", show=True)
            ).add_to(m)
  
            m.get_root().html.add_child(folium.Element(click_event_script))
            
            return render_template('maps/page_with_map.html', 
                name="Address of the point with latitude " + lat + " and longitude " + lon, 
                map_html=m._repr_html_())
  
        else:
            m = folium.Map(location=[45, -90], zoom_start=4)
 
            #folium.features.LatLngPopup().add_to(m)

            m.get_root().html.add_child(folium.Element(click_event_script))
            
            return render_template('maps/page_with_map.html', 
                name="No coordinates provided", 
                map_html=m._repr_html_())
            
    except Exception as e:
        flash("An error has been encountered:<br/>" + str(e), category="error")
        return render_template('maps/page_with_map.html', name="No map to display")

@bp.route('/am/map_nom_rev3')
def map_nom_rev3():
       
    lat = request.args.get('lat', None)
    lon = request.args.get('lon', None)
   
    try:
        if (lat != None and lon != None and isFloat(lat) and isFloat(lon)):
            return render_template('maps/page_with_address_rev.html', 
                name="Click on the map",
                loc=[float(lat), float(lon)],
                zoom=8)
        else:
            return render_template('maps/page_with_address_rev.html', 
                name="Click on the map", 
                loc=["", ""],
                zoom=4)
           
    except Exception as e:
        flash("An error has been encountered:<br/>" + str(e), category="error")
        return render_template('maps/page_with_map.html', name="No map to display")

@bp.route('/am/map_cho1')
def map_cho1():
    import json

    try:
        with open("prototypes/static/Canada_provincial_limits.geojson", 'r', encoding='utf-8') as f:
            province_geo = json.load(f)
   
        with open("prototypes/static/Unemployment_Rates_by_Canadian_Province.csv", 'r', encoding='utf-8') as f:
            province_data = f.read()
 
        return render_template('maps/page_with_choropleth_map_canada.html', 
            name="Choropleth map: unemployment rates by province in Canada", 
            province_geo=province_geo, 
            province_data=province_data)

    except Exception as e:
        flash("An error has been encountered:<br/>" + str(e), category="error")
        return render_template('maps/page_with_map.html', name="No map to display")

@bp.route('/am/map_cho2')
def map_cho2():
    import requests, pandas

    try:
        response = requests.get(
            "https://www.data.gouv.fr/fr/datasets/r/90b9341a-e1f7-4d75-a73c-bbc010c7feeb"
        )

        departments_geo = None
        if response.status_code == 200:
            departments_geo = response.json()
        else:
            flash("Error downloading department contours from the Internet", category="error")
            return render_template('maps/page_with_map.html', name="No map to display")

        departments_data = pandas.read_csv("prototypes/static/Densities per department.csv")

        m = folium.Map(location=[46.769567, 2.433057], zoom_start=6)

        crpl = folium.Choropleth(
            geo_data=departments_geo,
            data=departments_data,
            columns=["Department", "Density"],
            key_on="feature.properties.nom",
            threshold_scale
=[0, 20, 46, 79.7, 123.6, 180.5, 254.5, 350.6, 475.4, 637.6, 848.2, 1121.8, 1477.2, 1939.9, 2538.6, 3317.6, 4329.6, 5644.2, 7351.8, 9570, 12451.4, 16194.3, 21056.5],
            fill_color="BuPu",
            name="Densities",
            legend_name="Densities (inhabitants per km2)",
            highlight=True
        ).add_to(m)

        indexed_department_data = departments_data.set_index('Department')
  
        for dep in crpl.geojson.data['features']:
            dep_name = dep['properties'].get('nom', 'Unknown')
            if dep_name in indexed_department_data.index:
                dep['properties']['density'] = str(indexed_department_data.loc[dep_name, 'Density'])
            else:
                dep['properties']['density'] = "Unavailable"  
        
        folium.GeoJsonPopup(fields=['nom', 'density'], aliases=['Name:', 'Density:'], labels=True, localize=True, safe=False).add_to(crpl.geojson)
  
        folium.LayerControl().add_to(m)
        
        return render_template('maps/page_with_map.html', 
            name="Choropleth map: densities per department in France", 
            map_html=m._repr_html_())

    except Exception as e:
        flash("An error has been encountered:<br/>" + str(e), category="error")
        return render_template('maps/page_with_map.html', name="No map to display")

@bp.route('/am/map_rout1')
def map_rout1():
    import geopandas, json

    try:
        track = geopandas.read_file("prototypes/static/Along_the_Seine_river_and_beyond_by_bike.gpx", layer="tracks")
        if track.crs is None:
            track = track.set_crs("EPSG:4326")
        track_geo = track[['geometry']]
        track_geoJSON = json.loads(track_geo.to_json())

        return render_template('maps/page_with_route1.html', 
            name=" Map with route extracted from Komoot: along the Seine river and beyond by bike",
            loc=[49.2167, 1.1667],
            zoom=10,
            track_geoJSON=track_geoJSON)

    except Exception as e:
        flash("An error has been encountered:<br/>" + str(e), category="error")
        return render_template('maps/page_with_map.html', name="No map to display")

@bp.route('/am/map_rout2')
def map_rout2():
    import geopandas as gpd

    try:
        track = gpd.read_file("prototypes/static/From_El_Paso_to_Sedona.gpx", layer="tracks")
        if track.crs is None:
            track = track.set_crs("EPSG:4326")
        track_geo = track[['geometry']]
        track_geoJSON = track_geo.to_json()

        m = folium.Map(location=[33.542498, -111.870257], zoom_start=8)

        folium.GeoJson(
            data=track_geoJSON,
            style_function=lambda x: {'color': 'darkblue', 'weight': 5}
        ).add_to(m)

        track_geoJSONDict = track_geo.__geo_interface__

        geom_type = track_geoJSONDict["features"][0]["geometry"]["type"]
        coords = track_geoJSONDict["features"][0]["geometry"]["coordinates"]
        if geom_type == 'LineString':
            start_coords = [coords[0][1], coords[0][0]]   # [lat, lon]
            end_coords = [coords[-1][1], coords[-1][0]]
        elif geom_type == 'MultiLineString':
            start_coords = [coords[0][0][1], coords[0][0][0]]
            end_coords = [coords[-1][-1][1], coords[-1][-1][0]]
        else:
            start_coords = None
            end_coords = None

        if (start_coords != None or end_coords != None): 
            folium.Marker(start_coords, popup="Departure: El Paso", icon=folium.Icon(color='green')).add_to(m)
            folium.Marker(end_coords, popup="Arrival: Sedona", icon=folium.Icon(color='red')).add_to(m)
       
        bounds = track_geo.total_bounds
        m.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]],
            padding=(30, 30))

        return render_template('maps/page_with_map.html', 
            name = "Map with route extracted from Google Maps: from El Paso to Sedona", 
            map_html=m._repr_html_())

    except Exception as e:
        flash("An error has been encountered:<br/>" + str(e), category="error")
        return render_template('maps/page_with_map.html', name = "No map to display")

@bp.route('/am/map_rout3')
def map_rout3():
    import requests, json

    try:
        response = requests.get(
            "https://router.project-osrm.org/route/v1/foot/-1.238317,43.162498;-8.540143,42.881940?geometries=geojson"
        )

        if response.status_code == 200:
            response_json = response.json()
        else:
            flash("Error querying OSRM", category="error")
            return render_template('maps/page_with_map.html', name="No map to display")

        if not response_json.get("routes"):
            flash("No route found.", category="error")
            return render_template('maps/page_with_map.html', name="No map to display")

        route_geo = response_json['routes'][0]
        distance_miles = round(route_geo['distance'] / 1609.344, 2)
        duration_hours = round((distance_miles / 3.106856), 1)
        geom = route_geo['geometry']

        geojson_data = json.loads('{"type": "FeatureCollection", "features": [{"type": "Feature", "properties": {}}]}')
        geojson_data['features'][0]['properties'] = {
            'distance_miles': distance_miles,
            'duration_hours': duration_hours
        }
        geojson_data['features'][0]['geometry'] = geom

        gtype = geom['type']
        coords = geom['coordinates']

        if not coords:
            flash("No geometry coordinates in route", category="error")
            return render_template('maps/page_with_map.html', name="No map todisplay")
        if gtype == 'LineString':
            start_coords = coords[0][::-1]
            end_coords = coords[-1][::-1]
        elif gtype == 'MultiLineString':
            start_coords = coords[0][0][::-1]
            end_coords = coords[-1][-1][::-1]
        else:
            flash("No suitable geometry coordinates in route", category="error")
            return render_template('maps/page_with_map.html', name="No map todisplay")

        return render_template('maps/page_with_route3.html', 
            name="Map with route searched with OSRM: from Saint-Jean-Pied-de-Port to Santiago-de-Compostela", 
            loc=[42.874, -4.598],
            zoom=7,
            track_geo=geojson_data,
            start=start_coords,
            end=end_coords
        )

    except Exception as e:
        flash("An error has been encountered:<br/>" + str(e), category="error")
        return render_template('maps/page_with_map.html', name="No map to display")

@bp.route('/am/map_rout4')
def map_rout4():
    import requests, json, gpxpy, gpxpy.gpx

    try:
        response = requests.get(
            "https://router.project-osrm.org/route/v1/driving/-1.238317,43.162498;-8.540143,42.881940?steps=true&geometries=geojson"
        )

        if response.status_code == 200:
            response_json = response.json()
        else:
            flash("Error querying OSRM", category="error")
            return render_template('maps/page_with_map.html', name="No map to display")

        if not response_json.get("routes"):
            flash("No route found.", category="error")
            return render_template('maps/page_with_map.html', name="No map to display")

        route_geo = response_json['routes'][0]
        distance_miles = round(route_geo['distance'] / 1609.344, 2)
        duration_hours = round(route_geo['duration'] / 3600, 1)
        geom = route_geo['geometry']

        geojson_data = json.loads('{"type": "FeatureCollection", "features": [{"type": "Feature", "properties": {}}]}')
        geojson_data['features'][0]['properties'] = {
            'distance_miles': distance_miles,
            'duration_hours': duration_hours
        }
        geojson_data['features'][0]['geometry'] = geom

        gtype = geom['type']
        coords = geom['coordinates']

        if not coords:
            flash("No geometry coordinates in route", category="error")
            return render_template('maps/page_with_map.html', name="No map to display")
        if gtype == 'LineString':
            start_coords = coords[0][::-1]
            end_coords = coords[-1][::-1]
        elif gtype == 'MultiLineString':
            start_coords = coords[0][0][::-1]
            end_coords = coords[-1][-1][::-1]
        else:
            flash("No suitable geometry coordinates in route", category="error")
            return render_template('maps/page_with_map.html', name="No map to display")
    
        instructions = []
        i = 0
        for leg in route_geo['legs']:
            for step in leg['steps']:
                i = i + 1
                maneuver_type = step['maneuver'].get('type', '')
                modifier = step['maneuver'].get('modifier', '')
                road_ref = step.get('ref', '')
                road_name = step.get('name', '')
                dist = int(step.get('distance', 0)//1)

                if (maneuver_type == 'depart'):
                    instruction_text = 'Start from departure point'
                elif (maneuver_type == 'arrive'):
                    instruction_text = 'Arrive at destination'
                elif (maneuver_type == 'roundabout'):
                    instruction_text = 'Enter roundabout'
                elif (maneuver_type == 'exit roundabout'):
                    instruction_text = 'Exit roundabout'
                elif (modifier == 'left'):
                    instruction_text = 'Turn left'
                elif (modifier == 'right'):
                    instruction_text = 'Turn right'
                elif (modifier == 'slight left'):
                    instruction_text = 'Make a slight left'
                elif (modifier == 'slight right'):
                    instruction_text = 'Make a slight right'
                else:
                    instruction_text = 'Continue'

                if (road_ref != ''):
                    instruction_text = f"{instruction_text} on {road_ref}"
                    if (road_name != ''):
                        instruction_text = f"{instruction_text} ({road_name})"
                else:
                    if (road_name != ''):
                        instruction_text = f"{instruction_text} on { road_name}"

                instructions.append([i, instruction_text, dist])

        if gtype == 'LineString':
            gpx = gpxpy.gpx.GPX()    
            gpx_track = gpxpy.gpx.GPXTrack()
            gpx.tracks.append(gpx_track)
            gpx_segment = gpxpy.gpx.GPXTrackSegment()
            gpx_track.segments.append(gpx_segment)

            for lon, lat in coords:
                gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(latitude=lat, longitude=lon))

            gpx_data = gpx.to_xml()
        elif gtype == 'MultiLineString':
            gpx = gpxpy.gpx.GPX()
            gpx_track = gpxpy.gpx.GPXTrack()
            gpx.tracks.append(gpx_track)

            for part in coords:
                gpx_segment = gpxpy.gpx.GPXTrackSegment()
                gpx_track.segments.append(gpx_segment)

                for lon, lat in part:
                    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(latitude=lat, longitude=lon))

            gpx_data = gpx.to_xml()

        return render_template('maps/page_with_route4.html', 
            name="Map with route searched with OSRM: from Saint-Jean-Pied-de-Port to Santiago-de-Compostela", 
            loc=[42.874, -4.598],
            zoom=7,
            track_geo=geojson_data,
            start=start_coords,
            end=end_coords,
            instructions=instructions,
            gpx_data=gpx_data
        )

    except Exception as e:
        flash("An error has been encountered:<br/>" + str(e), category="error")
        return render_template('maps/page_with_map.html', name="No map to display")

@bp.route('/am/map_gl1')
def map_gl1():
    import geocoder

    try:
        position = geocoder.ip('me')

        if not position.ok or not position.latlng:
            flash("Unable to retrieve your position from IP address", category="error")
            return render_template('maps/page_with_map.html', name="No map to display")

        lat, lon = position.latlng

        m = folium.Map(location=[lat, lon], zoom_start=14)

        folium.Marker(
            location=[lat, lon],
            tooltip="I",
            popup=f"I'm here!<br>[{lat:.5f}, {lon:.5f}]",
            icon=folium.Icon(icon="user"),
        ).add_to(m)

        return render_template('maps/page_with_map.html', 
            name="Map with geolocation via IP address (server side)", 
            map_html=m._repr_html_())

    except Exception as e:
        flash("An error has been encountered:<br/>" + str(e), category="error")
        return render_template('maps/page_with_map.html', name="No map to display")

@bp.route('/am/map_gl2')
def map_gl2():
    return render_template('maps/page_with_leaflet_map_for_geoloc2.html', 
        name="Map with geolocation via IP address (client side)")

@bp.route('/am/map_gl3')
def map_gl3():
    return render_template('maps/page_with_leaflet_map_for_geoloc3.html', 
        name="Map with geolocation via the browser’s geolocation API")

@bp.route('/am/map_measure1')
def map_measure1():
    return render_template('maps/page_with_leaflet_map_for_measure1.html', 
        name="Map for measuring distances and areas")

@bp.route('/am/map_measure2')
def map_measure2():

    leaflet_script = """
        <style>
        .info.legend {
            background-color: white;
            padding: 10px;
            border: 2px solid black;
            border-radius: 5px;
            box-shadow: 0 0 15px rgba(0,0,0,0.2);
        }
        </style>
        
        <script src="https://cdn.jsdelivr.net/npm/@turf/turf@6/turf.min.js"></script>  
        <script type="text/javascript">
        window.onload = function() {
            var map;
            for (var key in window) {
                if (window[key] instanceof L.Map) {
                    map = window[key];
                    break;
                }
            }
            try {
                const legend = L.control({position: 'bottomleft'});
                legend.onAdd = function(map) {
                    const div = L.DomUtil.create('div', 'info legend');

                    div.innerHTML += `<strong>Distance and area measurement:</strong><br>`;
                    div.innerHTML += `- To measure a distance, draw a polyline by clicking two or more points on the map<br>`;
                    div.innerHTML += `- To close a polyline into a polygon and display its perimeter and area, press 'C'<br>`;
                    div.innerHTML += `- To finish the current measurement and start a new one, press 'R'`;

                    return div;
                };

                legend.addTo(map);

                let points = []; 
                let circleMarkers = [];
                let polyline = null;
                let polygon = null;
                let dist = 0;

                map.on('click', function(e) {
                    if (!polygon) {
                        const latlng = e.latlng;

                        points.push(latlng);

                        const newCircleMarker = L.circleMarker(latlng, {radius: 5}).addTo(map);
                        circleMarkers.push(newCircleMarker);

                        if (points.length === 1) {
                            polyline = L.polyline(points).addTo(map);

                            dist = 0;
                        } else {
                            polyline.addLatLng(latlng);

                            dist = dist + haversine(points[points.length - 2], points[points.length - 1])

                            newCircleMarker.bindPopup(`Length: ${dist.toFixed(3)} miles`)
                            .openPopup();
                        }
                    }
                });

                document.addEventListener('keydown', function(e) {    
                    const key = (e.key || '').toLowerCase();
                    if (key === 'r') {
                        if (polyline) polyline.remove();
                        if (polygon) polygon.remove();
                        for (let marker of circleMarkers) marker.remove();

                        points = [];
                        circleMarkers = [];
                        polygon = null;
                    } else if (key === 'c' && !polygon && points.length > 2) {
                        dist = dist + haversine(points[points.length - 1], points[0]);

                        polygon = L.polygon(points).addTo(map);
                        polyline.remove();

                        const geojson = polygon.toGeoJSON();
                         //const perimeter = turf.length(geojson, { units: "miles" });
                        const area = turf.area(geojson) / (1609.344 * 1609.344);

                        polygon.bindPopup(`<strong>Perimeter:</strong> ${dist.toFixed(3)} miles<br/><strong>Area:</strong> ${area.toFixed(3)} square miles`)
                        .openPopup();
                    }
                });

            } catch(e) {    
                if (typeof map !== 'undefined' && map) {map.remove();}

                const div = document.getElementById("map")
                if (div) {div.remove();}
        
                const elemDiv = document.createElement('div');
                elemDiv.innerHTML = `<p>${e}</p>`;
                document.body.appendChild(elemDiv);
            }

            function haversine(latlng1, latlng2) {
                //const R = 6371; // Earth's radius in kilometers
                const R = 3959; // Earth's radius in miles

                const toRad = angle => angle * Math.PI / 180;

                const dLat = toRad(latlng2.lat - latlng1.lat);
                const dLon = toRad(latlng2.lng - latlng1.lng);

                const phi1 = toRad(latlng1.lat);
                const phi2 = toRad(latlng2.lat);

                const a = Math.sin(dLat / 2) ** 2 +
                    Math.cos(phi1) * Math.cos(phi2) *
                    Math.sin(dLon / 2) ** 2;

                const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

                return R * c; // distance in miles
            }
        };
        </script>
    """

    try:
        m = folium.Map(location=[38, -100], zoom_start=5)

        m.get_root().html.add_child(folium.Element(leaflet_script))

        return render_template('maps/page_with_map.html', 
            name="Map for measuring distances and areas (built with Folium)", 
            map_html=m._repr_html_())

    except Exception as e:
        flash("An error has been encountered:<br/>" + str(e), category="error")
        return render_template('maps/page_with_map.html', name = "No map to display")

@bp.route('/proxy', methods=['GET', 'POST'])
def proxy():
    from flask import jsonify, Response
    import requests

    try:
        target_url = request.args.get('url')
        if not target_url:
            return jsonify({'error': 'Missing URL parameter'}), 400

        # Forward headers (optional: include your app's User-Agent)
        headers = {
            "User-Agent": "MyApp/1.0 (myemail@example.com)"
        }

        # Forward GET or POST data
        if request.method == 'POST':
            resp = requests.post(target_url, data=request.get_data(), headers=headers)
        else:
            resp = requests.get(target_url, headers=headers, params=request.args.to_dict(flat=True))

        # Return the response content and status, preserving its content type
        return Response(
            resp.content,
            status=resp.status_code,
            content_type=resp.headers.get('Content-Type', 'application/json')
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    