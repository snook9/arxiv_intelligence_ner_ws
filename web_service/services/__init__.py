"""
Name: arXiv Intelligence NER Web Service
Authors: Jonathan CASSAING
Web service specialized in Named Entity Recognition (NER), in Natural Language Processing (NLP)
"""

from .api import Api
from .ner_interface import NerInterface
from .spacy_ner_service import SpacyNerService
from .aws_comprehend_ner_service import AwsComprehendNerService
