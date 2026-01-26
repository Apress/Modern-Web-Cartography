import folium
from flask import Blueprint, render_template, request, flash

bp = Blueprint('simple_maps', __name__)

@bp.route('/sm/map0', methods=('GET', 'POST'))
def map0():
    m = folium.Map()
    return render_template('maps/page_with_map.html', 
        name="Hello World!", 
        map_html=m._repr_html_())

@bp.route('/sm/map1', methods=('GET', 'POST'))
def map1():
    try:
        m = folium.Map(location=[36.10250, -115.15579], zoom_start=14)

        return render_template('maps/page_with_map.html', 
            name="Simple map of Las Vegas", 
            map_html=m._repr_html_())
    
    except Exception as e:
        flash("An error has been encountered:<br/>" + str(e), category="error")
        return render_template('maps/page_with_map.html', name="No map to display")

@bp.route('/sm/map2')
def map2():
    try:
        m = folium.Map(
            location=(36.10250, -115.15579), 
            zoom_start=14,
            tiles='https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
            attr='Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)'
        )

        return render_template('maps/page_with_map.html', 
            name="Map of Las Vegas with topographic features", 
            map_html=m._repr_html_())
   
    except Exception as e:
        flash("An error has been encountered:<br/>" + str(e), category="error")
        return render_template('maps/page_with_map.html', name="No map to display")

@bp.route('/sm/map3')
def map3():
    try:
        m = folium.Map(location=[36.10250, -115.15579], zoom_start=14, control_scale=True)
        
        folium.Marker(
            location=[36.11574, -115.17481],
            tooltip="Click me!",
            popup="Caesars Palace",
            icon= folium.Icon(color="red", icon="fa-building", prefix="fa")
        ).add_to(m)

        folium.Marker(
            location=[36.11236, -115.17206],
            tooltip="Click me!",
            popup="Paris Las Vegas",
            icon= folium.Icon(color="red", icon="fa-building", prefix="fa")
        ).add_to(m)

        folium.Marker(
            location=[36.10205, -115.17425],
            tooltip="Click me!",
            popup="New York-New York",
            icon= folium.Icon(color="red", icon="fa-building", prefix="fa")
        ).add_to(m)
        
        folium.Marker(
            location=[36.08421, -115.15333],
            tooltip="Click me!",
            popup="Harry Reid International Airport",
            icon=folium.Icon(color="blue", icon="fa-plane", prefix="fa")
        ).add_to(m)
        
        return render_template('maps/page_with_map.html', 
            name="Map of Las Vegas with markers", 
            map_html=m._repr_html_())

    except Exception as e:
        flash("An error has been encountered:<br/>" + str(e), category="error")
        return render_template('maps/page_with_map.html', name="No map to display")

@bp.route('/sm/map4')
def map4():
    try:
        m = folium.Map(location=[36.10250, -115.15579], zoom_start=14, control_scale=True)
     
        casino_group = folium.FeatureGroup("Casinos hotels").add_to(m)
       
        folium.Marker(
            location=[36.11574, -115.17481],
            tooltip="Click me!",
            popup="Caesars Palace",
            icon= folium.Icon(color="red", icon="fa-building", prefix="fa")
        ).add_to(casino_group)

        folium.Marker(
            location=[36.11236, -115.17206],
            tooltip="Click me!",
            popup="Paris Las Vegas",
            icon= folium.Icon(color="red", icon="fa-building", prefix="fa")
        ).add_to(casino_group)

        folium.Marker(
            location=[36.10205, -115.17425],
            tooltip="Click me!",
            popup="New York-New York",
            icon= folium.Icon(color="red", icon="fa-building", prefix="fa")
        ).add_to(casino_group)
        
        airport_group = folium.FeatureGroup("Airports").add_to(m)
        
        folium.Marker(
            location=[36.08421, -115.15333],
            tooltip="Click me!",
            popup="Harry Reid International Airport",
            icon=folium.Icon(color="blue", icon="fa-plane", prefix="fa")
        ).add_to(airport_group)

        folium.TileLayer(
            tiles='https://{s}.tile-cyclosm.openstreetmap.fr/cyclosm/{z}/{x}/{y}.png',
            attr='<a href="https://github.com/cyclosm/cyclosm-cartocss-style/releases" title="CyclOSM - Open Bicycle render">CyclOSM</a> | Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            name="CyclOSM",
            overlay=False,
            control=True
        ).add_to(m)

        folium.TileLayer(
            tiles='https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
            attr='Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)',
            name="OpenTopoMap",
            overlay=False,
            control=True
        ).add_to(m)   

        folium.LayerControl().add_to(m)

        return render_template('maps/page_with_map.html', 
            name="Map of Las Vegas with marker groups and layer control", 
            map_html=m._repr_html_())

    except Exception as e:
        flash("An error has been encountered:<br/>" + str(e), category="error")
        return render_template('maps/page_with_map.html', name="No map to display")

