#!/usr/bin/python3
"""
//cities_by_states: display a HTML page of cities by state
"""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route("/cities_by_states", strict_slashes=False)
def cities_by_states_route():
    """
    displays the cities_by_states_list route
    """
    states = storage.all(State)
    print(f"STATES: {states}")
    return render_template("8-cities_by_states.html", states=states)


@app.teardown_appcontext
def remove_session(e):
    """
    removes the current SQLAlchemy Session
    """
    storage.close()


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000)
