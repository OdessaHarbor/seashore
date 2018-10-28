from flask import Flask
from flask_restful import Api
from Converter.apis import my_api
import os
import logging


def create_converter():
    """Create a Flask application using the app factory pattern.
    :return: Flask app
    """
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
    app = Flask("Converter", instance_relative_config=True)
    app.config.from_object("config.settings")
    app.config.from_pyfile("settings.py", silent=True)
    # enabling caching
    my_api.cache.init_app(app)

    api = Api(app)
    api.add_resource(my_api.Converter_api, '/currency_converter')

    return app


