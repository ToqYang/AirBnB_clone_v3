#!/usr/bin/python3
"""
Place crud
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place


@app_views.route("/cities/<city_id>/places", methods=['GET'],
                 strict_slashes=False)
def places_for_city_id(city_id):
    """Return a JSON list of places"""
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    places = city.places
    list_places = []
    for obj in places:
        list_places.append(obj.to_dict())
    return jsonify(list_places)


@app_views.route("/places/<place_id>", methods=['GET'], strict_slashes=False)
def list_places(place_id):
    """Return a JSON list of places"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_places(place_id):
    """Return a JSON list of places"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route("cities/<city_id>/places", methods=['POST'],
                 strict_slashes=False)
def post_places(city_id):
    """Return a JSON list of places"""
    json = request.get_json()
    if not json:
        abort(400, 'Not a JSON')
    if 'name' not in json:
        abort(400, 'Missing name')
    if 'user_id' not in json:
        abort(400, 'Missing user_id')
    user = storage.get('User', json['user_id'])
    if user is None:
        abort(404)
    new_place = Place(name=json['name'], city_id=state_id,
                      user_id=json['user_id'])
    storage.new(new_place)
    storage.save()

    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=['PUT'], strict_slashes=False)
def update_places(place_id):
    """Return a JSON places update"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    json = request.get_json()
    if not json:
        abort(400, 'Not a JSON')
    new_dict = place.to_dict()
    for k, v in json.items():
        if k in ['id', 'created_at', 'updated_at', 'user_id', 'city_id']:
            pass
        else:
            setattr(place, k, v)
    storage.save()

    return jsonify(place.to_dict()), 200
