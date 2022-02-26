from django.test import TestCase, Client
from app.models import DataEntry, Controller, Device
import datetime

class UpdateTargetParameter(TestCase):
    def setUp(self):
        self.case = 'Update parameter - normal'
        self.client = Client()
        Controller.objects.create(name='test_controller')
        controller = Controller.objects.get(name='test_controller')
        Device.objects.create(name='temperature', controller=controller, target = 22.0)

    def test(self):
        response = self.client.post('/api/target', {'id': '1', 'name': 'temperature', 'target': 30.0})
        print(f'Case - {self.case}, response: {response.content}')
