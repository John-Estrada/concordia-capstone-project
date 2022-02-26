from django.test import TestCase, Client
from app.models import DataEntry, Controller, Device
import datetime

class GetTargetParametersNoController(TestCase):
    def setUp(self):
        self.client = Client()
        
    def test(self):
        case = "Controller does not exist (get target parameters)"
        response = self.client.get('/api/target?id=1')
        print(f'Case: {case}, response: {response.content}')
        self.assertTrue(response.content == b'{"status": "failed", "message": "This controller does not exist"}')

class GetTargetParametersNoDevices(TestCase):
    def setUp(self):
        self.client = Client()
        self.case = 'Get parameters - no devices'
        Controller.objects.create(name="test_controller")
        controller = Controller.objects.get(name='test_controller')

    def test(self):
        response = self.client.get('/api/target?id=1')
        print(f'Case: {self.case}, response: {response.content}')
        self.assertTrue(response.content == b'{"status": "failed", "controller": "test_controller", "devices": [], "message": "This controller has no devices"}')
        
class GetTargetParametersNoTargets(TestCase):
    def setUp(self):
        self.client = Client()
        self.case = 'Get parameters - target set at 22.0'
        Controller.objects.create(name='test_controller')
        controller = Controller.objects.get(name='test_controller')
        Device.objects.create(name='temperature', controller=controller, target=22.0)

    def test(self):
        response = self.client.get('/api/target?id=1')
        print(f'Case: {self.case}, response: {response.content}')
        self.assertTrue(response.content == b'{"status": "success", "controller": "test_controller", "devices": [{"name": "temperature", "target": 22.0}]}')
