#!/usr/bin/python3
"""
flask app module
"""


import os
from models import storage
from flask import Flask, Blueprint
from api.v1.views import app_views
from flask import make_response, jsonify
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_session(exception=None):
    """
    close session
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Method to handler an 404 error"""

    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == '__main__':
    _host = os.getenv('HBNB_API_HOST')
    _port = os.getenv('HBNB_API_PORT')

    app.run(host=_host, port=_port, threaded=True)
