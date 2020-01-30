#!/usr/bin/python3
"""
Class city that contain the cities
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=['GET'],
                 strict_slashes=False)
def cities_for_id(state_id):
    """Return a JSON list of states"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    cities = state.cities
    list_cities = []
    for obj in cities:
        list_cities.append(obj.to_dict())
    return jsonify(list_cities)


@app_views.route("/cities/<city_id>", methods=['GET'], strict_slashes=False)
def list_city(city_id):
    """Return a JSON list of cities"""
    cities = storage.get("City", city_id)
    if cities is None:
        abort(404)
    return jsonify(cities.to_dict())


@app_views.route("/cities/<city_id>", methods=['DELETE'], strict_slashes=False)
def delete_cities(city_id):
    """Return a JSON list of states"""
    cities = storage.get("City", city_id)
    if cities is None:
        abort(404)
    cities.delete(cities)
    storage.save()

    return jsonify({}), 200


@app_views.route("states/<state_id>/cities", methods=['POST'])
def post_cities(state_id):
    """Return a JSON list of states"""
    json = request.get_json()
    if not json:
        abort(400, {'Not a JSON'})
    if 'name' not in json:
        abort(400, {'Missing name'})
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    new_city = City(name=json['name'], state_id=state_id)
    storage.new(new_city)
    storage.save()

    return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=['PUT'], strict_slashes=False)
def update_cities(city_id):
    """Return a JSON list of states"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    json = request.get_json()
    if not json:
        abort(400, {'Not a JSON'})
    new_dict = city.to_dict()
    for k, v in json.items():
        if k == 'id' or k == 'created_at' or k == 'updated_at':
            pass
        else:
            setattr(city, k, v)
    storage.save()

    return jsonify(city.to_dict()), 200
