#!/usr/bin/python3
""" users file """
from api.v1.views.__init__ import app_views
from flask import jsonify, abort, request
from models.__init__ import storage
from models.user import User


@app_views.route("/users", methods=["GET", "POST"])
def get_users():
    if request.method == "GET":
        return jsonify([
            obj.to_dict() for obj in storage.all("User").values()])
    elif request.method == "POST":
        httpDict = request.get_json()
        if not httpDict:
            abort(400, "Not a JSON")
        if "email" not in httpDict:
            abort(400, "Missing email")
        if "password" not in httpDict:
            abort(400, "Missing password")
        new_user = User(**httpDict)
        new_user.save()
        return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["GET", "DELETE"])
def get_user_by_id(user_id):
    obj = storage.get(User, user_id)
    if request.method == "GET":
        if obj is None:
            abort(404)
        return jsonify(obj.to_dict())
    elif request.method == "DELETE":
        if obj is None:
            abort(404)

        storage.delete(obj)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/users/<user_id>", methods=["PUT"])
def put_user(user_id):
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)

    updated_dict = request.get_json()
    if not updated_dict:
        abort(400, "Not a JSON")
    for key, value in updated_dict.items():
        if key not in ["id", "created_at", "updated_at", "email"]:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict()), 200
