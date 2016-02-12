#!/usr/bin/python
from flask import Flask
from flask import render_template
from flask import request
import sys

from tracker_database import TrackerDatabase

app = Flask(__name__)
#app.debug=True
#app.run(host='0.0.0.0')
database = TrackerDatabase("package.db")

@app.route("/package", methods=['GET'])
def package_get():

    uuid = request.values.getlist('uuid')
    if (len(uuid) <= 0):
        return "PLACEHOLDER"

    return str(uuid)

@app.route("/packagetrackupdate/<uuid>", methods=['POST'])
def package_track_update(uuid):
#    request.args.post()
    lat = None
    lon = None
    ele = None
    time = None
    delivered = None
    if all(query in request.form.keys() for query in ['lat', 'lon', 'ele', 'time']):
        lat = request.form['lat']
        lon = request.form['lon']
        ele = request.form['ele']  # Is this needed?
        time = request.form['time']
        database.track_new_package(uuid, lat, lon, time)
        return "Created", 201
    elif 'delivered' in request.form.keys():
        delivered = request.form['delivered']
        database.track_new_package(uuid, delivered)
        return "Created", 201
    return "Failed", 400

@app.route("/tracknewpackage", methods=['GET'])
def track_new_package():
    name = request.args.get('name')
    uuid = request.args.get('uuid')
    latitude = request.args.get('destinationLat')
    longitude = request.args.get('destinationLon')

    database.track_new_package(name, uuid, latitude, longitude)
    return "{\"ackUUID\":\"%s\"" %(name)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python web.py [IP address]")
        exit(1)

    app.run(host=sys.argv[1])
