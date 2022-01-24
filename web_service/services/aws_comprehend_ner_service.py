"""
Name: arXiv Intelligence NER Web Service
Authors: Jonathan CASSAING
Web service specialized in Named Entity Recognition (NER), in Natural Language Processing (NLP)
"""

import boto3
import textwrap
from botocore.exceptions import NoCredentialsError, ClientError
from .ner_interface import NerInterface
from web_service.entities.named_entity import NamedEntity, NamedEntityTypeEnum, NamedEntityScoreEnum

class AwsComprehendNerService(NerInterface):

    def __init__(self, aws_region: str = "us-east-1", max_char_per_request: int = 4900):
        self.aws_region = aws_region
        self.max_char_per_request = max_char_per_request

    def _convert_type_to_type_enum(self, type: str) -> NamedEntityTypeEnum:
        """Convert an AWS type to NamedEntityTypeEnum
        See: https://docs.aws.amazon.com/comprehend/latest/dg/how-entities.html
        """
        if type == "DATE":
            return NamedEntityTypeEnum.DATE
        if type == "COMMERCIAL_ITEM":
            return NamedEntityTypeEnum.PRODUCT
        if type == "EVENT":
            return NamedEntityTypeEnum.EVENT
        if type == "LOCATION":
            return NamedEntityTypeEnum.LOCATION
        if type == "ORGANIZATION":
            return NamedEntityTypeEnum.ORGANIZATION
        if type == "PERSON":
            return NamedEntityTypeEnum.PERSON
        if type == "QUANTITY":
            return NamedEntityTypeEnum.QUANTITY
        if type == "TITLE":
            return NamedEntityTypeEnum.TITLE
        return NamedEntityTypeEnum.OTHER

    def extract(self, text: str):
        # We split the text for each 'max_char_per_request' caracters
        lines = textwrap.wrap(text, self.max_char_per_request, break_long_words=False)

        # We init AWS Comprehend
        comprehend = boto3.client(service_name='comprehend', region_name=self.aws_region)

        named_entities = []
        offset = 0
        for line in lines:
            try:
                # We launch an AWS request
                data = comprehend.detect_entities(Text=line, LanguageCode='en')
                # We create the entities
                for entity in data["Entities"]:
                    named_entity = NamedEntity()
                    named_entity.text = entity["Text"]
                    named_entity.type = self._convert_type_to_type_enum(entity["Type"])
                    named_entity.begin_offset = entity["BeginOffset"] + offset
                    named_entity.end_offset = entity["EndOffset"] + offset
                    named_entity.aws_score = entity["Score"]
                    named_entity.score = NamedEntityScoreEnum.LOW
                    named_entities.append(named_entity)
            except NoCredentialsError:
                print("Unable to locate AWS credentials")
            except ClientError:
                print("An error occurred (UnrecognizedClientException) when calling the DetectEntities operation: The security AWS token included in the request is invalid")
            offset += len(line)

        # We must sort the list by begin_offset
        named_entities.sort(key=lambda named_entity: named_entity.begin_offset)

        return named_entities
