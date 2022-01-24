"""
Name: arXiv Intelligence NER Web Service
Authors: Jonathan CASSAING
Web service specialized in Named Entity Recognition (NER), in Natural Language Processing (NLP)
"""

import spacy
from .ner_interface import NerInterface
from web_service.entities.named_entity import NamedEntity, NamedEntityTypeEnum, NamedEntityScoreEnum

class SpacyNerService(NerInterface):

    def _convert_label_to_type_enum(self, label_: str) -> NamedEntityTypeEnum:
        """Convert a text label to NamedEntityTypeEnum
        Possible values from Spacy en_core_web_sm-3.2.0 are:
        "CARDINAL", "DATE", "EVENT", "FAC", "GPE", "LANGUAGE",
        "LAW", "LOC", "MONEY", "NORP", "ORDINAL", "ORG", "PERCENT",
        "PERSON", "PRODUCT", "QUANTITY", "TIME", "WORK_OF_ART"
        See: https://github.com/explosion/spacy-models/blob/master/meta/en_core_web_sm-3.2.0.json
        """
        if label_ == "DATE":
            return NamedEntityTypeEnum.DATE
        if label_ == "PRODUCT":
            return NamedEntityTypeEnum.PRODUCT
        if label_ == "EVENT":
            return NamedEntityTypeEnum.EVENT
        if label_ == "LOC":
            return NamedEntityTypeEnum.LOCATION
        if label_ == "ORG":
            return NamedEntityTypeEnum.ORGANIZATION
        if label_ == "PERSON":
            return NamedEntityTypeEnum.PERSON
        if label_ == "QUANTITY":
            return NamedEntityTypeEnum.QUANTITY
        return NamedEntityTypeEnum.OTHER

    def extract(self: object, text: str):        
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text)

        named_entities = []

        for ent in doc.ents:
            named_entity = NamedEntity()
            named_entity.text = ent.text
            named_entity.type = self._convert_label_to_type_enum(ent.label_)
            named_entity.begin_offset = ent.start
            named_entity.end_offset = ent.end
            named_entity.score = NamedEntityScoreEnum.LOW

            named_entities.append(named_entity)

        return named_entities
