import json
import folium
# Load data
with open('map.json') as f:
  data = json.load(f)


# Define color schemes for kinds and types
kind_colors = {
    'CALL': 'blue',
    'USAGE': 'green',
    'PHONE_USAGE': 'red',
    'DISTRACTION': 'orange',
    'BRAKE': 'purple',
    # ... add more kinds as needed
}

type_colors = {
    'VALIDPERIOD': 'pink',
    'DANGEROUSMANEUVER': 'black',
    'SPEEDING': 'yellow',
    # ... add more types as needed
}
# Extract coordinates
start_lat = data['start_latitude']
start_lon = data['start_longitude'] 
end_lat = data['end_latitude']
end_lon = data['end_longitude']

event_lats = [event['start_latitude'] for event in data['events']]
event_lons = [event['start_longitude'] for event in data['events']]
# Get event timestamps  
timestamps = [event['start_timestamp'] for event in data['events']]

# Sort events by timestamp
sorted_events = sorted(zip(timestamps, event_lats, event_lons), key=lambda x: x[0])

# Extract coordinates
lats, lons = zip(*[(lat, lon) for _, lat, lon in sorted_events])

# Create map
map = folium.Map(location=[lats[0], lons[0]], zoom_start=12) 

# Add tile layer
folium.TileLayer(
  tiles='https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
  attr='Google',
  name='Google Maps',
  API_key='AIzaSyDULzUGZSaiiYhQ156jjOi4iicO-r9p7CY'
).add_to(map)

# Add start marker
folium.Marker(
  location=[start_lat, start_lon], 
  icon=folium.Icon(color='green')
).add_to(map)

# Add end marker
folium.Marker(
  location=[end_lat, end_lon],
  icon=folium.Icon(color='red')
).add_to(map)

# Add markers for each event
for event in data['events']:
    # Determine color for the marker based on kind and type
    kind = event.get('kind')
    type_ = event.get('type')
    color = kind_colors.get(kind, 'gray')  # Default to gray if kind not found
    # If type has a specific color, override kind color
    if type_ in type_colors:
        color = type_colors[type_]

    # Create marker for the event
    folium.Marker(
        location=[event['start_latitude'], event['start_longitude']],
        icon=folium.Icon(color=color),
        popup=f"Kind: {kind}, Type: {type_}"
    ).add_to(map)

folium.PolyLine(
  locations=list(zip(lats, lons)),
  weight=3,
  color='gray'
).add_to(map)

# Save map
map.save('map.html')


##Progressive Google API Key
##https://maps.googleapis.com/maps/api/js?key=AIzaSyCuGmlcHyK05gGmOQDtvYJgl2ky3yC7cv0&libraries=places




# from flask import Flask, render_template
# import json

# app = Flask(__name__)

# @app.route('/')
# def index():

#   with open('map.json', 'r') as file:
#     data = json.load(file)
#     # Load your data here
#     # data = json.loads(map.json)
#     return render_template('map_view.html', data=data)

# if __name__ == '__main__':
#     app.run(debug=True)
