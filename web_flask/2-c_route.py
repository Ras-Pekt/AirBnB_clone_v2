#!/usr/bin/python3
"""
a script that starts a Flask web application
/: displays Hello HBNB!
/hbnb: displays HBNB
/c/<text>: display “C ” followed by the value of the text variable
"""

from flask import Flask
from markupsafe import escape

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


@app.route("/c/<text>", strict_slashes=False)
def c_route(text):
    """
    displays the c route
    """
    text = text.replace("_", " ")
    return f"C {escape(text)}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
