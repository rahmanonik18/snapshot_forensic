from flask import Flask, request, jsonify, session, render_template, redirect, url_for, flash
from flask import make_response
import requests
import json
from datetime import datetime


app = Flask(__name__)

@app.route('/')
def index():
    with open('map.json', 'r') as file:
        json_data = json.load(file)
        trips = json_data['data']['trips']

        for trip in trips:
            trip['start_time'] = datetime.fromtimestamp(trip['start_time']).strftime('%Y-%m-%d %H:%M:%S')
            trip['end_time'] = datetime.fromtimestamp(trip['end_time']).strftime('%Y-%m-%d %H:%M:%S')
        
        trips.sort(key=lambda x: x['start_time'], reverse=True)

        return render_template('map_view.html', trips=trips)
    
@app.route('/tripDetails', methods=['POST'])
def tripDetails():
    data = request.json
    rowIndex = data['rowIndex']
    with open('map.json', 'r') as file:
        json_data = json.load(file)
        trips = json_data['data']['trips']
        for trip in trips:
            trip['start_time'] = datetime.fromtimestamp(trip['start_time']).strftime('%Y-%m-%d %H:%M:%S')
            trip['end_time'] = datetime.fromtimestamp(trip['end_time']).strftime('%Y-%m-%d %H:%M:%S')
        trips.sort(key=lambda x: x['start_time'], reverse=True)
    
    selected_trip = trips[rowIndex - 1]
    trip_info = {
        "start_time": selected_trip["start_time"],
        "start_location": selected_trip["start_location"],
        "end_location": selected_trip["end_location"],
        "end_time": selected_trip["end_time"],
        "start_latitude": selected_trip["start_latitude"],
        "start_longitude": selected_trip["start_longitude"],
        "end_latitude": selected_trip["end_latitude"],
        "end_longitude": selected_trip["end_longitude"],
        "events": selected_trip.get("events", [])
    }
    print(trip_info)
    return jsonify(trip_info)

if __name__ == '__main__':
    app.run(debug=True)
