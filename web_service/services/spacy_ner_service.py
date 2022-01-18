"""
Name: arXiv Intelligence NER Web Service
Authors: Jonathan CASSAING
Web service specialized in Named Entity Recognition (NER), in Natural Language Processing (NLP)
"""

from .ner_interface import NerInterface
from web_service.entities.named_entity import NamedEntity, NamedEntityScoreEnum, NamedEntityTypeEnum

class SpacyNerService(NerInterface):
    def extract(self: object, text: str):
        
        named_entity_1 = NamedEntity()
        named_entity_1.text = "Spacy Entity"
        named_entity_1.score = NamedEntityScoreEnum.MEDIUM
        named_entity_1.type = NamedEntityTypeEnum.PERSON
        named_entity_1.begin_offset = 986
        named_entity_1.end_offset = named_entity_1.begin_offset + len(named_entity_1.text)

        return named_entity_1
