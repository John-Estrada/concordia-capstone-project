from django.test import TestCase, Client
from app.models import DataEntry, Controller, Device
import datetime

class PostData(TestCase):
    controller = None
    device = None 

    def setUp(self):
        self.client = Client()
        Controller.objects.create(name="test_controller")
        controller = Controller.objects.get(name="test_controller")
        Device.objects.create(name='temperature', controller=controller, target=25.0)


    def test(self):
        case =  'All params missing'
        response = self.client.post('/api/generic')
        print(f'Case: {case}, response: {response.content}')
        self.assertTrue(response.content == b'{"status": "failure", "message": "The following parameters are missing: sensor, value, controller"}')

        # controller missing
        case =  'Controller missing'
        response = self.client.post('/api/generic', {'value': 32.50, 'sensor':'temperature'})
        print(f'Case: {case}, response: {response.content}')
        self.assertTrue(response.content == b'{"status": "failure", "message": "The following parameters are missing: controller"}')

        # value missing
        case =  'Value missing'
        response = self.client.post('/api/generic', {'sensor':'temperature', 'controller': 'test_controller'})
        print(f'Case: {case}, response: {response.content}')
        self.assertTrue(response.content == b'{"status": "failure", "message": "The following parameters are missing: value"}')

        # sensor missing
        case =  'Sensor missing'
        response = self.client.post('/api/generic', {'value': 32.50, 'controller': 'test_controller'})
        print(f'Case: {case}, response: {response.content}')
        self.assertTrue(response.content == b'{"status": "failure", "message": "The following parameters are missing: sensor"}')

        # all params present
        case =  'All params present'
        response = self.client.post('/api/generic', {'value': 32.50, 'controller': 'test_controller', 'sensor': 'temperature'})
        print(f'Case: {case}, response: {response.content}')
        self.assertTrue(response.content == b'{"status": "success"}')
        temp = DataEntry.objects.get(value=32.50)
        self.assertTrue(temp.value == 32.50)

        # controller does not exist
        case =  'Controller does not exist'
        response = self.client.post('/api/generic', {'value': 32.50, 'controller': 'first_controller', 'sensor': 'temperature'})
        print(f'Case: {case}, response: {response.content}')
        self.assertTrue(response.content == b'{"status": "failure", "message": "The specified controller does not exist"}')
