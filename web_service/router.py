"""
Name: arXiv Intelligence NER Web Service
Authors: Jonathan CASSAING
Web service specialized in Named Entity Recognition (NER), in Natural Language Processing (NLP)
"""

from flask import Blueprint, request
from flasgger import swag_from
from web_service.services import Api

bp = Blueprint("router", __name__, template_folder="templates")

@swag_from("swagger/hello_world.yml", methods=["GET"])
@bp.route("/", methods=["GET", "POST"])
def index():
    """Index of the API.

    Returns:
        flask.Response: standard flask HTTP response.
    """
    return Api.index(request)

@bp.route("/document/<int:doc_id>", methods=["GET"])
def get_document(doc_id):
    """Information about a document.
    GET method returns metadata, named entities and RDF triples about the document,
    specified by the ID parameter.
        See README.md for response format.
    Returns:
        flask.Response: standard flask HTTP response.
    """
    return Api.get_document(request, doc_id)
