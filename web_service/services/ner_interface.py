"""
Name: arXiv Intelligence NER Web Service
Authors: Jonathan CASSAING
Web service specialized in Named Entity Recognition (NER), in Natural Language Processing (NLP)
"""

from abc import ABC, abstractmethod

class NerInterface(ABC):
    @abstractmethod
    def extract(self: object, text: str):
        """This function must extract named entities from the text
        Args:
            text (str): text where to search named entities.
        Returns:
            list<NamedEntity>: list of the named entities, must be sorted by begin_offset."""
        pass
