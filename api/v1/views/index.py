#!/usr/bin/python3
""" Index file that contain the json
    status code """
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status")
def status():
    """Return status of api"""
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def stats():
    """Stats route"""
    return jsonify({
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    })
