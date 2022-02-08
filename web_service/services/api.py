"""
Name: arXiv Intelligence NER Web Service
Authors: Jonathan CASSAING
Web service specialized in Named Entity Recognition (NER), in Natural Language Processing (NLP)
"""

import json
import urllib.request
from json import JSONDecodeError
from pathlib import Path
from flask import Response, render_template, current_app
from werkzeug.utils import secure_filename
from sqlalchemy import select
from web_service.entities import DocumentEntity, PdfEntity, MessageEntity, MessageEncoder
from web_service.common import session_factory

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
            and filename.rsplit(".", 1)[1].lower()
            in current_app.project_config.get_allowed_extensions()
        )

    @staticmethod
    def post_document(request, doc_url):
        """Index of the API.
        GET method returns a welcome message or retreive the doc_url parameter.
        POST method can be used to upload a PDF file.
            See README.md for response format.

        Returns:
            flask.Response: standard flask HTTP response.
        """
        # If it's a POST method OR
        # it's a GET method and no doc_url are given OR
        if request.method == "POST" or \
           (request.method == "GET" and doc_url is not None):

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

                # If the file's type is not allowed
                if Api.allowed_file(file.filename) is False:
                    return Response(
                        json.dumps(
                            MessageEntity("This file's type is not allowed!"), cls=MessageEncoder
                        ),
                        mimetype="application/json;charset=utf-8",
                    ), 400

                # All it's OK, so we save the file in an upload folder
                filepath = Path().joinpath(
                    current_app.project_config.get_upload_temp_folder(),
                    # Check user input
                    secure_filename(file.filename)
                    )
                file.save(filepath)

            # Else, it's a GET method and no doc_url are given
            elif request.method == "GET" and doc_url is not None:
                try:
                    # We open the URL
                    with urllib.request.urlopen(doc_url) as response:
                        # We split the URL to get the filename
                        filename = doc_url.rsplit('/', 1).pop()
                        # All seems OK, so we save the file in an upload folder
                        filepath = Path().joinpath(
                            current_app.project_config.get_upload_temp_folder(),
                            # Check user input
                            secure_filename(filename)
                        )
                        file = open(filepath, 'wb')
                        # Save the file in an upload folder
                        file.write(response.read())
                        file.close()
                # Except, error in the given URL
                except ValueError as err:
                    return Response(
                        json.dumps(MessageEntity("Incorrect URL: {0}".format(err)), cls=MessageEncoder),
                        mimetype="application/json;charset=utf-8",
                    ), 400
                except urllib.error.URLError as err:
                    return Response(
                        json.dumps(MessageEntity("Incorrect URL: {0}".format(err)), cls=MessageEncoder),
                        mimetype="application/json;charset=utf-8",
                    ), 400

            # Here, we have the uploaded file saved in a folder
            # The full file path is filepath
            # Extract and persist the file in the database
            doc_id = PdfEntity(current_app.project_config).start_ner(filepath)
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
                        "The file '" + filepath.name + "' has been received successfully!",
                        doc_id,
                    ),
                    cls=MessageEncoder,
                ),
                mimetype="application/json;charset=utf-8",
            ), 201
        
        # Else, it's a basic GET method
        # Generate an index HTML page with an outstanding look & feel
        return render_template("index.html", title="NER Web Service")

    @staticmethod
    def get_document_metadata(request, doc_id: int):
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
                data = {}
                data["id"] = user_obj.id
                data["status"] = user_obj.status
                data["uploaded_date"] = user_obj.uploaded_date
                data["author"] = user_obj.author
                data["creator"] = user_obj.creator
                data["producer"] = user_obj.producer
                data["subject"] = user_obj.subject
                data["title"] = user_obj.title
                data["number_of_pages"] = user_obj.number_of_pages
                data["raw_info"] = user_obj.raw_info
                if user_obj.named_entities is not None:
                    try:
                        data["named_entities"] = json.loads(user_obj.named_entities)
                    except JSONDecodeError:
                        data["named_entities"] = None
                # Converting the object to JSON string
                json_data = json.dumps(data)
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

    @staticmethod
    def get_document_content(request, doc_id: int):
        """Content inside a document.
        GET method returns content about the document,
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
                data = {}
                data["id"] = user_obj.id
                data["content"] = user_obj.content
                # Converting the object to JSON string
                json_data = json.dumps(data)
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
