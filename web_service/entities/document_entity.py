"""
Name: arXiv Intelligence NER Web Service
Authors: Jonathan CASSAING
Web service specialized in Named Entity Recognition (NER), in Natural Language Processing (NLP)
"""

import json
from sqlalchemy import Column, Integer, String
from web_service.common import Base, session_factory

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
    # Date and time column in the database
    date = Column("date", String(255))
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

    def __init__(self: object):
        """Initialize the object"""

    def insert(
            self,
            date: str = None,
            author: str = None,
            creator: str = None,
            producer: str = None,
            subject: str = None,
            title: str = None,
            number_of_pages: int = None,
            raw_info: str = None,
            content: str = None,):
        """Insert a new object to the database"""

        session = session_factory()
        self.status = "PENDING"
        self.date = str(date)
        self.author = str(author)
        self.creator = str(creator)
        self.producer = str(producer)
        self.subject = str(subject)
        self.title = str(title)
        self.number_of_pages = number_of_pages
        self.raw_info = str(raw_info)
        self.content = str(content)
        session.add(self)
        session.commit()
        # We save the ID cause it will wiped after the session.close()
        self.internal_id = self.id
        session.close()

        return self.internal_id

    def update(
            self,
            object_id: int,
            date: str = None,
            author: str = None,
            creator: str = None,
            producer: str = None,
            subject: str = None,
            title: str = None,
            number_of_pages: int = None,
            raw_info: str = None,
            content: str = None):
        """Update an object in the database"""

        session = session_factory()
        pdf_entity = session.query(DocumentEntity).get(object_id)
        pdf_entity.status = "SUCCESS"
        pdf_entity.date = str(date)
        pdf_entity.author = str(author)
        pdf_entity.creator = str(creator)
        pdf_entity.producer = str(producer)
        pdf_entity.subject = str(subject)
        pdf_entity.title = str(title)
        pdf_entity.number_of_pages = number_of_pages
        pdf_entity.raw_info = str(raw_info)
        pdf_entity.content = str(content)
        session.commit()
        # We save the ID cause it will wiped after the session.close()
        self.internal_id = self.id
        session.close()

        return self.internal_id

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
                "date": o.date,
                "author": o.author,
                "creator": o.creator,
                "producer": o.producer,
                "subject": o.subject,
                "title": o.title,
                "number_of_pages": o.number_of_pages,
                "raw_info": o.raw_info,
                "content": o.content,
            }
        # Base class will raise the TypeError.
        return super().default(o)
