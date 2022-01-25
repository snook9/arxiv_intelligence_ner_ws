"""
Name: arXiv Intelligence NER Web Service
Authors: Jonathan CASSAING
Web service specialized in Named Entity Recognition (NER), in Natural Language Processing (NLP)
"""

import spacy
from web_service.entities.named_entity import NamedEntity, NamedEntityTypeEnum, NamedEntityScoreEnum
from .ner_interface import NerInterface

class SpacyNerService(NerInterface):
    """NER Service from Spacy library"""

    @staticmethod
    def _convert_label_to_type_enum(label_: str) -> NamedEntityTypeEnum:
        """Convert a text label to NamedEntityTypeEnum
        Possible values from Spacy en_core_web_sm-3.2.0 are:
        "CARDINAL", "DATE", "EVENT", "FAC", "GPE", "LANGUAGE",
        "LAW", "LOC", "MONEY", "NORP", "ORDINAL", "ORG", "PERCENT",
        "PERSON", "PRODUCT", "QUANTITY", "TIME", "WORK_OF_ART"
        See: https://github.com/explosion/spacy-models/blob/master/meta/en_core_web_sm-3.2.0.json
        """
        type_enum = None
        if label_ == "DATE":
            type_enum = NamedEntityTypeEnum.DATE
        elif label_ == "PRODUCT":
            type_enum = NamedEntityTypeEnum.PRODUCT
        elif label_ == "EVENT":
            type_enum = NamedEntityTypeEnum.EVENT
        elif label_ == "LOC":
            type_enum = NamedEntityTypeEnum.LOCATION
        elif label_ == "ORG":
            type_enum = NamedEntityTypeEnum.ORGANIZATION
        elif label_ == "PERSON":
            type_enum = NamedEntityTypeEnum.PERSON
        elif label_ == "QUANTITY":
            type_enum = NamedEntityTypeEnum.QUANTITY
        else:
            type_enum = NamedEntityTypeEnum.OTHER
        return type_enum

    def extract(self: object, text: str):
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text)

        named_entities = []

        for ent in doc.ents:
            named_entity = NamedEntity()
            named_entity.text = ent.text
            named_entity.type = self._convert_label_to_type_enum(ent.label_)
            named_entity.begin_offset = ent.start_char
            named_entity.end_offset = ent.end_char
            named_entity.score = NamedEntityScoreEnum.LOW

            named_entities.append(named_entity)

        return named_entities
