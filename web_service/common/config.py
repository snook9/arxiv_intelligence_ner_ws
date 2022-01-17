"""
Name: arXiv Intelligence NER Web Service
Authors: Jonathan CASSAING
Web service specialized in Named Entity Recognition (NER), in Natural Language Processing (NLP)
"""

import sys
import configparser
from pathlib import Path

class Config:
    """Class for accessing config.ini file"""

    def __init__(self: object, ):
        """Initialize the object"""
        config = configparser.ConfigParser()
        # We load the global config file
        config.read('config/config.ini')

        try:
            self.upload_temp_folder = Path(config.get("DEFAULT","upload_temp_folder"))
        except configparser.NoOptionError as err:
            print(f"Error in file config/config.ini: {err=}, {type(err)=}", file=sys.stderr)
            self.upload_temp_folder = Path("tmp")

        try:
            self.allowed_extensions = config.get("DEFAULT","allowed_extensions").split()
        except configparser.NoOptionError as err:
            print(f"Error in file config/config.ini: {err=}, {type(err)=}", file=sys.stderr)
            self.allowed_extensions = "pdf"

        try:
            self.ner_methods = config.get("DEFAULT","ner_methods").split()
        except configparser.NoOptionError as err:
            print(f"Error in file config/config.ini: {err=}, {type(err)=}", file=sys.stderr)
            self.ner_methods = "nltk spacy"

    def get_upload_temp_folder(self):
        """Returns upload_temp_folder"""
        return self.upload_temp_folder

    def get_allowed_extensions(self):
        """Returns allowed_extensions"""
        return self.allowed_extensions
    
    def get_ner_methods(self):
        """Returns allowed_extensions"""
        return self.ner_methods
