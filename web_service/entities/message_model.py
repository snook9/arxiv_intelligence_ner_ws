"""
Name: arXiv Intelligence NER Web Service
Authors: Jonathan CASSAING
Web service specialized in Named Entity Recognition (NER), in Natural Language Processing (NLP)
"""

import json

class MessageModel:
    """Class for returning a generic message"""

    # ID of the inserted object
    object_id = None
    # Generic user message
    message = ""

    def __init__(self: object, message: str = None, object_id: int = None):
        self.object_id = object_id
        self.message = message


class MessageEncoder(json.JSONEncoder):
    """Class for converting full object to JSON string"""

    def default(self, o):
        if isinstance(o, MessageModel):
            return {"id": o.object_id, "message": o.message}

        # Base class will raise the TypeError.
        return super().default(o)
