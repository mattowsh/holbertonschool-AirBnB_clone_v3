#!/usr/bin/python3
""" Place endpoints """
from flask import jsonify, request, abort
from models import storage
from models.place import Place
from models.user import User
from api.v1.views import app_views


@app_views.route('/cities/<string:city_id>/places', methods=["GET", "POST"])
def places_from_city(city_id):
    # Creating a list of dictionaries of all the cities in the database.
    cities = [obj.to_dict() for obj in storage.all("City").values()]
    # Creating a list of all the ids of the cities in the database.
    citiesIds = [obj['id'] for obj in cities]
    if city_id in citiesIds:
        if request.method == "GET":
            places = storage.all("Place")
            placesInCity = [obj.to_dict() for obj in places.values()
                           if obj.city_id == city_id]
            return jsonify(placesInCity)
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
