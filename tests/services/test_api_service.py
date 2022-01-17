"""
Name: arXiv Intelligence NER Web Service
Authors: Jonathan CASSAING
Web service specialized in Named Entity Recognition (NER), in Natural Language Processing (NLP)
"""

import unittest
import web_service.services as ApiService
from web_service import create_app

class test_ApiService(unittest.TestCase):
    def test_allowed_file(self):
        """Test different file types"""
        with create_app({"TESTING": True}).app_context():
            # Must be OK for PDF file type
            self.assertTrue(ApiService.ApiService().allowed_file("file.pdf"))
            # Must be False for other file types
            self.assertFalse(ApiService.ApiService().allowed_file("file.doc"))
