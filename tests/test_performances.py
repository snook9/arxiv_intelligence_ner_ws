"""
Name: arXiv Intelligence NER Web Service
Authors: Jonathan CASSAING
Web service specialized in Named Entity Recognition (NER), in Natural Language Processing (NLP)
"""

import json
import time

pdf_list = ["https://arxiv.org/pdf/2203.10451.pdf",
            "https://arxiv.org/pdf/2203.10525.pdf",
            "https://arxiv.org/pdf/2203.08617.pdf",
            "https://arxiv.org/pdf/2203.07998.pdf",
            "https://arxiv.org/pdf/2203.07993.pdf",
            "https://arxiv.org/pdf/2203.07782.pdf",
            "https://arxiv.org/pdf/2203.07676.pdf",
            "https://arxiv.org/pdf/2203.07507.pdf",
            "https://arxiv.org/pdf/2203.08111.pdf",
            "https://arxiv.org/pdf/2203.08015.pdf"]

def get_medatadata(client, doc_url):
    """Returns metadata of a document"""
    response = client.get("/?doc_url=" + doc_url)
    if response is None:
        print("GET /: Error while sending the file: %s", doc_url)
        return None

    message = json.loads(response.get_data(as_text=True))

    if message["id"] != -1:
        status = "PENDING"
        while status == "PENDING":
            time.sleep(2)
            response = client.get("/document/metadata/" + str(message["id"]))
            if response is None:
                print("GET /document/metadata/: \
                    Error while retrieving metadata of the file: %s", message["id"])
                status = "ERROR"
                break

            data = json.loads(response.get_data(as_text=True))
            status = data["status"]
        return data

def create_json_comparator(client):
    """This function create json files in the folder
    tests/reference_json. These files are used for
    named entities performance measurement"""
    for pdf in pdf_list:
        data = get_medatadata(client, pdf)
        if data is None:
            continue

        json_dict = dict()
        json_dict["pdf_url"] = pdf
        json_dict["named_entities"] = []
        for named_entity in data["named_entities"]:
            if named_entity["type"] == "PERSON":
                json_dict["named_entities"].append(named_entity["text"])

        filename = "tests/reference_json/" + pdf.rsplit('/', 1)[1] + ".json"
        with open(filename, 'w', encoding="utf-8") as file:
            json.dump(json_dict, file)

def test_performance_measurement(client):
    """This function compare the named entities from
    the json files in the folder tests/reference_json
    with the responses of the Web Service"""
    for pdf in pdf_list:
        data = get_medatadata(client, pdf)
        if data is None:
            continue

        data_to_compare = dict()
        data_to_compare["pdf_url"] = pdf
        data_to_compare["named_entities"] = []
        for named_entity in data["named_entities"]:
            if named_entity["type"] == "PERSON":
                data_to_compare["named_entities"].append(named_entity["text"])

        filename = "tests/reference_json/" + pdf.rsplit('/', 1)[1] + ".json"
        with open(filename, 'r', encoding="utf-8") as file:
            ref_data = file.read()

        ref_data = json.loads(ref_data)

        for named_entity in data_to_compare["named_entities"]:
            if named_entity in ref_data["named_entities"]:
                print("FOUND")
            else:
                print("NOT FOUND")
