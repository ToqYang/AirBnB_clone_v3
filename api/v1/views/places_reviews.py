#!/usr/bin/python3
"""
Reviews CRUD
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.review import Review


@app_views.route("/places/<place_id>/reviews", methods=['GET'],
                 strict_slashes=False)
def review_for_place_id(place_id):
    """Return a JSON list of reviews"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    review = place.reviews
    list_reviews = []
    for obj in review:
        list_reviews.append(obj.to_dict())
    return jsonify(list_reviews)


@app_views.route("/reviews/<review_id>", methods=['GET'], strict_slashes=False)
def list_review(review_id):
    """Return a JSON list of reviews"""
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """delete a JSON list of review"""
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route("places/<place_id>/reviews", methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """Create a JSON list of reviews"""
    json = request.get_json()
    if not json:
        abort(400, 'Not a JSON')
    if 'user_id' not in json:
        abort(400, 'Missing user_id')
    if 'text' not in json:
        abort(400, 'Missing text')
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    user = storage.get('User', json['user_id'])
    if user is None:
        abort(404)

    new_review = Review(text=json['text'],
                      user_id=json['user_id'],
                      place_id=place_id)
    storage.new(new_review)
    storage.save()

    return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Return a JSON review update"""
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    json = request.get_json()
    if not json:
        abort(400, 'Not a JSON')
    new_dict = review.to_dict()
    for k, v in json.items():
        if k in ['id', 'created_at', 'updated_at', 'user_id', 'place_id']:
            pass
        else:
            setattr(place, k, v)
    storage.save()

    return jsonify(review.to_dict()), 200
