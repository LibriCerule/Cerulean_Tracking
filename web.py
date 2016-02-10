from flask import Flask
from flask import render_template
from flask import request
import sys

app = Flask(__name__)
#app.debug=True
#app.run(host='0.0.0.0')

@app.route("/package", methods=['GET'])
def package_get():

    uuid = request.values.getlist('uuid')
    if (len(uuid) <= 0):
        return "PLACEHOLDER"

    return str(uuid)

@app.route("/packagetrackupdate/<uuid>", methods=['POST'])
def package_track_update(uuid):
#    request.args.post()
    lat = request.form['lat']
    lon = request.form['lon']
    ele = request.form['ele']
    time = request.form['time']
    
    delivered = request.form['delivered']
    return "PLACEHOLDER"

@app.route("/tracknewpackage", methods=['GET'])
def track_new_package():
    name = request.args.get('name')
    latitude = request.args.get('destinationLat')
    longitude = request.args.get('destinationLon')
    uuid = request.args.get('uuid')

    return "{\"ackUUID\":\"%s\"" %(name)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python hello.py [IP address]")
        exit(1)

    app.run(host=sys.argv[1])
