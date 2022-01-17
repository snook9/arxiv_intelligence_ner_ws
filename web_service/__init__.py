"""
Name: arXiv Intelligence NER Web Service
Authors: Jonathan CASSAING
Web service specialized in Named Entity Recognition (NER), in Natural Language Processing (NLP)
"""

import configparser
import sys
from pathlib import Path
from flask import Flask, request
from flasgger import Swagger, LazyString, LazyJSONEncoder
from web_service import router
from web_service.common import Config

def create_app(test_config=None):
    """Create and configure the flask app with the factory pattern"""
    app = Flask(__name__, instance_relative_config=True)
    app.json_encoder = LazyJSONEncoder

    # We load the config.ini file, one time
    app.project_config = Config()

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # Register the router
    app.register_blueprint(router.bp)

    # We load the setup config file
    setup_config = configparser.ConfigParser()
    setup_config.read('setup.cfg')
    try:
        print(
            setup_config.get('metadata', 'name_long') +
            " v" + setup_config.get('metadata', 'version')
        )
    except KeyError as err:
        print(f"Error in file setup.cfg: {err=}, {type(err)=}", file=sys.stderr)

    # We create the instance folder for the database
    path_folder = Path("instance")
    if False is path_folder.exists():
        # If the folder doesn't exist, we create it
        path_folder.mkdir()

    # We create the temp folder for uploaded files
    folder = app.project_config.get_upload_temp_folder()
    if False is folder.exists():
        # If the folder doesn't exist, we create it
        folder.mkdir()

    swagger = Swagger(app, template=swagger_template, config=swagger_config)

    return app

swagger_template = dict(
    info = {
        "title": LazyString(lambda: "Swagger UI document of the arXiv Intelligence NER Web Service"),
        "version": LazyString(lambda: "0.1"),
        "description": LazyString(lambda: "This document describes the web service interface specification."),
    },
    host = LazyString(lambda: request.host)
)
swagger_config = {
    "headers": [],
    "specs": [
        {
        "endpoint": "/",
        "route": "/swagger.json",
        "rule_filter": lambda rule: True,
        "model_filter": lambda tag: True,
    }],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}
