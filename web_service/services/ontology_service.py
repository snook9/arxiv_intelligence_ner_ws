"""
Name: arXiv Intelligence NER Web Service
Authors: Jonathan CASSAING
Web service specialized in Named Entity Recognition (NER), in Natural Language Processing (NLP)
"""

from owlready2 import *
from web_service.entities.named_entity import NamedEntity

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

        with self._foaf:
            person = self._foaf["Person"]
            person.lastName = named_entity.text

        return person.lastName
