#!/usr/bin/python3
"""
 Description of each state and the responses
"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states", strict_slashes=False)
def list_states():
    """Return a JSON list of states"""
    states = storage.all("State")
    list_state = []
    for key, val in states.items():
        list_state.append(val.to_dict())
    return jsonify(list_state)


@app_views.route("/states/<state_id>")
def states_for_id(state_id):
    """Return a JSON list of states"""
    states = storage.all("State")
    list_state = []
    for key, val in states.items():
        if val.to_dict()['id'] == state_id:
            list_state.append(val.to_dict())
    if len(list_state) == 0:
        abort(404)
    return jsonify(list_state)


@app_views.route("/states/<state_id>", methods=['DELETE'])
def delete_state(state_id):
    """Return a JSON list of states"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()

    return jsonify({})


@app_views.route("/states/", methods=['POST'])
def post_state():
    """Return a JSON list of states"""
    json = request.get_json()
    if not json:
        return "Not a JSON", 404
    if 'name' not in json:
        return "Missing name", 404
    new_state = State(**json)
    storage.new(new_state)
    storage.save()

    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=['PUT'])
def update_state(state_id):
    """Return a JSON list of states"""
    json = request.get_json()
    if not json:
        return "Not a JSON", 404
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    new_dict = state.to_dict()
    for k, v in json.items():
        setattr(state, k, v)
    storage.save()

    return jsonify(state.to_dict()), 200
