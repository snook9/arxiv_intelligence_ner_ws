"""
Name: arXiv Intelligence NER Web Service
Authors: Jonathan CASSAING
Web service specialized in Named Entity Recognition (NER), in Natural Language Processing (NLP)
"""

import json
import io
import time

def test_post_document(client):
    """Test the index route"""
    response = client.get("/")
    assert response.status_code == 200

    data = dict()

    # Test uploading a file without file part
    data["file"] = b"my file content", "test_file.txt"
    response = client.post("/", data=data, content_type="multipart/form-data")
    assert response.status_code == 400

    # Test uploading a file with a forbidden extension
    data["file"] = io.BytesIO(b"my file content"), "test_file.doc"
    response = client.post("/", data=data, content_type="multipart/form-data")
    assert response.status_code == 400

    # Test uploading a real pdf file
    data["file"] = (open("tests/article.pdf", 'rb'), "tests/article.pdf")
    response = client.post("/", data=data, content_type="multipart/form-data")
    assert response.status_code == 201

def test_get_document(client):
    """Test the index route"""
    # Test indicating a wrong URL type
    response = client.get("/?doc_url=ceciestunefichierabsent")
    assert response.status_code == 400

    # Test indicating a wrong URL
    response = client.get("/?doc_url=https://ceciestunemauvaiseurl")
    assert response.status_code == 400

    # Test indicating a real file from URL
    response = client.get("/?doc_url=https://arxiv.org/ftp/arxiv/papers/2201/2201.05599.pdf")
    assert response.status_code == 201

    # We get the json response
    data = json.loads(response.get_data(as_text=True))

    # We wait 8 sec to let the process finish
    time.sleep(8)

    # We check the metadata of the uploaded document
    response = client.get("/document/metadata/" + str(data["id"]))
    data = json.loads(response.get_data(as_text=True))
    # If the process is SUCCESS
    assert data["status"] == "SUCCESS"

def test_get_document_metadata(client):
    """Test the /document/metadata/<id> route"""
    # We insert a first document in the database (in case the db is empty)
    data = dict()
    data["file"] = (open("tests/article.pdf", 'rb'), "tests/article.pdf")
    response = client.post("/", data=data, content_type="multipart/form-data")
    # We wait 3 sec to let the process finish
    time.sleep(3)

    # Now, the first document exists
    # So, we get it
    response = client.get("/document/metadata/1")
    data = json.loads(response.get_data(as_text=True))

    # The status must be 200 OK
    assert response.status_code == 200
    # We test if we received the ID of the JSON object
    assert data["id"] == 1

    response = client.get("/document/metadata/1000000000")
    assert response.status_code == 404

    response = client.post("/document/metadata/1")
    assert response.status_code == 405

def test_get_document_content(client):
    """Test the /document/content/<id> route"""
    # We insert a first document in the database (in case the db is empty)
    data = dict()
    data["file"] = (open("tests/article.pdf", 'rb'), "tests/article.pdf")
    response = client.post("/", data=data, content_type="multipart/form-data")
    # We wait 3 sec to let the process finish
    time.sleep(3)

    # Now, the first document exists
    # So, we get it
    response = client.get("/document/content/1")
    data = json.loads(response.get_data(as_text=True))

    # The status must be 200 OK
    assert response.status_code == 200
    # We test if we received the ID of the JSON object
    assert data["id"] == 1

    response = client.get("/document/content/1000000000")
    assert response.status_code == 404

    response = client.post("/document/content/1")
    assert response.status_code == 405
