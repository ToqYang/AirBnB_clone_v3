#!/usr/bin/python3
# App for the api
from flask import Flask

app = Flask(__name__)

from models import storage
from api.v1.views import app_views
import os

app.register_blueprint(app_views)


@app.teardown_appcontext
def close_session(exeption=None):
    """Close session"""
    storage.close()


if __name__ == '__main__':
    host = os.getenv('HBNB_API_HOST')
    port = os.getenv('HBNB_API_PORT')
    if host is None:
        host = '0.0.0.0'
    if port is None:
        port = 5000
    app.run(host=host, port=port, threaded=True)
