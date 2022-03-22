"""
Name: arXiv Intelligence NER Web Service
Authors: Jonathan CASSAING
Web service specialized in Named Entity Recognition (NER), in Natural Language Processing (NLP)
"""

import json
import time

# PDF list used as references to compare
# the extracted named entities
# The named entities as references are saved
# in the folder tests/reference_json
# These json files match with this PDF list
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
    # Upload the document
    response = client.get("/?doc_url=" + doc_url)
    if response is None:
        print("GET /: Error while sending the file: %s", doc_url)
        return None

    # Convert response to JSON
    message = json.loads(response.get_data(as_text=True))

    if message["id"] != -1:
        status = "PENDING"
        # While the status is not SUCCESS or ERROR
        while status == "PENDING":
            # Wait some seconds before request
            time.sleep(2)
            # Request metadata
            response = client.get("/document/metadata/" + str(message["id"]))
            if response is None:
                print("GET /document/metadata/: \
                    Error while retrieving metadata of the file: %s", message["id"])
                status = "ERROR"
                break

            # Convert response to JSON
            data = json.loads(response.get_data(as_text=True))
            # Save the new status
            status = data["status"]

        # If while is finished, return data
        return data

    return None

def test_performance_measurement(client):
    """This function compare the named entities from
    the json files in the folder tests/reference_json
    with the real responses of the Web Service"""
    for pdf in pdf_list:
        # For each PDF, we get metadata
        data = get_medatadata(client, pdf)
        if data is None:
            continue

        # Build the dataset to compare
        # We convert the JSON format
        # with the same format that
        # the JSON files in tests/reference_json
        data_to_compare = dict()
        data_to_compare["pdf_url"] = pdf
        data_to_compare["named_entities"] = []
        for named_entity in data["named_entities"]:
            if named_entity["type"] == "PERSON":
                data_to_compare["named_entities"].append(named_entity["text"])
        # We remove duplicates from the list
        data_to_compare["named_entities"] = list(dict.fromkeys(data_to_compare["named_entities"]))

        # Build the dataset as reference
        # We read all JSON in tests/reference_json
        filename = "tests/reference_json/" + pdf.rsplit('/', 1)[1] + ".json"
        with open(filename, 'r', encoding="utf-8") as file:
            ref_data = file.read()

        ref_data = json.loads(ref_data)

        # We compare both datasets
        named_entities_match = 0
        named_entities_error = 0
        for named_entity in data_to_compare["named_entities"]:
            if named_entity in ref_data["named_entities"]:
                # For each named entity found
                named_entities_match += 1
            else:
                # If the named entity is a false positive
                named_entities_error += 1

        # Computing the score
        accuracy = (named_entities_match * 100) / len(ref_data["named_entities"])
        result = dict()
        result["pdf_url"] = pdf
        result["named_entities_found"] = named_entities_match
        result["actual_named_entities"] = len(ref_data["named_entities"])
        result["accuracy"] = str(round(accuracy, 3)) + " %"
        result["accuracy_description"] = "Percentage based on number of named entities found "\
           "vs. reference"
        result["error"] = named_entities_error
        result["error_description"] = "Number of named entities as false positives"
        # Saving result in tests/reference_json
        filename = "tests/reference_json/result_" + pdf.rsplit('/', 1)[1] + ".json"
        with open(filename, 'w', encoding="utf-8") as file:
            json.dump(result, file)

def create_json_comparator(client):
    """This function create json files in the folder
    tests/reference_json. These files are used, as references,
    for named entities performance measurement"""
    for pdf in pdf_list:
        # For each PDF, we get metadata
        data = get_medatadata(client, pdf)
        if data is None:
            continue

        # We keep the PDF url
        # and the PERSON named entities
        json_dict = dict()
        json_dict["pdf_url"] = pdf
        json_dict["named_entities"] = []
        for named_entity in data["named_entities"]:
            if named_entity["type"] == "PERSON":
                json_dict["named_entities"].append(named_entity["text"])

        # We remove duplicates from the list
        json_dict["named_entities"] = list(dict.fromkeys(json_dict["named_entities"]))

        # The json files are saved in tests/reference_json
        filename = "tests/reference_json/" + pdf.rsplit('/', 1)[1] + ".json"
        with open(filename, 'w', encoding="utf-8") as file:
            json.dump(json_dict, file)
