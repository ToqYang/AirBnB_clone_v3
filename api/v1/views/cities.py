#!/usr/bin/python3
""" Class city that contain the cities """
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route("/states/<state_id>/cities", strict_slashes=False)
def cities_for_id(state_id):
    """Return a JSON list of states"""
    if not state_id:
        abort(404)
    cities = storage.all("City")
    list_cities = []
    for key, val in cities.items():
        if val.to_dict()['state_id'] == state_id:
            list_cities.append(val.to_dict())
    if len(list_cities) == 0:
        abort(404)
    return jsonify(list_cities)


@app_views.route("/cities/<city_id>")
def list_city(city_id):
    """Return a JSON list of cities"""
    cities = storage.get("City", city_id)
    if cities is None:
        abort(404)
    return jsonify(cities.to_dict())


@app_views.route("/cities/<city_id>", methods=['DELETE'])
def delete_cities(city_id):
    """Return a JSON list of states"""
    cities = storage.get("City", city_id)
    if cities is None:
        abort(404)
    storage.delete(cities)
    storage.save()

    return jsonify({}), 200


@app_views.route("states/<state_id>/cities", methods=['POST'])
def post_cities(state_id):
    """Return a JSON list of states"""
    json = request.get_json()
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    if not json:
        return "Not a JSON", 404
    if 'name' not in json:
        return "Missing name", 404
    json['state_id'] = state_id
    new_city = City(**json)
    storage.new(new_city)
    storage.save()

    return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=['PUT'])
def update_cities(city_id):
    """Return a JSON list of states"""
    json = request.get_json()
    if not json:
        return "Not a JSON", 404
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    new_dict = city.to_dict()
    for k, v in json.items():
        setattr(city, k, v)
    storage.save()

    return jsonify(city.to_dict()), 200
