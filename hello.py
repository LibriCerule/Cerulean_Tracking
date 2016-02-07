from flask import Flask
import sys

app = Flask(__name__)
#app.debug=True
#app.run(host='0.0.0.0')

@app.route("/")
def index():
    return "Hello world"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python hello.py [IP address]")
        exit(1)

    app.run(host=sys.argv[1])
