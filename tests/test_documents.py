import json
import shutil
import unittest
from app import create_app


class DocumentsTestCase(unittest.TestCase):
    def setUp(self):
        app = create_app()
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()
        self.test_knowledge_base = "app_test/test"

    def tearDown(self):
        self.ctx.pop()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree("vector_store/app_test")

    def test_add_document_knowledge_base(self):
        req = {"knowledge_base": self.test_knowledge_base,
               "document": "hello.txt"}
        response = self.client.post("/document", json=req,
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.get_data(as_text=True))
        self.assertEqual(response["message"], "Document added to "
                         "knowledge base")

    def test_add_document_knowledge_base_invalid_document(self):
        req = {"knowledge_base": self.test_knowledge_base,
               "document": "invalid.txt"}
        response = self.client.post("/document", json=req,
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_delete_document_from_knowledge_base(self):
        req = {"knowledge_base": self.test_knowledge_base,
               "document": "hello.txt"}
        response = self.client.delete("/document", json=req,
                                      content_type="application/json")
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.get_data(as_text=True))
        self.assertEqual(response["message"], "Document deleted from "
                         "knowledge base")

    def test_delete_document_from_knowledge_base_invalid_input(self):
        req = {"knowledge_base": "invalid",
               "document": "hello.txt"}
        response = self.client.delete("/document", json=req,
                                      content_type="application/json")
        self.assertEqual(response.status_code, 400)
        response = json.loads(response.get_data(as_text=True))
        self.assertEqual(response["error"], "Cannot delete document, check "
                         "request data")

    def test_get_similar_documents_from_knowledge_base(self):
        self.test_add_document_knowledge_base()
        query_string = "knowledge_base=%s&query_doc=hello.txt" % \
            self.test_knowledge_base
        print(query_string)
        response = self.client.get(f"/documents?{query_string}")
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.get_data(as_text=True))
        self.assertEqual(len(response["documents"]), 1)

    def test_get_similar_documents_knowledge_base_invalid_knowledge_base(self):
        query_string = "knowledge_base=invalid&query_doc=hello.txt"
        print(query_string)
        response = self.client.get(f"/documents?{query_string}")
        self.assertEqual(response.status_code, 400)
        response = json.loads(response.get_data(as_text=True))
        self.assertEqual(response["error"], "Cannot get similar documents, "
                         "check query params")


if __name__ == "__main__":
    unittest.main()
