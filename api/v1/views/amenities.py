#!/usr/bin/python3
""" State endpoints """
from flask import jsonify, request, abort
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
def all_amenities():
        """Return all amenities"""
        my_list = []
        for i in storage.all("Amenity").values():
                my_list.append(i.to_dict())
        return jsonify(my_list)


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['GET'])
def get_amenity_by_amenity_id(amenity_id):
        """Return amenity by given id"""
        for i in storage.all("Amenity").values():
                if i.id == amenity_id:
                        my_amen = storage.all()["Amenity" + '.' + amenity_id]
                        return jsonify(my_amen.to_dict())
        abort(404)


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_amenity_by_id(amenity_id):
        """Delete amenity"""
        for i in storage.all("Amenity").values():
                if i.id == amenity_id:
                        my_amen = storage.all()["Amenity" + '.' + amenity_id]
                        storage.delete(my_amen)
                        storage.save()
                        return jsonify({})
        abort(404)


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def create_amenity():
        """Create aamenity"""
        newam = request.get_json(silent=True)
        if newam is None:
                abort(400, 'Not a JSON')
        elif 'name' not in newam.keys():
                abort(400, 'Missing name')
        else:
                my_amen = Amenity(**newam)
                storage.new(my_amen)
                storage.save()
                return jsonify(my_amen.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['PUT'])
def update_amenity(amenity_id):
        """Update amenity"""
        updateam = request.get_json(silent=True)
        if updateam is None:
                abort(400, 'Not a JSON')
        for i in storage.all("Amenity").values():
                if i.id == amenity_id:
                        my_amen = storage.all()["Amenity" + '.' + amenity_id]
                        for key, value in updateam.items():
                                if key == 'id' or key == 'created_at' \
                                   or key == 'updated_at':
                                        pass
                                else:
                                        setattr(my_amen, key, value)
                        storage.save()
                        return jsonify(my_amen.to_dict()), 200
        abort(404)