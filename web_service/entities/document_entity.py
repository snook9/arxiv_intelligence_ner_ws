"""
Name: arXiv Intelligence NER Web Service
Authors: Jonathan CASSAING
Web service specialized in Named Entity Recognition (NER), in Natural Language Processing (NLP)
"""

import json
from sqlalchemy import Column, Integer, String
from web_service.common import Base, session_factory
from web_service.entities.named_entity import NamedEntity, NamedEntityScoreEnum, NamedEntityTypeEnum

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

    def __init__(self: object):
        """Initialize the object"""

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
        self.uploaded_date = str(uploaded_date)
        self.author = str(author)
        self.creator = str(creator)
        self.producer = str(producer)
        self.subject = str(subject)
        self.title = str(title)
        self.number_of_pages = number_of_pages
        self.raw_info = str(raw_info)
        self.content = str(content)
        self.named_entities = str(named_entities)
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
        pdf_entity.uploaded_date = str(uploaded_date)
        pdf_entity.author = str(author)
        pdf_entity.creator = str(creator)
        pdf_entity.producer = str(producer)
        pdf_entity.subject = str(subject)
        pdf_entity.title = str(title)
        pdf_entity.number_of_pages = number_of_pages
        pdf_entity.raw_info = str(raw_info)
        pdf_entity.content = str(content)
        pdf_entity.named_entities = str(named_entities)
        session.commit()
        # We save the ID cause it will wiped after the session.close()
        self.internal_id = self.id
        session.close()

        return self.internal_id
    
    def extract_named_entities(self, text: str):
        named_entities = list()

        named_entity_1 = NamedEntity()
        named_entity_1.text = "Jean Luc"
        named_entity_1.score = NamedEntityScoreEnum.MEDIUM
        named_entity_1.aws_score = -1
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

class DocumentEncoder(json.JSONEncoder):
    """Class for converting full object to JSON string"""

    def default(self, o):
        if isinstance(o, DocumentEntity):
            doc_id = o.id
            if None is doc_id:
                # If None, the object was created after a INSERT query,
                # so, the internal_id is the table id
                doc_id = o.internal_id

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
                "named_entities": o.named_entities
            }
        # Base class will raise the TypeError.
        return super().default(o)
