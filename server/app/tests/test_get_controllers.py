from django.test import TestCase, Client
from app.models import DataEntry, Controller, Device
import datetime

class GetAvailableControllers(TestCase):
    def setUp(self):
        self.client = Client()
        Controller.objects.create(name="test_controller")
        controller = Controller.objects.get(name="test_controller")

    def test(self):
        case = "Get controllers - 1 added"
        response = self.client.get('/api/get_available_controllers')
        print(f'Case: {case}, response: {response.content}')
        self.assertTrue(response.content == b'{"result": "success", "controllers": [[1, "test_controller"]]}')

class GetAvailableControllers(TestCase):
    def setUp(self):
        self.client = Client()

    def test(self):
        case = "Get controllers - no controllers exist"
        response = self.client.get('/api/get_available_controllers')
        print(f'Case: {case}, response: {response.content}')
        self.assertTrue(response.content == b'{"result": "success", "controllers": []}')
