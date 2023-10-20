#!/usr/bin/python3
"""
a script that starts a Flask web application
/: displays Hello HBNB!
/hbnb: displays HBNB
"""

from flask import Flask

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_route():
    """
    displays the home route
    """
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb_route():
    """
    displays the hbnb route
    """
    return "HBNB"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
