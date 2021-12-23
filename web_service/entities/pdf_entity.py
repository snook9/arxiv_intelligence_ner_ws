"""
Name: arXiv Intelligence NER Web Service
Authors: Jonathan CASSAING
Web service specialized in Named Entity Recognition (NER), in Natural Language Processing (NLP)
"""

from datetime import datetime
from pathlib import Path
from multiprocessing import Process
# pdftotext is used to extract PDF content (text body)
import pdftotext
# PyPDF2 is used to extract PDF meta data
from PyPDF2 import PdfFileReader
from web_service.entities.document_entity import DocumentEntity

class PdfEntity(DocumentEntity):
    """Class for representing Pdf entity and his Data Access Object
    """

    def __init__(self: object):
        """Initialize the object"""
        pass

    def _async_insert(self, filename: Path, object_id: int):
        """Private method to extract then update a PDF object in the database
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

            # Extracting meta data
            pdf = PdfFileReader(file)
            info = pdf.getDocumentInfo()
            number_of_pages = pdf.getNumPages()
            author = info.author
            creator = info.creator
            producer = info.producer
            subject = info.subject
            title = info.title

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
                "".join(data)
            )
            return self.internal_id

    def start_ner(self, filename: Path):
        """Start the recognition of named entities
        Public method to extract then persist a PDF object in the database
        First, this method ask an ID for the futur line in the database, then,
        this method create a process for extracting data and
        persisting the object in the database.
        This method returns the ID of the object in the database
        which will be inserted when the process will finish.

        Args:
            filename (str): filename of the target file

        Returns:
            int: ID of the persisted object in the database,
            otherwise - returns None if the file's type is not supported.
        """
        if str(filename).rsplit(".", 1)[1].lower() == "pdf":
            # We persist an empty object just to get the ID of the line in the database
            object_id = self.insert()

            process = Process(target=self._async_insert, args=(filename, object_id))
            process.start()

            return object_id

        return None
