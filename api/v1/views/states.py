#!/usr/bin/python3
"""
Description of each state and the responses
"""

from flask import jsonify, abort, request, make_response
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
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", methods=['DELETE'])
def delete_state(state_id):
    """Return a JSON list of states"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()

    return jsonify({})


@app_views.route("/states/", methods=['POST'])
def post_state():
    """Return a JSON list of states"""
    json = request.get_json()
    if not json:
        return make_response(jsonify({"Not a JSON"}), 400)
    if 'name' not in json:
        return make_response(jsonify({"Misssing name"}), 400)
    new_state = State(**json)
    storage.new(new_state)
    storage.save()

    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=['PUT'])
def update_state(state_id):
    """Return a JSON list of states"""
    json = request.get_json()
    if not json:
        return make_response(jsonify({"Not a JSON"}), 400)
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    new_dict = state.to_dict()
    for k, v in json.items():
        if k == 'id' or k == 'created_at' or k == 'update_ati':
            pass
        else:
            setattr(state, k, v)
    storage.save()

    return jsonify(state.to_dict()), 200
