from flask import Flask
from flask import render_template
import sys

app = Flask(__name__)
#app.debug=True
#app.run(host='0.0.0.0')

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python hello.py [IP address]")
        exit(1)

    app.run(host=sys.argv[1])
