"""
Name: arXiv Intelligence NER Web Service
Authors: Jonathan CASSAING
Web service specialized in Named Entity Recognition (NER), in Natural Language Processing (NLP)
"""

from abc import ABC, abstractmethod
from web_service.entities.named_entity import NamedEntityRelationshipEnum

class NerInterface(ABC):
    """NER Interface for services"""

    @abstractmethod
    def extract(self: object, text: str,
                relationship: NamedEntityRelationshipEnum = NamedEntityRelationshipEnum.QUOTED,
                offset: int = 0):
        """This function must extract named entities from the text
        Args:
            text (str): text where to search named entities.
            relationship (NamedEntityRelationshipEnum):
            use to set a relationship between the named entities and the text
            offset (int): to set an offset for the named entity location, in the text
        Returns:
            list<NamedEntity>: list of the named entities, must be sorted by begin_offset."""
