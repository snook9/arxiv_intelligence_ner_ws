"""
Name: arXiv Intelligence NER Web Service
Authors: Jonathan CASSAING
Web service specialized in Named Entity Recognition (NER), in Natural Language Processing (NLP)
"""

from flask import Blueprint, request
from web_service.services import Api

bp = Blueprint("router", __name__, template_folder="templates")

@bp.route("/", methods=["GET", "POST"])
def index():
    """Index of the API.

    Returns:
        flask.Response: standard flask HTTP response.
    """
    return Api.index(request)
