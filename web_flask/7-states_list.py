#!/usr/bin/python3
"""
/states_list: display a HTML page
"""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route("/states_list", strict_slashes=False)
def states_route():
    """
    displays the states_list route
    """
    states = storage.all(State)
    print(f"STATES: {states}")
    return render_template("7-states_list.html", states=states)


@app.teardown_appcontext
def remove_session(e):
    """
    removes the current SQLAlchemy Session
    """
    storage.close()


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000)
