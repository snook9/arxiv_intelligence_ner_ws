"""
Name: arXiv Intelligence NER Web Service
Authors: Jonathan CASSAING
Web service specialized in Named Entity Recognition (NER), in Natural Language Processing (NLP)
"""

from pathlib import Path
from owlready2 import *
from web_service.entities.named_entity import NamedEntity, NamedEntityTypeEnum

class OntologyService():
    """Ontology service"""

    def __init__(self: object):
        self._onto = get_ontology("file://owl/template-arxiv-intelligence.owl").load()
        #self._foaf = get_namespace("http://xmlns.com/foaf/0.1/")
        self._foaf = get_ontology("http://xmlns.com/foaf/spec/index.rdf").load()

        # TODO TEMP CODE à supprimer
        #print(self._onto["Author"])
        print(self._foaf["Person"])
        print(self._foaf["Document"])

    def build_ontology(self: object, named_entity: NamedEntity):
        if named_entity.type == NamedEntityTypeEnum.PERSON:
            with self._onto:
                person = self._foaf.Person(named_entity.text)
                # We split the text after the first space
                full_name = named_entity.text.split(" ", 1)
                try:
                    # We suppose the first word is the first name
                    person.firstName.append(full_name[0])
                except IndexError:
                    pass
                try:
                    # We rest is the last name
                    person.lastName.append(full_name[1])
                except IndexError:
                    pass
                return person

        # Else, we return none
        return None

    def save(self: object, filepath: Path):
        self._onto.save(filepath)
