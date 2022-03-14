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

    Swagger(app, template=swagger_template, config=swagger_config)

    return app

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Swagger UI document of the arXiv Intelligence NER Web Service",
        "version": "1.0",
        "description": "This document describes the web service interface specification."
    },
    "host": LazyString(lambda: request.host),  # overrides localhost:500
    "schemes": [
        "http",
        "https"
    ],
    "securityDefinitions": {
        "wsstore_auth": {
            "type": "basic"
        }
    },
    "security": [
        {
            "wsstore_auth": ["read", "write"]
        }
    ],
    "definitions": {
        "Message": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer",
                    "format": "int32",
                    "description": "ID of the uploaded PDF file, otherwise 'null' if error"
                },
                "message": {
                    "type": "string",
                    "description": "Explicit human readable status message"
                }
            }
        },
        "Content": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer",
                    "format": "int32",
                    "description": "ID of the uploaded PDF file, otherwise 'null' if error"
                },
                "content": {
                    "type": "string",
                    "description": "Content of the PDF document"
                }
            }
        },
        "Metadata": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer",
                    "format": "int32",
                    "description": "ID of the uploaded PDF file, otherwise 'null' if not found, \
                    Important: when the id is null, the response is a Message json object"
                },
                "status": {
                    "type": "string",
                    "description": "Status of the document processing",
                    "enum": [
                        "SUCCESS",
                        "PENDING",
                        "ERROR"
                    ]
                },
                "uploaded_date": {
                    "type": "string",
                    "format": "2022-03-14-09-48-51.679768",
                    "description": "Date and time when the file was uploaded"
                },
                "author": {
                    "type": "string",
                    "description": "Author specified in the PDF file as meta data"
                },
                "creator": {
                    "type": "string",
                    "description": "Creator specified in the PDF file as meta data"
                },
                "producer": {
                    "type": "string",
                    "description": "Producer specified in the PDF file as meta data"
                },
                "subject": {
                    "type": "string",
                    "description": "Subject specified in the PDF file as meta data "
                },
                "title": {
                    "type": "string",
                    "description": "Title specified in the PDF file as meta data"
                },
                "number_of_pages": {
                    "type": "integer",
                    "format": "int32",
                    "description": "Nomber of pages in the PDF file"
                },
                "raw_info": {
                    "type": "string",
                    "description": "Additional information in the PDF file as meta data"
                },
                "named_entities": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "text": {
                                "type": "string",
                                "description": "text of the named entity"
                            },
                            "begin_offset": {
                                "type": "integer",
                                "format": "int32",
                                "description": "start index of the entity \
                                in the full document content"
                            },
                            "end_offset": {
                                "type": "integer",
                                "format": "int32",
                                "description": "end index of the entity \
                                 in the full document content"
                            },
                            "relationship": {
                                "type": "string",
                                "description": "Relation between the document and the named entity",
                                "enum": [
                                    "QUOTED",
                                    "REFERENCED"
                                ]
                            },
                            "score": {
                                "type": "string",
                                "description": "Entity reliability score",
                                "enum": [
                                    "LOW",
                                    "MEDIUM",
                                    "HIGH"
                                ]
                            },
                            "type": {
                                "type": "string",
                                "description": "Type of the named entity",
                                "enum": [
                                    "PRODUCT",
                                    "DATE",
                                    "EVENT",
                                    "LOCATION",
                                    "ORGANIZATION",
                                    "PERSON",
                                    "QUANTITY",
                                    "TITLE",
                                    "OTHER"
                                ]
                            }
                        }
                    }
                }
            }
        }
    }
}

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
