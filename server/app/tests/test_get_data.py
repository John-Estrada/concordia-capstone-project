from django.test import TestCase, Client
from app.models import DataEntry, Controller, Device
import datetime

class GetData(TestCase):
    controller = None
    device = None 

    def setUp(self):
        self.client = Client()
        Controller.objects.create(name="test_controller")
        controller = Controller.objects.get(name="test_controller")
        Device.objects.create(name='temperature', controller=controller, target=25.0)
        device = Device.objects.get(name='temperature', controller = controller)
        DataEntry.objects.create(controller=controller, data_type = 'temperature', value = 10.0, timestamp = datetime.datetime.fromtimestamp(1637105911), device = device)

    def test(self):
        # 1. from a specific time range
        # http://localhost:8000/api/generic?sensor=temperature&start=1637105911&end=9999999999&controller=1
        case = 'From a specific time range - data entry exists'
        sensor = 'temperature'
        start = 1637105911
        end = 9999999999
        controller_id = 'test_controller'
        response = self.client.get(f'/api/generic?sensor={sensor}&start={start}&end={end}&controller={controller_id}')
        print(f'Case: {case}, response: {response.content}')
        self.assertTrue(response.content == b'{"status": "success", "results": [["2021-11-16T18:38:31Z", "10.00"]], "sensor": "temperature"}')

        # 2. get data values where results list is empty
        case = 'Controller exists - no data values in time range'
        sensor = 'temperature'
        start = 1037105911
        end = 1637105910
        controller_id = 'test_controller'
        response = self.client.get(f'/api/generic?sensor={sensor}&start={start}&end={end}&controller={controller_id}')
        print(f'Case: {case}, response: {response.content}')
        self.assertTrue(response.content == b'{"status": "success", "results": [], "sensor": "temperature"}')

        # 3. get data values from a sensor that does not exist
        case = 'Sensor does not exist'
        sensor = 'fake_sensor'
        start = 1637105911
        end = 9999999999
        controller_id = 'test_controller'
        response = self.client.get(f'/api/generic?sensor={sensor}&start={start}&end={end}&controller={controller_id}')
        print(f'Case: {case}, response: {response.content}')
        self.assertTrue(response.content == b'{"status": "success", "results": [], "sensor": "fake_sensor"}')

        # 4. get data values from a controller that does not exist
        case = 'Controller does not exist'
        sensor = 'fake_sensor'
        start = 1637105911
        end = 9999999999
        controller_id = 0
        response = self.client.get(f'/api/generic?sensor={sensor}&start={start}&end={end}&controller={controller_id}')
        print(f'Case: {case}, response: {response.content}')
        self.assertTrue(response.content == b'{"status": "failure", "results": "This controller does not exist"}')