@bp.route('/sm/map5')
def map5():
    try:
        m = folium.Map(location=[36.10250, -115.15579], zoom_start=14, control_scale=True)
     
        casino_group = folium.FeatureGroup("Casinos hotels").add_to(m)
       
        folium.Marker(
            location=[36.11574, -115.17481],
            tooltip="Click me!",
            popup="Caesars Palace",
            icon= folium.Icon(color="red", icon="fa-building", prefix="fa")
        ).add_to(casino_group)

        folium.Marker(
            location=[36.11236, -115.17206],
            tooltip="Click me!",
            popup="Paris Las Vegas",
            icon= folium.Icon(color="red", icon="fa-building", prefix="fa")
        ).add_to(casino_group)

        folium.Marker(
            location=[36.10205, -115.17425],
            tooltip="Click me!",
            popup="New York-New York",
            icon= folium.Icon(color="red", icon="fa-building", prefix="fa")
        ).add_to(casino_group)
        
        airport_group = folium.FeatureGroup("Airports").add_to(m)
        
        folium.Marker(
            location=[36.08421, -115.15333],
            tooltip="Click me!",
            popup="Harry Reid International Airport",
            icon=folium.Icon(color="blue", icon="fa-plane", prefix="fa")
        ).add_to(airport_group)

        folium.TileLayer(
            tiles='https://{s}.tile-cyclosm.openstreetmap.fr/cyclosm/{z}/{x}/{y}.png',
            attr='<a href="https://github.com/cyclosm/cyclosm-cartocss-style/releases" title="CyclOSM - Open Bicycle render">CyclOSM</a> | Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            name="CyclOSM",
            overlay=False,
            control=True
        ).add_to(m)

        folium.TileLayer(
            tiles='https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
            attr='Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)',
            name="OpenTopoMap",
            overlay=False,
            control=True
        ).add_to(m)   

        folium.raster_layers.ImageOverlay(
            image="prototypes/static/Stratosphere.jpg",
            name="Stratosphere Tower",
            bounds=[ [36.083, -115.1330], [36.113, -115.1131]],
            opacity=0.5,
            alt="Stratosphere Tower",
            control=True
        ).add_to(m)

        folium.LayerControl().add_to(m)

        return render_template('maps/page_with_map.html', 
            name="Map of Las Vegas with image overlay", 
            map_html=m._repr_html_())

    except Exception as e:
        flash("An error has been encountered:<br/>" + str(e), category="error")
        return render_template('maps/page_with_map.html', name="No map to display")

@bp.route('/sm/map6')
def map6():
    try:
        m = folium.Map(location=[ 42.480656, 6.822510], zoom_start=8, control_scale=True)

        line_coordinates = [
            (43.312071, 5.364504),
            (43.297080, 5.357294),
            (43.285398, 5.335579),
            (43.201450, 5.299530),
            (42.350882, 5.927124),
            (41.816822, 8.640747),
            (41.883423, 8.741683),
            (41.906934, 8.756790),
            (41.922220, 8.740825)
        ]

        line_group = folium.FeatureGroup(name="Marseille-Ajaccio route").add_to(m)
        
        folium.PolyLine(line_coordinates, 
            color='blue',
            weight=4,
            opacity=0.7,
            tooltip="Marseille-Ajaccio"
        ).add_to(line_group)

        circle_group = folium.FeatureGroup(name="Blue circle").add_to(m)
        
        folium.Circle(
            location=[43.085840, 7.943115],
            radius=50000,
            stroke=False,
            fill=True,
            fill_color="cornflowerblue",
            fill_opacity=0.6,
            popup="Blue circle 100 km in diameter",
            tooltip="Click me!"
        ).add_to(circle_group)

        locations = [
            [42.163861, 4.916382],
            [42.314335, 5.619507],
            [41.972203, 6.690674],
            [41.496698, 6.503906],
            [41.529605, 5.234985]
        ]           

        polygon_group = folium.FeatureGroup(name="Yellow polygon").add_to(m)
        
        folium.Polygon(
            locations=locations,
            color="orange",
            weight=6,
            opacity=1,
            fill=True,
            fill_color="yellow",
            fill_opacity=0.5,
            popup="Yellow polygon",
            tooltip="Click me!"
        ).add_to(polygon_group)

        folium.LayerControl().add_to(m)

        return render_template('maps/page_with_map.html', 
            name="Map of the Marseille-Ajaccio shipping route", 
            map_html=m._repr_html_())

    except Exception as e:
        flash("An error has been encountered:<br/>" + str(e), category="error")
        return render_template('maps/page_with_map.html', name="No map to display")

