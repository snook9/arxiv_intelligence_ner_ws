"""
Name: arXiv Intelligence NER Web Service
Authors: Jonathan CASSAING
Web service specialized in Named Entity Recognition (NER), in Natural Language Processing (NLP)
"""

from flask import Blueprint, request
from flask_restx import Resource, Api
from web_service.services import ApiService

bp = Blueprint("router", __name__, template_folder="templates")

# TODO TEMP code
bp2 = Blueprint("router2", __name__, template_folder="templates")
api = Api(bp2,
    title='My Title',
    version='1.0',
    description='A description',
    # All API metadatas
)

# TODO TEMP code
@api.route('/index', endpoint='index')
class Router2(Resource):
    def get(self):
        return ApiService.index(request)
    
    @api.doc(responses={403: 'Not Authorized'})
    def post(self, id):
        api.abort(403)

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
