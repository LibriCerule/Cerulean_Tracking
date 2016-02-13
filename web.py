#!/usr/bin/python
import sys

from flask import Flask
from flask import render_template
from flask import request

from tracker_database import TrackerDatabase
from directions import Directions

app = Flask(__name__)
#app.debug=True
#app.run(host='0.0.0.0')
database = TrackerDatabase("package.db")
directions = Directions("gmapskey")

@app.route("/calculatedistancetime", methods=['GET'])
def calculate_distance_time():
    uuid = request.args.get('uuid')
    destinfo = database.get_package(uuid)
    currentinfo = database.get_package_updates(uuid)
    if len(currentinfo) <= 0:
        return "None"

    return "{" + ",".join(directions.getData((destinfo[2], destinfo[3]),(currentinfo[-1][1], currentinfo[-1][2]))) + "}"


@app.route("/getpackageofuser", methods=['GET'])
def get_package_of_user():
    username = request.args.get('username')
    packages = database.get_package_of_user(username)
    return "{" + ",".join(content[0] for content in packages) + "}"

@app.route("/package", methods=['GET'])
def package_get():
    uuid = request.args.get('uuid')
    package = database.get_package(uuid)
    return "{\"uuid\":%s, \"name\":%s, \"lat\":%s, \"lon\":%s, \"delivered\":%s}" %(package[0], package[1], package[2], package[3], package[4])

@app.route("/getpackageupdates", methods=['GET'])
def get_package_updates():
    uuid = request.args.get('uuid')
    package = database.get_package_updates(uuid)
    json_out = "{"
    json_out += ",".join("{\"uuid\":%s, \"lat\":%s, \"lon\":%s, \"timestamp\":%s}" %(update[0], update[1], update[2], update[3]) for update in package)
    json_out += "}"
    return json_out


@app.route("/registerpackagetouser", methods=['POST'])
def register_package_to_user():
    uuid = request.form['uuid']
    username = request.form['username']
    database.register_package_to_user(username, uuid)
    return "Created", 201

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
    return "{\"ackUUID\":\"%s\"}" %(name)

@app.route("/register", methods=['POST'])
def register():
    if all(query in request.form.keys() for query in ['username', 'password']):
        username = request.form['username']
        password_hash = request.form['password']
        if database.register_user(username, password_hash):
            return "Created", 201
        else:
            return "Failed", 400
    return "Failed", 406


@app.route("/login", methods=['POST'])
def login():
    if all(query in request.form.keys() for query in ['username', 'password']):
        attempt = database.login(request.form['username'], request.form['password'])
        return attempt
    return "Failed to log in", 403

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python web.py [IP address]")
        exit(1)

    app.run(host=sys.argv[1])
