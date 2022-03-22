"""
Name: arXiv Intelligence NER Web Service
Authors: Jonathan CASSAING
Web service specialized in Named Entity Recognition (NER), in Natural Language Processing (NLP)
"""

import json
import time

def create_json_comparator(client):
    """Function for measuring the performance"""
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

    for pdf in pdf_list:
        response = client.get("/?doc_url=" + pdf)
        if response is None:
            print("GET /: Error while sending the file: %s", pdf)
            continue
        else:
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

            json_dict = dict()
            json_dict["pdf_url"] = pdf
            json_dict["named_entities"] = []
            for named_entity in data["named_entities"]:
                if named_entity["type"] == "PERSON":
                    json_dict["named_entities"].append(named_entity["text"])

            filename = "tests/reference_json/" + pdf.rsplit('/', 1)[1] + ".json"
            with open(filename, 'w', encoding="utf-8") as file:
                json.dump(json_dict, file)
