"""
Name: arXiv Intelligence NER Web Service
Authors: Jonathan CASSAING
Web service specialized in Named Entity Recognition (NER), in Natural Language Processing (NLP)
"""

import textwrap
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from web_service.entities.named_entity import NamedEntity, NamedEntityTypeEnum, NamedEntityScoreEnum
from web_service.entities.named_entity import NamedEntityRelationshipEnum
from .ner_interface import NerInterface

class AwsComprehendNerService(NerInterface):
    """NER Service from AWS Comprehend"""

    def __init__(self, aws_region: str = "us-east-1", max_char_per_request: int = 4900):
        self.aws_region = aws_region
        self.max_char_per_request = max_char_per_request

    @staticmethod
    def _convert_type_to_type_enum(type_str: str) -> NamedEntityTypeEnum:
        """Convert an AWS type to NamedEntityTypeEnum
        See: https://docs.aws.amazon.com/comprehend/latest/dg/how-entities.html
        """
        ne_type_enum = None
        if type_str == "DATE":
            ne_type_enum = NamedEntityTypeEnum.DATE
        elif type_str == "COMMERCIAL_ITEM":
            ne_type_enum = NamedEntityTypeEnum.PRODUCT
        elif type_str == "EVENT":
            ne_type_enum = NamedEntityTypeEnum.EVENT
        elif type_str == "LOCATION":
            ne_type_enum = NamedEntityTypeEnum.LOCATION
        elif type_str == "ORGANIZATION":
            ne_type_enum = NamedEntityTypeEnum.ORGANIZATION
        elif type_str == "PERSON":
            ne_type_enum = NamedEntityTypeEnum.PERSON
        elif type_str == "QUANTITY":
            ne_type_enum = NamedEntityTypeEnum.QUANTITY
        elif type_str == "TITLE":
            ne_type_enum = NamedEntityTypeEnum.TITLE
        else:
            ne_type_enum = NamedEntityTypeEnum.OTHER
        return ne_type_enum

    def extract(self: object, text: str,
                relationship: NamedEntityRelationshipEnum = NamedEntityRelationshipEnum.QUOTED,
                offset: int = 0):
        # We split the text for each 'max_char_per_request' caracters
        lines = textwrap.wrap(text, self.max_char_per_request, break_long_words=False)

        # We init AWS Comprehend
        comprehend = boto3.client(service_name='comprehend', region_name=self.aws_region)

        named_entities = []
        lines_offset = 0 + offset
        for line in lines:
            try:
                # We launch an AWS request
                data = comprehend.detect_entities(Text=line, LanguageCode='en')
                # We create the entities
                for entity in data["Entities"]:
                    named_entity = NamedEntity()
                    named_entity.text = entity["Text"]
                    named_entity.type = self._convert_type_to_type_enum(entity["Type"])
                    named_entity.begin_offset = entity["BeginOffset"] + lines_offset
                    named_entity.end_offset = entity["EndOffset"] + lines_offset
                    named_entity.aws_score = entity["Score"]
                    named_entity.score = NamedEntityScoreEnum.LOW
                    named_entity.relationship = relationship
                    named_entities.append(named_entity)
            except NoCredentialsError:
                print("Unable to locate AWS credentials")
            except ClientError:
                print("An error occurred (UnrecognizedClientException) \
                when calling the DetectEntities operation: \
                The security AWS token included in the request is invalid")
            lines_offset += len(line)

        # We must sort the list by begin_offset
        named_entities.sort(key=lambda named_entity: named_entity.begin_offset)

        return named_entities
