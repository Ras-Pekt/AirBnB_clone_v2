#!/usr/bin/python3
"""
a script that starts a Flask web application
/: displays Hello HBNB!
/hbnb: displays HBNB
/c/<text>: displays “C ” followed by the value of the text variable
/python/<text>: displays “Python ”, followed by the value of the text variable
/number/<n>: display n is a number
/number_template/<n>: display a HTML page
"""

from flask import Flask, render_template
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
    return f"c {escape(text)}"


@app.route("/python", strict_slashes=False)
@app.route("/python/", strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def python_route(text="is cool"):
    """
    displays the python route
    """
    text = text.replace("_", " ")
    return f"Python {escape(text)}"


@app.route("/number/<int:n>", strict_slashes=False)
def number_route(n):
    """
    displays the number route
    """
    return f"{n} is a number"


@app.route("/number_template/<int:n>", strict_slashes=False)
def number_template_route(n):
    """
    displays the number_template route
    """
    return render_template("5-number.html", n=n)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
