"""
Name: arXiv Intelligence NER Web Service
Authors: Jonathan CASSAING
Web service specialized in Named Entity Recognition (NER), in Natural Language Processing (NLP)
"""

from flask import Blueprint, request
from flasgger import swag_from
from web_service.services import Api

bp = Blueprint("router", __name__, template_folder="templates")

@swag_from("swagger/get_document_upload.yml", methods=["GET"])
@swag_from("swagger/post_document_upload.yml", methods=["POST"])
@bp.route("/", methods=["GET", "POST"])
@bp.route("/document/upload", methods=["GET", "POST"])
def post_document():
    """Index of the API.

    Returns:
        flask.Response: standard flask HTTP response.
    """
    doc_url = request.args.get('doc_url')
    return Api.post_document(request, doc_url)

@swag_from("swagger/document_metadata.yml", methods=["GET"])
@bp.route("/document/metadata/<int:doc_id>", methods=["GET"])
def get_document_metadata(doc_id):
    """Information about a document.
    GET method returns metadata, named entities and RDF triples about the document,
    specified by the ID parameter.
        See README.md for response format.
    Returns:
        flask.Response: standard flask HTTP response.
    """
    return Api.get_document_metadata(request, doc_id)

@swag_from("swagger/document_content.yml", methods=["GET"])
@bp.route("/document/content/<int:doc_id>", methods=["GET"])
def get_document_content(doc_id):
    """Content inside a document.
    GET method returns content about the document,
    specified by the ID parameter.
        See README.md for response format.
    Returns:
        flask.Response: standard flask HTTP response.
    """
    return Api.get_document_content(request, doc_id)
