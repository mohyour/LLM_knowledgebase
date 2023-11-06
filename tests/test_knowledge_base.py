import json
import shutil
import unittest
from app import create_app


class KnowledgeBaseTestCase(unittest.TestCase):
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

    def test_home(self):
        response = self.client.get("/", data={"content": "hello world"})
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.get_data(as_text=True))
        self.assertEqual(response["data"], "Home page")

    def test_create_knowledge_base(self):
        req = {"knowledge_base": self.test_knowledge_base,
               "document": "hello.txt"}
        response = self.client.post("/knowledge_base", json=req,
                                    content_type="application/json")
        self.assertEqual(response.status_code, 201)
        response = json.loads(response.get_data(as_text=True))
        self.assertEqual(response["message"], "Knowledge base created")

    def test_create_knowledge_base_invalid_document(self):
        req = {"knowledge_base": self.test_knowledge_base,
               "document": "invalid.txt"}
        response = self.client.post("/knowledge_base", json=req,
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_delete_knowledge_base(self):
        req = {"knowledge_base": self.test_knowledge_base,
               "document": "hello.txt"}
        response = self.client.delete("/knowledge_base", json=req,
                                      content_type="application/json")
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.get_data(as_text=True))
        self.assertEqual(response["message"], "Knowledge base deleted")

    def test_delete_knowledge_base_invalid_knowledge_base(self):
        req = {"knowledge_base": "invalid",
               "document": "hello.txt"}
        response = self.client.delete("/knowledge_base", json=req,
                                      content_type="application/json")
        self.assertEqual(response.status_code, 400)
        response = json.loads(response.get_data(as_text=True))
        self.assertEqual(response["message"], "Cannot delete knowledge base, "
                         "check request data and logs")


if __name__ == "__main__":
    unittest.main()
