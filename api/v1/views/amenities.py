#!/usr/bin/python3
""" Class city that contain the cities """
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.amenity import Amenity


@app_views.route("/amenities", strict_slashes=False)
def amenities_for_id():
    """Return a JSON list of states"""
    amenities = storage.all("Amenity")
    list_amenities = []
    for key, val in amenities.items():
        list_amenities.append(val.to_dict())
    if len(list_amenities) == 0:
        abort(404)
    return jsonify(list_amenities)


@app_views.route("/amenities/<amenity_id>")
def list_amenities(amenity_id):
    """Return a JSON list of amenities """
    amenities = storage.get("Amenity", amenity_id)
    if amenities is None:
        abort(404)
    return jsonify(amenities.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'])
def delete_amenities(amenity_id):
    """Return a JSON list of amenities"""
    amenities = storage.get("Amenity", amenity_id)
    if amenities is None:
        abort(404)
    storage.delete(amenities)
    storage.save()

    return jsonify({}), 200


@app_views.route("/amenities", methods=['POST'])
def post_aminities():
    """Return a JSON list of amenities"""
    json = request.get_json()
    if not json:
        abort(404)
    if not json:
        return "Not a JSON", 404
    if 'name' not in json:
        return "Missing name", 404
    new_amenity = Amenity(**json)
    storage.new(new_amenity)
    storage.save()

    return jsonify(new_amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=['PUT'])
def update_amenities(amenity_id):
    """Return a JSON list of states"""
    json = request.get_json()
    if not json:
        return "Not a JSON", 404
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    new_dict = amenity.to_dict()
    for k, v in json.items():
        setattr(amenity, k, v)
    storage.save()

    return jsonify(amenity.to_dict()), 200
