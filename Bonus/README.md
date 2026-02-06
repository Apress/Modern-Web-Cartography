<h1>Route Planner example</h1>
<p>Route_planner.html is a small <strong>route-planning application</strong>. It is designed to enable hikers, cyclists, and even motorists to plan their trip by plotting a route on a map.</p>
<p>This application is also a <strong>GPX editor</strong>: the route can be exported as a GPX file and then used with GPS devices or mobile navigation apps such as OsmAnd or Locus.</p>
<p>This example is more complex than those included in the book, although it uses the same techniques: <strong>Leaflet</strong> to render the map and the route, <strong>Nominatim</strong> to locate places from their addresses, <strong>BRouter</strong> to plan routes between locations, and the browser’s <strong>Geolocation API</strong> to determine the user’s position. The entire application is contained in a single HTML file and can be run simply by opening it in a web browser.</p>
<p>In this tool, <strong>a route</strong> consists of:</p>
<ul>
<li><strong>One or more stages</strong>. A stage represents a journey planned to be completed in one go or in a single day. It consists of:
<ul>
<li><strong>A starting point, an end point, and optional waypoints</strong>. These points are rendered on the map using <strong>circle markers</strong>.</li>
<li><strong>One or more sections</strong>. A section is a path (curved or straight) connecting two points of a stage. Sections are rendered on the map using <strong>polylines</strong>. Their position and shape are calculated using BRouter or by drawing a straight segment, depending on the selected option.</li>
</ul>
</ul>
<p>The tool provides functions to create, modify, and delete stages, as well as their points and sections.</p>
<p>A key feature of this example is its extensive use of <strong>event handlers</strong> attached to various objects: the map, circle markers, and polylines. Depending on the context (stage editing mode or supervision mode), the required event handlers differ, and most of them cannot be assigned once and for all. Instead, they must <strong>registered</strong>, in order to be dynamically <strong>retrieved</strong>, <strong>removed</strong>, and <strong>replaced</strong> by others as the context changes.</p>
<br/>
<p>Patrick MARIE</p>
