from django.test import TestCase, Client
from app.models import DataEntry, Controller, Device
import datetime

# datastring too short
class TooShort(TestCase):
    def setUp(self):
        self.case = 'Datastring - too short'
        self.client = Client()
        Controller.objects.create(name='test_controller')
        controller = Controller.objects.get(name='test_controller')
        Device.objects.create(name='temperature', controller=controller, target=22.0)

    def test(self):
        response = self.client.post('/api/datastring', {'datastring': 'test_controller,1645595126'})
        print(f'Case - {self.case}, response: {response.content}')
        self.assertTrue(response.content == b'{"result": "failure", "message": "Data string is too short - check whether any values are missing. Expected format is: controller_name,timestamp,temperature,rh,ec,ph"}')

# datastring normal
class Normal(TestCase):
    def setUp(self):
        self.case = 'Datastring - normal'
        self.client = Client()
        Controller.objects.create(name='test_controller')
        controller = Controller.objects.get(name='test_controller')
        Device.objects.create(name='temperature', controller=controller, target=22.0)

    def test(self):
        response = self.client.post('/api/datastring', {'datastring': 'test_controller,1645595126,22.0,23.0,24.0,25.0'})
        print(f'Case - {self.case}, response: {response.content}')
        self.assertTrue(response.content == b'{"result": "success"}')
        temp = DataEntry.objects.filter(data_type = 'temperature', timestamp=datetime.datetime.fromtimestamp(int('1645595126'))).first()
        rh = DataEntry.objects.filter(data_type = 'humidity', timestamp=datetime.datetime.fromtimestamp(int('1645595126'))).first()
        ec = DataEntry.objects.filter(data_type = 'conductivity', timestamp=datetime.datetime.fromtimestamp(int('1645595126'))).first()
        ph = DataEntry.objects.filter(data_type = 'ph', timestamp=datetime.datetime.fromtimestamp(int('1645595126'))).first()
        self.assertTrue(temp.value == 22.0)
        self.assertTrue(rh.value == 23.0)
        self.assertTrue(ec.value == 24.0)
        self.assertTrue(ph.value == 25.0)
        print(f'temp - {temp.value}')

# datastring missing 
class DataStringMissing(TestCase):
    def setUp(self):
        self.case = 'Datastring - datastring missing'
        self.client = Client()
        Controller.objects.create(name='test_controller')
        controller = Controller.objects.get(name='test_controller')
        Device.objects.create(name='temperature', controller=controller, target=22.0)

    def test(self):
        response = self.client.post('/api/datastring')
        print(f'Case - {self.case}, response: {response.content}')
        self.assertTrue(response.content == b'{"result": "failure", "message": "Datastring missing"}')
        temp = DataEntry.objects.filter(data_type = 'temperature', timestamp=datetime.datetime.fromtimestamp(int('1645595126')))
        self.assertTrue(not temp.exists())

# controller missing
class ControllerMissing(TestCase):
    def setUp(self):
        self.case = 'Datastring - controller missing'
        self.client = Client()
        Controller.objects.create(name='test_controller')
        controller = Controller.objects.get(name='test_controller')
        Device.objects.create(name='temperature', controller=controller, target=22.0)

    def test(self):
        response = self.client.post('/api/datastring', {'datastring': 'aaaaa,1645595126,22.0,23.0,24.0,25.0'})
        print(f'Case - {self.case}, response: {response.content}')
        self.assertTrue(response.content == b'{"result": "failure", "message": "The controller aaaaa does not exist"}')
        temp = DataEntry.objects.filter(data_type = 'temperature', timestamp=datetime.datetime.fromtimestamp(int('1645595126')))
        self.assertTrue(not temp.exists())

# value not a float
class ValueNotFloat(TestCase):
    def setUp(self):
        self.case = 'Datastring - value not float'
        self.client = Client()
        Controller.objects.create(name='test_controller')
        controller = Controller.objects.get(name='test_controller')
        Device.objects.create(name='temperature', controller=controller, target=22.0)

    def test(self):
        response = self.client.post('/api/datastring', {'datastring': 'test_controller,1645595126,aaaa,23.0,24.0,25.0'})
        print(f'Case - {self.case}, response: {response.content}')
        self.assertTrue(response.content == b'{"result": "failure", "message": "One of the values is not a float - check datastring format"}')
        temp = DataEntry.objects.filter(data_type = 'temperature', timestamp=datetime.datetime.fromtimestamp(int('1645595126')))
        self.assertTrue(not temp.exists())
