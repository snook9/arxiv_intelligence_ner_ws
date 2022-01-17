"""
Name: arXiv Intelligence NER Web Service
Authors: Jonathan CASSAING
Web service specialized in Named Entity Recognition (NER), in Natural Language Processing (NLP)
"""


import json
import io
import time
from web_service.entities.pdf_entity import PdfEntity
from web_service import create_app

def test_index(client):
    """Test the index route"""
    response = client.get("/document/upload")
    assert response.status_code == 200

    data = dict()

    # Test uploading a file without file part
    data["file"] = b"my file content", "test_file.txt"
    response = client.post("/document/upload", data=data, content_type="multipart/form-data")
    assert response.status_code == 400

    # Test uploading a file with a forbidden extension
    data["file"] = io.BytesIO(b"my file content"), "test_file.doc"
    response = client.post("/document/upload", data=data, content_type="multipart/form-data")
    assert response.status_code == 400

    # Test uploading a real pdf file
    data["file"] = (open("tests/article.pdf", 'rb'), "tests/article.pdf")
    response = client.post("/document/upload", data=data, content_type="multipart/form-data")
    assert response.status_code == 201

def test_get_document(client):
    """Test the /document/<id> route"""
    # To insert a first document in the database (in case the db is empty)
    with create_app({"TESTING": True}).app_context():
        PdfEntity().start_ner("tests/article.pdf")
        # We wait 3 sec to let the process finish
        time.sleep(3)

    # Now, the first document exists
    # So, we get it
    response = client.get("/document/1")
    data = json.loads(response.get_data(as_text=True))

    # The status must be 200 OK
    assert response.status_code == 200
    # We test if we received the ID of the JSON object
    assert data["id"] == 1

    response = client.get("/document/1000000000")
    assert response.status_code == 404

    response = client.post("/document/1")
    assert response.status_code == 405
