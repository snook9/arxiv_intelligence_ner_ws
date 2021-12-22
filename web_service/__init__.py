"""
Name: arXiv Intelligence NER Web Service
Authors: Jonathan CASSAING
Web service specialized in Named Entity Recognition (NER), in Natural Language Processing (NLP)
"""

from pathlib import Path
from flask import Flask
from web_service import router

def create_app(test_config=None):
    """Create and configure the flask app with the factory pattern"""
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_pyfile("config.py", silent=False)
        app.config.update(test_config)

    # Register the router
    app.register_blueprint(router.bp)

    # Check if the folder where uploaded files will be saved exists
    folder = Path(app.config["UPLOAD_FOLDER"])
    if False is folder.exists():
        # If the folder doesn't exist, we create it
        folder.mkdir()

    return app
