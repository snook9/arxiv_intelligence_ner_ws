"""
Name: arXiv Intelligence NER Web Service
Authors: Jonathan CASSAING
Web service specialized in Named Entity Recognition (NER), in Natural Language Processing (NLP)
"""

import json
from pathlib import Path
from flask import Response, render_template
from werkzeug.utils import secure_filename
from sqlalchemy import select
from web_service.entities import DocumentEntity, PdfEntity, MessageEntity, MessageEncoder
from web_service.common import Config, session_factory
from web_service.entities.document_entity import DocumentEncoder

class Api:
    """Api controller of the arXiv Intelligence NER Web Service"""

    def __init__(self: object):
        pass

    @staticmethod
    def allowed_file(filename: str):
        """Check is the file extension is allowed according to the config.cfg file.
        Args:
            filename (str): file to check.
        Returns:
            bool: True if the extension of the filename is allowed, otherwise - returns False.
        """
        return (
            "." in filename
            and filename.rsplit(".", 1)[1].lower() in Config().get_allowed_extensions()
        )

    @staticmethod
    def index(request):
        """Index of the API.
        GET method returns a wellcome message.
        POST method can be used to upload a PDF file.
            See README.md for response format.

        Returns:
            flask.Response: standard flask HTTP response.
        """
        # If it's a POST request (the client try to send a file)
        if request.method == "POST":
            # check if the post request has the file part
            if "file" not in request.files:
                return Response(
                    json.dumps(MessageEntity("No file part"), cls=MessageEncoder),
                    mimetype="application/json;charset=utf-8",
                ), 400

            # Else, we get the file
            file = request.files["file"]

            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == "":
                return Response(
                    json.dumps(MessageEntity("No selected file"), cls=MessageEncoder),
                    mimetype="application/json;charset=utf-8",
                ), 400

            # If the file's type is allowed
            if file and Api.allowed_file(file.filename):
                # Check user input
                filename = secure_filename(file.filename)
                filepath = Path().joinpath(Config().get_upload_temp_folder(), filename)
                # Save the file in an upload folder
                file.save(filepath)
                # Extract and persist the file in the database
                doc_id = PdfEntity().start_ner(filepath)
                # If failed
                if None is doc_id:
                    # Returns the appropriate error
                    return Response(
                        json.dumps(
                            MessageEntity("This file's type is not allowed!"),
                            cls=MessageEncoder,
                        ),
                        mimetype="application/json;charset=utf-8",
                    ), 400
                # Else, returning the ID of the object in the database
                return Response(
                    json.dumps(
                        MessageEntity(
                            "The file '" + filename + "' has been sent successfully!",
                            doc_id,
                        ),
                        cls=MessageEncoder,
                    ),
                    mimetype="application/json;charset=utf-8",
                ), 201

            # Else, the file's type is not allowed
            return Response(
                json.dumps(
                    MessageEntity("This file's type is not allowed!"), cls=MessageEncoder
                ),
                mimetype="application/json;charset=utf-8",
            ), 400

        # Generate an index HTML page with an outstanding look & feel
        return render_template("index.html", title="NER Web Service")

    @staticmethod
    def get_document(request, doc_id: int):
        """Information about a document.
        GET method returns metadata, named entities and RDF triples about the document,
        specified by the ID parameter.
            See README.md for response format.
        Returns:
            flask.Response: standard flask HTTP response.
        """
        if request.method == "GET":
            # Preparing the query for the ID
            stmt = select(DocumentEntity).where(DocumentEntity.id == doc_id)
            # Retreive the session
            session = session_factory()
            # Executing the query
            result = session.execute(stmt)
            # Parsing the result
            for user_obj in result.scalars():
                # Converting the object to JSON string
                json_data = json.dumps(user_obj, cls=DocumentEncoder)
                # We leave the for and return the first element
                # (cause "normaly", there is only one row)
                return Response(json_data, mimetype="application/json;charset=utf-8")
            # Else, no document found
            return Response(
                json.dumps(MessageEntity("No document found"), cls=MessageEncoder),
                mimetype="application/json;charset=utf-8",
            ), 404
        return Response(
            json.dumps(MessageEntity("Incorrect HTTP method"), cls=MessageEncoder),
            mimetype="application/json;charset=utf-8",
        ), 405
