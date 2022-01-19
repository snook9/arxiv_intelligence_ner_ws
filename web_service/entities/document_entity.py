"""
Name: arXiv Intelligence NER Web Service
Authors: Jonathan CASSAING
Web service specialized in Named Entity Recognition (NER), in Natural Language Processing (NLP)
"""

import json
import sys
from datetime import datetime
from multiprocessing import Process
from pathlib import Path
from sqlalchemy import Column, Integer, String
from web_service.common.base import Base, session_factory
from web_service.common.config import Config
from .named_entity import NamedEntity, NamedEntityEncoder
from .named_entity import NamedEntityScoreEnum, NamedEntityTypeEnum
from web_service.services.spacy_ner_service import SpacyNerService
from web_service.services.aws_comprehend_ner_service import AwsComprehendNerService

class DocumentEntity(Base):
    """Class for representing a generic document entity and his Data Access Object
    """

    # Table name in the database
    __tablename__ = "document"
    # Internal ID is used to store the real ID (in database) after the session close
    internal_id = None
    # ID primary key in the database
    # Nota: this id is wiped after a session.close()
    id = Column("id", Integer, primary_key=True)
    # Status column in the database
    status = Column("status", String(255))
    # Uploaded date and time column in the database
    uploaded_date = Column("uploaded_date", String(255))
    # Author PDF meta data
    author = Column("author", String(255))
    # Creator PDF meta data
    creator = Column("creator", String(255))
    # Producer PDF meta data
    producer = Column("producer", String(255))
    # Subjet PDF meta data
    subject = Column("subject", String(255))
    # Title PDF meta data
    title = Column("title", String(255))
    # Pages count PDF meta data
    number_of_pages = Column("number_of_pages", Integer)
    # Raw informations PDF meta data
    raw_info = Column("raw_info", String())
    # Content column in the database
    content = Column("content", String)
    # Named entities extracted in json format
    named_entities = Column("named_entities", String())

    def __init__(self: object, config: Config):
        """Initialize the object"""
        self.config = config

    def insert(
            self,
            uploaded_date: str = None,
            author: str = None,
            creator: str = None,
            producer: str = None,
            subject: str = None,
            title: str = None,
            number_of_pages: int = None,
            raw_info: str = None,
            content: str = None,
            named_entities: str = None):
        """Insert a new object to the database"""

        session = session_factory()
        self.status = "PENDING"
        if uploaded_date is not None: self.uploaded_date = str(uploaded_date)
        if author is not None: self.author = str(author)
        if creator is not None: self.creator = str(creator)
        if producer is not None: self.producer = str(producer)
        if subject is not None: self.subject = str(subject)
        if title is not None: self.title = str(title)
        if number_of_pages is not None: self.number_of_pages = number_of_pages
        if raw_info is not None: self.raw_info = str(raw_info)
        if content is not None: self.content = str(content)
        if named_entities is not None: self.named_entities = str(named_entities)
        session.add(self)
        session.commit()
        # We save the ID cause it will wiped after the session.close()
        self.internal_id = self.id
        session.close()

        return self.internal_id

    def update(
            self,
            object_id: int,
            uploaded_date: str = None,
            author: str = None,
            creator: str = None,
            producer: str = None,
            subject: str = None,
            title: str = None,
            number_of_pages: int = None,
            raw_info: str = None,
            content: str = None,
            named_entities: str = None):
        """Update an object in the database"""

        session = session_factory()
        pdf_entity = session.query(DocumentEntity).get(object_id)
        pdf_entity.status = "SUCCESS"
        if uploaded_date is not None: pdf_entity.uploaded_date = str(uploaded_date)
        if author is not None: pdf_entity.author = str(author)
        if creator is not None: pdf_entity.creator = str(creator)
        if producer is not None: pdf_entity.producer = str(producer)
        if subject is not None: pdf_entity.subject = str(subject)
        if title is not None: pdf_entity.title = str(title)
        if number_of_pages is not None: pdf_entity.number_of_pages = number_of_pages
        if raw_info is not None: pdf_entity.raw_info = str(raw_info)
        if content is not None: pdf_entity.content = str(content)
        if named_entities is not None: pdf_entity.named_entities = str(named_entities)
        session.commit()
        # We save the ID cause it will wiped after the session.close()
        self.internal_id = self.id
        session.close()

        return self.internal_id

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
        try:
            # Extracting data end metadata of the document
            document = self.extract_document(filename)
        except IOError:
            print(
                "Error: the file", filename.absolute, "does not appear to exist",
                file=sys.stderr
                )

        # We extract the named entities
        named_entities = self.extract_named_entities(document.content)
        # We convert named entities to json
        json_named_entities = json.dumps(named_entities, cls=NamedEntityEncoder)

        # Saving content to the database
        self.update(
            object_id,
            datetime.today().strftime("%Y-%m-%d-%H-%M-%S.%f"),
            document.author,
            document.creator,
            document.producer,
            document.subject,
            document.title,
            document.number_of_pages,
            document.raw_info,
            document.content,
            json_named_entities
        )
        return self.internal_id

    def extract_named_entities(self, text: str):
        """This method extracted the named entities from the text"""

        ner_services = []
        ner_methods = self.config.get_ner_methods()
        if "aws-comprehend" in ner_methods:
            ner_services.append(AwsComprehendNerService(self.config.get_aws_region()))
        if "nltk" in ner_methods:
            print("NLTK NER method enabled")
        if "spacy" in ner_methods:
            ner_services.append(SpacyNerService())

        named_entities = []

        for ner_service in ner_services:
            named_entities.extend(ner_service.extract(text))

        named_entity_1 = NamedEntity()
        named_entity_1.text = "Jean Luc"
        named_entity_1.score = NamedEntityScoreEnum.MEDIUM
        named_entity_1.type = NamedEntityTypeEnum.PERSON
        named_entity_1.begin_offset = 120
        named_entity_1.end_offset = named_entity_1.begin_offset + len(named_entity_1.text)

        named_entity_2 = NamedEntity()
        named_entity_2.text = "AIRBUS"
        named_entity_2.score = NamedEntityScoreEnum.HIGH
        named_entity_2.aws_score = 0.98
        named_entity_2.type = NamedEntityTypeEnum.ORGANIZATION
        named_entity_2.begin_offset = 526
        named_entity_2.end_offset = named_entity_1.begin_offset + len(named_entity_1.text)

        named_entities.append(named_entity_1)
        named_entities.append(named_entity_2)

        return named_entities

    @staticmethod
    def extract_document(filename: Path):
        """Method for extracting data and metadata from a document

        You must overwrite extract_document() by your own code
        if you would extract data and metadata from a specific document.
        See PdfEntity for example.
        Returns:
            document (DocumentEntity): You must fill the following attributes of the document;
            author, creator, producer, subject, title, number_of_pages, info, content."""
        with open(filename, "r", encoding='utf-8') as file:
            # Extracting the text (content)
            content = file.read()
            document = DocumentEntity()
            document.content = content
            return document

    def start_ner(self, filename: Path):
        """Start the recognition of named entities
        Public method to extract then persist a document in the database
        First, this method ask an ID for the futur line in the database, then,
        this method create a process for extracting data and
        persisting the object in the database.
        This method returns the ID of the object in the database
        which will be inserted when the process will finish.

        This method calls _async_ner() method and execute it in a separated process.
        You must overwrite extract_document() by your own code
        if you would extract data and metadata from a specific document.
        See PdfEntity for example.

        Args:
            filename (str): filename of the target file

        Returns:
            int: ID of the persisted object in the database,
            otherwise - returns None if the file's type is not supported.
        """
        # We persist an empty object just to get the ID of the line in the database
        object_id = self.insert()
        # We launch the process
        process = Process(target=self._async_ner, args=(filename, object_id))
        process.start()
        # Returning the id in the database
        return object_id

class DocumentEncoder(json.JSONEncoder):
    """Class for converting full object to JSON string"""

    def default(self, o):
        if isinstance(o, DocumentEntity):
            doc_id = o.id
            if None is doc_id:
                # If None, the object was created after a INSERT query,
                # so, the internal_id is the table id
                doc_id = o.internal_id

            json_named_entities = None
            if o.named_entities is not None:
                json_named_entities = json.loads(o.named_entities)

            return {
                "id": doc_id,
                "status": o.status,
                "uploaded_date": o.uploaded_date,
                "author": o.author,
                "creator": o.creator,
                "producer": o.producer,
                "subject": o.subject,
                "title": o.title,
                "number_of_pages": o.number_of_pages,
                "raw_info": o.raw_info,
                "content": o.content,
                "named_entities": json_named_entities
            }
        # Base class will raise the TypeError.
        return super().default(o)
