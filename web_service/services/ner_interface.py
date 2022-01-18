"""
Name: arXiv Intelligence NER Web Service
Authors: Jonathan CASSAING
Web service specialized in Named Entity Recognition (NER), in Natural Language Processing (NLP)
"""

from abc import ABC, abstractmethod

class NerInterface(ABC):
    @abstractmethod
    def extract(self: object, text: str):
        pass
