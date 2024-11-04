from flask import Flask, render_template_string, request, jsonify
import requests

app = Flask(__name__)

# Replace with your actual Mapillary API key
MAPILLARY_API_KEY = "MLY|8608659509183618|6726200e78d0bf6073f8909d83f519b8"

@app.route('/')
def home():
    # HTML template with enhanced features using free APIs
    html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Enhanced Free Map Application</title>
        <style>
            /* Basic flat UI styling */
            body, html {{
                margin: 0;
                padding: 0;
                height: 100%;
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
            }}
            
            #map {{
                height: 100vh;
                width: 100%;
            }}

            #controls {{
                position: absolute;
                top: 20px;
                left: 20px;
                z-index: 5;
                background: white;
                padding: 10px;
                border-radius: 8px;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
                font-size: 14px;
            }}

            .btn {{
                background-color: #007bff;
                color: white;
                padding: 8px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                margin-right: 5px;
                margin-top: 5px;
            }}

            .btn:hover {{
                background-color: #0056b3;
            }}

            #searchBar {{
                width: 200px;
                padding: 5px;
                margin-right: 5px;
            }}
        </style>

        <!-- Leaflet.js for OpenStreetMap integration -->
        <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
        <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
        
        <!-- Mapillary JS SDK for street-level imagery -->
        <script src="https://unpkg.com/mapillary-js@4.0.0-beta.12/dist/mapillary.min.js"></script>
    </head>
    <body>

        <div id="controls">
            <input type="text" id="searchBar" placeholder="Search location" />
            <button class="btn" onclick="searchLocation()">Search</button>
            <button class="btn" onclick="toggleMapillary()">Toggle Mapillary View</button>
        </div>
        <div id="map"></div>

        <script>
            let map;
            let mapillaryViewer = null;
            const defaultLocation = [6.9669852, 121.9476747]; // Example coordinates
            const mapillaryApiKey = "{MAPILLARY_API_KEY}";
            let markers = [];
            let mapillaryActive = false;

            // Initialize the Leaflet map with OpenStreetMap tiles
            function initializeLeafletMap() {{
                map = L.map('map').setView(defaultLocation, 15);
                L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                    maxZoom: 19,
                    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                }}).addTo(map);

                // Add a default marker
                addMarker(defaultLocation, "Default Location");
                loadLandmarks(defaultLocation);
            }}

            // Function to add a marker to the map
            function addMarker(latlng, popupText) {{
                const marker = L.marker(latlng).addTo(map)
                    .bindPopup(popupText)
                    .on('click', () => {{
                        map.flyTo(latlng, 18);
                    }});
                markers.push(marker);
            }}

            // Function to initialize Mapillary viewer
            function initializeMapillaryViewer() {{
                if (mapillaryViewer) return;
                mapillaryViewer = new Mapillary.Viewer(
                    'map',
                    mapillaryApiKey,
                    null
                );
            }}

            // Toggle Mapillary Street View
            function toggleMapillary() {{
                if (mapillaryActive) {{
                    mapillaryViewer.remove();
                    mapillaryViewer = null;
                    document.getElementById("map").innerHTML = "";  // Clear Mapillary container
                    initializeLeafletMap();
                    mapillaryActive = false;
                }} else {{
                    if (map) {{
                        map.remove();
                        map = null;
                    }}
                    initializeMapillaryViewer();
                    loadNearestMapillaryImage(defaultLocation);
                    mapillaryActive = true;
                }}
            }}

            // Function to load the nearest Mapillary image
            function loadNearestMapillaryImage(location) {{
                const url = `https://graph.mapillary.com/images?fields=id&closeto={{location[1]}},{{location[0]}}&radius=100&limit=1&access_token={{mapillaryApiKey}}`;
                fetch(url)
                    .then(response => response.json())
                    .then(data => {{
                        if (data.data && data.data.length > 0) {{
                            const imageKey = data.data[0].id;
                            mapillaryViewer.setImage(imageKey);
                        }} else {{
                            alert("No Mapillary street view images available near this location.");
                        }}
                    }})
                    .catch(error => console.error("Error loading Mapillary image:", error));
            }}

            // Function to search for a location using Nominatim
            function searchLocation() {{
                const query = document.getElementById('searchBar').value;
                if (!query) {{
                    alert("Please enter a location to search.");
                    return;
                }}
                const url = `https://nominatim.openstreetmap.org/search?format=json&q={{encodeURIComponent(query)}}&limit=1`;
                fetch(url)
                    .then(response => response.json())
                    .then(data => {{
                        if (data && data.length > 0) {{
                            const lat = parseFloat(data[0].lat);
                            const lon = parseFloat(data[0].lon);
                            const displayName = data[0].display_name;
                            if (mapillaryActive) {{
                                // If Mapillary is active, load the nearest image
                                loadNearestMapillaryImage([lat, lon]);
                            }} else {{
                                map.setView([lat, lon], 15);
                                addMarker([lat, lon], displayName);
                            }}
                        }} else {{
                            alert("Location not found.");
                        }}
                    }})
                    .catch(error => console.error("Error during geocoding:", error));
            }}

            // Function to fetch and display landmarks using Overpass API
            function loadLandmarks(location) {{
                const overpassUrl = "https://overpass-api.de/api/interpreter";
                const query = `
                    [out:json];
                    (
                        node["tourism"="museum"]({{bbox}});
                        node["amenity"="park"]({{bbox}});
                        node["amenity"="restaurant"]({{bbox}});
                        node["historic"="monument"]({{bbox}});
                        node["shop"]({{bbox}});
                    );
                    out center;
                `;
                const bbox = getBoundingBox(location, 1500); // 1.5 km radius
                const finalQuery = query.replace("{{bbox}}", bbox);
                fetch(overpassUrl, {{
                    method: "POST",
                    body: finalQuery
                }})
                .then(response => response.json())
                .then(data => {{
                    if (data.elements && data.elements.length > 0) {{
                        data.elements.forEach(element => {{
                            const lat = element.lat;
                            const lon = element.lon;
                            let name = element.tags.name || "Unnamed";
                            let type = "";
                            if (element.tags.tourism === "museum") {{
                                type = "Museum";
                            }} else if (element.tags.amenity === "park") {{
                                type = "Park";
                            }} else if (element.tags.amenity === "restaurant") {{
                                type = "Restaurant";
                            }} else if (element.tags.historic === "monument") {{
                                type = "Monument";
                            }} else if (element.tags.shop) {{
                                type = "Shop";
                            }}
                            addMarker([lat, lon], `{{type}}: {{name}}`);
                        }});
                    }}
                }})
                .catch(error => console.error("Error fetching landmarks:", error));
            }}

            // Function to calculate bounding box for Overpass query
            function getBoundingBox(location, radius) {{
                const lat = location[0];
                const lon = location[1];
                const R = 6378.1; // Radius of the Earth in km
                const dLat = (radius / 1000) / R * (180 / Math.PI);
                const dLon = (radius / 1000) / (R * Math.cos(lat * Math.PI / 180)) * (180 / Math.PI);
                const south = lat - dLat;
                const north = lat + dLat;
                const west = lon - dLon;
                const east = lon + dLon;
                return `${{south}},${{west}},${{north}},${{east}}`;
            }}

            // Initialize the map and additional features
            initializeLeafletMap();

        </script>
    </body>
    </html>
    """
    return render_template_string(html_template)

if __name__ == '__main__':
    app.run(debug=True)
