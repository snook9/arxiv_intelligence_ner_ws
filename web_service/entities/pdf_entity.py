"""
Name: arXiv Intelligence NER Web Service
Authors: Jonathan CASSAING
Web service specialized in Named Entity Recognition (NER), in Natural Language Processing (NLP)
"""

from pathlib import Path
# pdftotext is used to extract PDF content (text body)
import pdftotext
# PyPDF2 is used to extract PDF meta data
from PyPDF2 import PdfFileReader
from web_service.common import Config
from web_service.entities.document_entity import DocumentEntity

class PdfEntity(DocumentEntity):
    """Class for representing Pdf entity and his Data Access Object
    """
    def __init__(self: object, config: Config):
        self.config = config
        super().__init__(config)

    def extract_document(self, filename: Path):
        """Overwriting DocumnetEntity.extract_document() by a specific pdf code"""
        with open(filename, "rb") as file:
            document = DocumentEntity(self.config)
            # Extracting the text (content)
            data = pdftotext.PDF(file)
            document.content = "".join(data)

            # Extracting meta data
            pdf = PdfFileReader(file)
            document.raw_info = pdf.getDocumentInfo()
            document.number_of_pages = pdf.getNumPages()
            document.author = document.raw_info.author
            document.creator = document.raw_info.creator
            document.producer = document.raw_info.producer
            document.subject = document.raw_info.subject
            document.title = document.raw_info.title
            return document
