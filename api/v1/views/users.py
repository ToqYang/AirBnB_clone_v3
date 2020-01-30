#!/usr/bin/python3
""" Class User that contain the users """
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route("/users", strict_slashes=False)
def list_users():
    """Return a JSON list of users """
    users = storage.all("User")
    list_users = []
    for key, val in users.items():
        list_users.append(val.to_dict())
    return jsonify(list_users)


@app_views.route("/users/<user_id>")
def list_users_id(user_id):
    """Return a JSON list of user """
    users = storage.get("User", user_id)
    if users is None:
        abort(404)
    return jsonify(users.to_dict())


@app_views.route("/users/<user_id>", methods=['DELETE'])
def delete_users(user_id):
    """ Return a JSON list of users """
    users = storage.get("User", users_id)
    if users is None:
        abort(404)
    storage.delete(users)
    storage.save()

    return jsonify({}), 200


@app_views.route("/users", methods=['POST'])
def post_users():
    """ Return a JSON list of users """
    json = request.get_json()
    if not json:
        abort(404)
    if not json:
        return "Not a JSON", 404
    if 'email' not in json:
        return "Missing email", 404
    if 'password' not in json:
        return "Missing password", 404
    new_users = User(email=json['email'],
                     password=json['password'],
                     first_name=json['first_name'])
    storage.new(new_users)
    storage.save()

    return jsonify(new_users.to_dict()), 201


@app_views.route("/users/<user_id>", methods=['PUT'])
def update_users(user_id):
    """Return a JSON list of users """
    json = request.get_json()
    if not json:
        abort(400, {'Not a JSON'})
    users = storage.get("User", user_id)
    if users is None:
        abort(404)
    new_dict = users.to_dict()
    for k, v in json.items():
        if k == 'id' or k == 'email' or k == 'created_at' or k == 'updated_at':
            pass
        else:
            setattr(users, k, v)
    storage.save()

    return jsonify(users.to_dict()), 200
