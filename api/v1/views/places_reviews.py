#!/usr/bin/python3
""" Places reviews endpoints """
from flask import jsonify, request, abort
from models import storage
from models.state import Place
from models.review import Review
from models.user import User
from api.v1.views import app_views


@app_views.route('/places/<string:place_id>/reviews', methods=["GET", "POST"])
def places_reviews(place_id):
    """Retrieves the list of all Review objects of a Place"""
    if request.method == 'GET':
        place = storage.get(Place, place_id)

        if not place:
            abort(404)

        all_reviews = []
        for place in place.reviews:
            all_reviews.append(place.to_dict())
        return jsonify(all_reviews)

    elif request.method == 'POST':
        http_data = request.get_json()
        if not http_data:
            abort(400, 'Not a JSON')
        if "user_id" not in http_data:
            abort(400, "Missing user_id")
        if "text" not in http_data:
            abort(400, "Missing text")

        place = storage.get(Place, place_id)
        if not place:
            abort(404)

        user = storage.get(User, http_data["user_id"])
        if not user:
            abort(404)

        http_data["place_id"] = place_id
        new_review = Review(**http_data)
        new_review.save()
        return jsonify(new_review.to_dict()), 201


@app_views.route('reviews/<string:review_id>', methods=["GET", "DELETE", "PUT"])
def review_by_id(review_id):
    """Retrieves, deletes or updates a Review object by review_id"""
    if request.method == 'GET':
        review = storage.get(Review, review_id)
        if not review:
            abort(404)

        return jsonify(review.to_dict())

    elif request.method == 'DELETE':
        review = storage.get(Review, review_id)
        if not review:
            abort(404)
        else:
            storage.delete(review)
            storage.save()
            return jsonify({}), 200

    elif request.method == 'PUT':
        review = storage.get(Review, review_id)
        if not review:
            abort(404)

        http_data = request.get_json()
        if not http_data:
            abort(400, 'Not a JSON')

        static_attrs = ['id', 'user_id',
                        'place_id', 'created_at', 'updated_at']
        for key, value in http_data.items():
            if key not in static_attrs:
                setattr(review, key, value)
            storage.save()
            return jsonify(review.to_dict()), 200

    abort(404)

