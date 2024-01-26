from flask import Flask, render_template, jsonify, request
import json
import requests


import requests
import json

# Function to get directions from Google Maps API
def get_directions(start_lat, start_lon, end_lat, end_lon, api_key):
    # Define the endpoint and parameters
    endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
    params = {
        'origin': f'{start_lat},{start_lon}',
        'destination': f'{end_lat},{end_lon}',
        'key': api_key
    }
    
    # Make a request to the Google Maps API
    response = requests.get(endpoint, params=params)
    directions = response.json()
    
    # Extract polyline points from the first route, first leg, and steps
    polyline_points = []
    if directions["status"] == "OK":
        steps = directions['routes'][0]['legs'][0]['steps']
        for step in steps:
            start_location = (step['start_location']['lat'], step['start_location']['lng'])
            end_location = (step['end_location']['lat'], step['end_location']['lng'])
            polyline_points.append(start_location)
            polyline_points.append(end_location)
    else:
        print(f"Error from Google Maps API: {directions['status']}")
    return polyline_points


app = Flask(__name__)

@app.route('/')
def index():
    # Render the HTML page
    return render_template('map_view.html')  # assuming you've named your HTML file index.html

@app.route('/directions', methods=['POST'])
def directions():

    with open('map.json') as f:
        data = json.load(f)
    # Extract start and end points from POST request
    start_lat = request.json['start_lat']
    start_lon = request.json['start_lon']
    end_lat = request.json['end_lat']
    end_lon = request.json['end_lon']

    # Call the get_directions function (make sure to include your implementation)
    route_points = get_directions(start_lat, start_lon, end_lat, end_lon, "AIzaSyDULzUGZSaiiYhQ156jjOi4iicO-r9p7CY")

    # Return the polyline points as JSON
    return jsonify(route_points)

if __name__ == '__main__':
    app.run(debug=True)