@bp.route('/sm/map7')
def map7():
    import requests

    try:
        geojson_data = requests.get(
            "https://raw.githubusercontent.com/python-visualization/folium-example-data/main/world_countries.json"
        ).json()

        m = folium.Map(location=[15, 0], 
            zoom_start=2)

        folium.GeoJson(geojson_data, 
            name="Countries",
            style_function=lambda feature: {
                'color': 'darkgreen',
                'weight': 2,
                'fillColor': 'green',
                'fillOpacity': 0.5
            },
            tooltip= folium.GeoJsonTooltip(fields=['name'], aliases=['Country:'])
        ).add_to(m)

        folium.LayerControl().add_to(m)

        return render_template('maps/page_with_map.html', 
            name="Map of the world with country outlines highlighted", 
            map_html=m._repr_html_())

    except Exception as e:
        flash("An error has been encountered:<br/>" + str(e), category="error")
        return render_template('maps/page_with_map.html', name="No map to display")

@bp.route('/sm/map8')
def map8():
    import requests

    try:
        topojson_data = requests.get(
            "https://cdn.jsdelivr.net/npm/us-atlas@3/counties-10m.json"
        ).json()

        m = folium.Map(location=[37.8, -96], 
            zoom_start=4)

        folium.TopoJson(topojson_data,
            object_path="objects.counties",
            name="US counties",
            style_function=lambda feature: {
                'color': 'green',
                'weight': 2,
                'fillColor': 'lightgreen',
                'fillOpacity': 0.5
            },
            tooltip=folium.GeoJsonTooltip(fields=['name'], aliases=['County:'])
        ).add_to(m)

        folium.LayerControl().add_to(m)

        return render_template('maps/page_with_map.html', 
            name = "Map of the US with county outlines", 
            map_html=m._repr_html_())

    except Exception as e:
        flash("An error has been encountered:<br/>" + str(e), category="error")
        return render_template('maps/page_with_map.html', name = "No map to display")

@bp.route('/sm/map9')
def map9():
    import json, pandas
   
    try:
        with open("prototypes/static/europe.geojson") as f:
            state_geo = json.loads(f.read())
    
        state_data = pandas.read_csv("prototypes/static/EU_median_living_standards.csv")
   
        m = folium.Map(location=[53, 12], zoom_start=4)
   
        folium.Choropleth(
            geo_data= state_geo,
            data=state_data,
            columns=["Country", "2022"],
            key_on="feature.properties.NAME",
            fill_color="YlGn",
            bins=16,
            fill_opacity=0.7,
            line_opacity=0.2,
            name="choropleth",
            legend_name="Median living standards (€)"
        ).add_to(m)
   
        return render_template('maps/page_with_map.html', 
            name="Choropleth map of median living standards in the European Union", 
            map_html=m._repr_html_())
   
    except Exception as e:
        flash("An error has been encountered:<br/>" + str(e), category="error")
        return render_template('maps/page_with_map.html', name="No map to display")

@bp.route('/sm/map10')
def map10():

    leaflet_script = """
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
                map.on('click', function(e) {
                    map.flyTo(e.latlng, map.getZoom() + 1);
                });

                map.on('keydown', function(e) {
                    if (e.originalEvent.key === 'Escape') {
                        map.setZoom(5);
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
        };
        </script>
    """

    try:
        m = folium.Map(location=[21, 80], zoom_start=5)

        m.get_root().html.add_child(folium.Element(leaflet_script))

        return render_template('maps/page_with_map.html', 
            name="Map with interactivity added by injecting Leaflet statements", 
            map_html=m._repr_html_())

    except Exception as e:
        flash("An error has been encountered:<br/>" + str(e), category="error")
        return render_template('maps/page_with_map.html', name = "No map to display")
