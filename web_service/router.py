"""
Name: arXiv Intelligence NER Web Service
Authors: Jonathan CASSAING
Web service specialized in Named Entity Recognition (NER), in Natural Language Processing (NLP)
"""

from flask import Blueprint, request
from flask_restx import Resource
from web_service.services import ApiService

bp = Blueprint("router", __name__, template_folder="templates")

class Router(Resource):
    @bp.route("/document/upload", methods=["GET", "POST"])
    def index():
        """Index of the API.

        Returns:
            flask.Response: standard flask HTTP response.
        """
        return ApiService.index(request)

    @bp.route("/document/<int:doc_id>", methods=["GET"])
    def get_document(doc_id):
        """Information about a document.
        GET method returns metadata, named entities and RDF triples about the document,
        specified by the ID parameter.
            See README.md for response format.
        Returns:
            flask.Response: standard flask HTTP response.
        """
        return ApiService.get_document(request, doc_id)
