from flask import Flask
from flask_restful import Api
from .apis import my_api




def create_converter():
    app = Flask(__name__, instance_relative_config=True)
    # app.config.from_object("config.settings")
    app.config.from_pyfile("settings.py", silent=True)

    my_api.cache.init_app(app)
    api = Api(app)
    api.add_resource(my_api.Converter, '/currency_converter')

    return app


