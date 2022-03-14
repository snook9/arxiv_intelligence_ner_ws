"""
Name: arXiv Intelligence NER Web Service
Authors: Jonathan CASSAING
Web service specialized in Named Entity Recognition (NER), in Natural Language Processing (NLP)
"""

from web_service import create_app
from waitress import serve

app = create_app()

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=5000)
