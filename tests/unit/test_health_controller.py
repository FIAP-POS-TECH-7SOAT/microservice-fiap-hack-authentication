import unittest
from flask import Flask

from src.adapters.drivers.http.controllers.health_controller import health_bp

class TestHealthController(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(health_bp())
        self.client = self.app.test_client()
        
    def test_health_check(self):
        response = self.client.get('/health')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("message", data)
        self.assertEqual(data["message"], "Page Loaded")