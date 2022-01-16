"""
Name: arXiv Intelligence NER Web Service
Authors: Jonathan CASSAING
Web service specialized in Named Entity Recognition (NER), in Natural Language Processing (NLP)
"""

import json
from datetime import datetime
# pdftotext is used to extract PDF content (text body)
import pdftotext
from pathlib import Path
# PyPDF2 is used to extract PDF meta data
from PyPDF2 import PdfFileReader
from web_service.entities.document_entity import DocumentEntity
from web_service.entities.named_entity import NamedEntityEncoder

class PdfEntity(DocumentEntity):
    """Class for representing Pdf entity and his Data Access Object
    """

    def _async_ner(self, filename: Path, object_id: int):
        """Private method to extract named entities then update a PDF object in the database
        You must use insert() without parameter before,
        to get the id of your futur line in the database.

        Args:
            filename (str): filename of the target file
            object_id (int): id of the database line to update

        Returns:
            int: ID of the persisted object in the database.
        """
        today = datetime.today().strftime("%Y-%m-%d-%H-%M-%S.%f")

        with open(filename, "rb") as file:
            # Extracting the text (content)
            data = pdftotext.PDF(file)
            content = "".join(data)

            # Extracting meta data
            pdf = PdfFileReader(file)
            info = pdf.getDocumentInfo()
            number_of_pages = pdf.getNumPages()
            author = info.author
            creator = info.creator
            producer = info.producer
            subject = info.subject
            title = info.title

            # We extract the named entities
            named_entities = self.extract_named_entities(content)
            # We convert named entities to json
            json_named_entities = json.dumps(named_entities, cls=NamedEntityEncoder)

            # Saving content AND meta data to the database
            self.update(
                object_id,
                today,
                author,
                creator,
                producer,
                subject,
                title,
                number_of_pages,
                info,
                content,
                json_named_entities
            )
            return self.internal_id
