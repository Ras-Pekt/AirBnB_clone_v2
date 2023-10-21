#!/usr/bin/python3
"""
/states/<id>: displays a HTML page of a state by id
"""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route("/states", strict_slashes=False)
@app.route("/states/<id>", strict_slashes=False)
def states_route(id=None):
    """
    displays the states_list route, or
    the states by id route
    """
    states = storage.all(State)
    if id:
        for state in states.values():
            if state.id == id:
                return render_template("9-states.html", state=state)
        return render_template("9-states.html", state="Not found!")
    else:
        return render_template("7-states_list.html", states=states)


# @app.route("/states/<id>", strict_slashes=False)
# def states_id_route(id):
#     """
#     displays the states by id route
#     """
#     states = storage.all(State)
#     for state in states.values():
#         if state.id == id:
#             return render_template("9-states.html", state=state)
#     return render_template("9-states.html", state="Not Found")


@app.teardown_appcontext
def remove_session(e):
    """
    removes the current SQLAlchemy Session
    """
    storage.close()


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000)
