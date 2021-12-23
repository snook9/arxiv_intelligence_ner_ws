"""
Name: arXiv Intelligence NER Web Service
Authors: Jonathan CASSAING
Web service specialized in Named Entity Recognition (NER), in Natural Language Processing (NLP)
"""

import json
from pathlib import Path
from flask import Response, current_app as app
from werkzeug.utils import secure_filename
from web_service.entities import PdfEntity, MessageEntity, MessageEncoder
from web_service.common import Config

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
            and filename.rsplit(".", 1)[1].lower() in Config().allowed_extensions
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
                filepath = Path().joinpath(Config().upload_temp_folder, filename)
                # Save the file in an upload folder
                file.save(filepath)
                # Extract and persist the file in the database
                doc_id = PdfEntity().extract_and_persist(filepath)
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
        return Response("Hello World!")
