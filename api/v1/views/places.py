#!/usr/bin/python3
""" Place endpoints """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.user import User


@app_views.route('/cities/<string:city_id>/places', methods=["GET", "POST"])
def places_by_city(city_id):
    """Retrieves all places of a City object or add a new Place by city_id"""

    if request.method == 'GET':
        detector = 0
        for obj in storage.all("City").values():
            if obj.id == city_id:
                detector = 1
                break
            else:
                pass

        if detector != 0:
            results = []
            for place in storage.all("Place").values():
                if place.city_id == city_id:
                    results.append(place.to_dict())
            return jsonify(results)
	else:
            abort(404)

    elif request.method == "POST":
        req_json = request.get_json()
        if not req_json:
            abort(400, 'Not a JSON')
        if not req_json.get("user_id"):
            abort(400, "Missing user_id")
        user = storage.get(User, req_json.get("user_id"))
        if not user:
            abort(404, "Not found")
        if 'name' not in req_json:
            abort(400, 'Missing name')
        req_json["city_id"] = city_id
        new_place = Place(**req_json)
        new_place.save()
        return jsonify(new_place.to_dict()), 201
    else:
        abort(404)	


@app_views.route('/places/<string:place_id>', methods=["GET", "DELETE", "PUT"])
def place_by_id(place_id):
    """Retrieves, deletes or updates a Place object by place_id"""
    # tambien se puede optimizar, manito

    if request.method == 'GET':
        for obj in storage.all("Place").values():
            if obj.id == place_id:
                return jsonify(obj.to_dict())

    elif request.method == 'DELETE':
        for obj in storage.all("Place").values():
            if obj.id == place_id:
                storage.delete(obj)
                storage.save()
                return jsonify({}), 200

    elif request.method == 'PUT':
        for obj in storage.all("Place").values():
            if obj.id == place_id:
                http_data = request.get_json()
                if not http_data:
                    abort(400, 'Not a JSON')

                statics_attrs = ["id", "user_id",
                                 "city_id", "created_at", "updated_at"]
                for key, value in http_data.items():
                    if key not in statics_attrs:
                        setattr(obj, key, value)
                storage.save()
                return jsonify(obj.to_dict()), 200

    abort(404)
