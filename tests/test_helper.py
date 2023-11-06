import shutil
import unittest
import os
from app import helper


class HelperTestCase(unittest.TestCase):
    valid_document = "railway.txt"
    invalid_document = "invalid.txt"
    knowledge_base = "vector_store/app_test/test"

    def tearDown(self):
        if os.path.isdir("vector_store/app_test"):
            shutil.rmtree("vector_store/app_test")

    def test_create_knowledge_base(self):
        result = helper.create_knowledge_base(self.valid_document,
                                              self.knowledge_base)
        self.assertIsNone(result)
        self.assertTrue(os.path.isdir(self.knowledge_base))

    def test_create_knowledge_base_already_exist(self):
        helper.create_knowledge_base(self.valid_document,
                                     self.knowledge_base)
        with self.assertRaises(Exception):
            helper.create_knowledge_base(self.valid_document,
                                         self.knowledge_base)

    def test_delete_knowledge_base(self):
        helper.create_knowledge_base(self.valid_document,
                                     self.knowledge_base)
        result = helper.delete_knowledge_base(self.knowledge_base)
        self.assertIsNone(result)
        self.assertFalse(os.path.isdir(self.knowledge_base))

    def test_delete_non_existing_knowledge_base(self):
        with self.assertRaises(OSError):
            helper.delete_knowledge_base("invalid_knowledge_base")

    def test_add_document_to_existing_knowledge_base(self):
        helper.create_knowledge_base(self.valid_document,
                                     self.knowledge_base)
        result = helper.add_document_to_knowledge_base(self.valid_document,
                                                       self.knowledge_base)
        self.assertIsNone(result)
        self.assertTrue(os.path.isdir(self.knowledge_base))

    def test_add_document_to_new_knowledge_base_creates_knowledge_base(self):
        new_knowledge_base = "vector_store/app_test/test"
        result = helper.add_document_to_knowledge_base(self.valid_document,
                                                       new_knowledge_base)
        self.assertIsNone(result)
        self.assertTrue(os.path.isdir(new_knowledge_base))

    def test_add_document_invalid_document(self):
        with self.assertRaises(Exception):
            helper.add_document_to_knowledge_base(self.invalid_document,
                                                  self.knowledge_base)

    def test_delete_document_from_knowledge_base(self):
        helper.create_knowledge_base(self.valid_document,
                                     self.knowledge_base)
        result = helper.delete_document_from_knowledge_base(
            self.valid_document, self.knowledge_base)
        self.assertIsNone(result)

    def test_delete_document_from_knowledge_base_invalid(self):
        helper.create_knowledge_base(self.valid_document,
                                     self.knowledge_base)
        result = helper.delete_document_from_knowledge_base(
            self.valid_document, self.knowledge_base)
        self.assertIsNone(result)

    def test_find_similar_documents(self):
        query_doc = "stephen.txt"
        hello_doc = "hello.txt"
        helper.add_document_to_knowledge_base(self.valid_document,
                                              self.knowledge_base)
        helper.add_document_to_knowledge_base(hello_doc,
                                              self.knowledge_base)
        result = helper.find_similar_document(query_doc,
                                              self.knowledge_base)
        self.assertIsNotNone(result)
        self.assertEqual(type(result), list)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0][0].metadata["source"], self.valid_document)
        self.assertEqual(result[1][0].metadata["source"], hello_doc)

    def test_similar_documents_empty_when_no_docs(self):
        query_doc = "stephen.txt"
        helper.add_document_to_knowledge_base(self.valid_document,
                                              self.knowledge_base)
        helper.delete_document_from_knowledge_base(self.valid_document,
                                                   self.knowledge_base)
        result = helper.find_similar_document(query_doc,
                                              self.knowledge_base)
        self.assertIsNotNone(result)
        self.assertEqual(type(result), list)
        self.assertEqual(len(result), 0)
