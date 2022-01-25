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
from web_service.services.spacy_ner_service import SpacyNerService
from web_service.services.aws_comprehend_ner_service import AwsComprehendNerService
from .named_entity import NamedEntityScoreEnum, NamedEntityEncoder

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

    @staticmethod
    def _binary_search(named_entities, target_begin_offset):
        """This algorithm is a binary search
        It search in the named_entities list,
        the named entity which match with target_begin_offset.
        The named_entities list must be sorted by begin_offset field
        Args:
            named_entities (list<NamedEntity>): list where search the offset.
            target_begin_offset (int): offset to search in the list.
        Returns:
            index: the index of the offset searched,
            otherwise the nearest index if the offset was not found,
            None in case of error.
            named_entity: the named_entity matching with the specified offset,
            otherwise - returns None.
        """
        aaa = 0
        bbb = len(named_entities)
        if bbb == 0:
            # If the list is empty, we leave
            return None, None
        while bbb > aaa + 1:
            mmm = (aaa + bbb) // 2
            if named_entities[mmm].begin_offset > target_begin_offset:
                bbb = mmm
            else:
                aaa = mmm

        if named_entities[aaa].begin_offset == target_begin_offset:
            return aaa, named_entities[aaa]

        if named_entities[aaa].begin_offset > target_begin_offset:
            nearest_index = aaa
        else:
            nearest_index = bbb

        return nearest_index, None

    def _merge(self, named_entities_1, named_entities_2) -> list:
        """Merge distinct the two named_entities_1 and named_entities_2 lists
        These two lists must be sorted by begin_offset field
        Args:
            named_entities_1 (list<NamedEntity>): list to merge.
            named_entities_2 (list<NamedEntity>): list to merge.
        Returns:
            list<NamedEntity>: merged list.
        """
        # First, we search the smallest list
        if len(named_entities_1) < len(named_entities_2):
            smallest_list = named_entities_1
            biggest_list = named_entities_2
        else:
            smallest_list = named_entities_2
            biggest_list = named_entities_1

        # We merge each element of the smallest list in the biggest list
        for named_entity in smallest_list:
            # We search the named_entity in the biggest list
            index, named_entity_searched = self._binary_search(
                biggest_list,
                named_entity.begin_offset
                )
            if index is not None:
                # If we have found it and the text match the current named entity
                # No need to insert
                if named_entity_searched is not None \
                    and (named_entity_searched.text == named_entity.text):
                    # But we just keep the aws_score (if exist)
                    try:
                        if named_entity.aws_score is not None:
                            named_entity_searched.aws_score = named_entity.aws_score
                    except AttributeError:
                        pass
                    # Also, we increment the score
                    if named_entity_searched.score == NamedEntityScoreEnum.LOW:
                        named_entity_searched.score = NamedEntityScoreEnum.MEDIUM
                    elif named_entity_searched.score == NamedEntityScoreEnum.MEDIUM:
                        named_entity_searched.score = NamedEntityScoreEnum.HIGH
                # Else, we have no found the named entity
                else:
                    # So, we insert it as new element in the biggest list
                    biggest_list.insert(index, named_entity)

        return biggest_list

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
        if uploaded_date is not None:
            self.uploaded_date = str(uploaded_date)
        if author is not None:
            self.author = str(author)
        if creator is not None:
            self.creator = str(creator)
        if producer is not None:
            self.producer = str(producer)
        if subject is not None:
            self.subject = str(subject)
        if title is not None:
            self.title = str(title)
        if number_of_pages is not None:
            self.number_of_pages = number_of_pages
        if raw_info is not None:
            self.raw_info = str(raw_info)
        if content is not None:
            self.content = str(content)
        if named_entities is not None:
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
        if uploaded_date is not None:
            pdf_entity.uploaded_date = str(uploaded_date)
        if author is not None:
            pdf_entity.author = str(author)
        if creator is not None:
            pdf_entity.creator = str(creator)
        if producer is not None:
            pdf_entity.producer = str(producer)
        if subject is not None:
            pdf_entity.subject = str(subject)
        if title is not None:
            pdf_entity.title = str(title)
        if number_of_pages is not None:
            pdf_entity.number_of_pages = number_of_pages
        if raw_info is not None:
            pdf_entity.raw_info = str(raw_info)
        if content is not None:
            pdf_entity.content = str(content)
        if named_entities is not None:
            pdf_entity.named_entities = str(named_entities)
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
            print("NLTK NER method not supported yet")
        if "spacy" in ner_methods:
            ner_services.append(SpacyNerService())

        named_entities = []

        # For each NER service
        for ner_service in ner_services:
            # We get the named entities list
            temp_named_entities_list = ner_service.extract(text)
            # We merge the named entities list with the previous list
            named_entities = self._merge(named_entities, temp_named_entities_list)

        return named_entities

    def extract_document(self, filename: Path):
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
            document = DocumentEntity(self.config)
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
