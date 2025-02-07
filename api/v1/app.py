#!/usr/bin/python3
"""Start a flask web app"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS


app = Flask(__name__)


CORS(app, origins='0.0.0.0')
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def storage_close(exit):
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """Handler for 404 errors that returns a JSON-formatted 404
    status code response"""
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
        host = '0.0.0.0'
        if getenv('HBNB_API_HOST'):
            host = getenv('HBNB_API_HOST')
        port = 5000
        if getenv('HBNB_API_PORT'):
            port = getenv('HBNB_API_PORT')
        app.run(host=host, port=port, threaded=True, debug=True)
