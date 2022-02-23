from django.test import TestCase, Client
from app.models import DataEntry, Controller, Device
import datetime

# TODO: implement these test cases
# post data value
# curl -X POST -F "sensor=temperature" -F "value=32.50" -F "controller=a" "http://localhost:8000/api/generic"
# 0. all values correct
# 1. controller does not exist
# 2. controller does not have the given sensor type
# 3. sensor value empty/not exist
# 4. data value empty/not exist
# 5. controller value empty/not exist


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

# get data values
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
        controller_id = 1
        response = self.client.get(f'/api/generic?sensor={sensor}&start={start}&end={end}&controller={controller_id}')
        print(f'Case: {case}, response: {response.content}')
        self.assertTrue(response.content == b'{"status": "success", "results": [["2021-11-16T18:38:31Z", "10.00"]], "sensor": "temperature"}')

        # 2. get data values where results list is empty
        case = 'Controller exists - no data values in time range'
        sensor = 'temperature'
        start = 1037105911
        end = 1637105910
        controller_id = 1
        response = self.client.get(f'/api/generic?sensor={sensor}&start={start}&end={end}&controller={controller_id}')
        print(f'Case: {case}, response: {response.content}')
        self.assertTrue(response.content == b'{"status": "success", "results": [], "sensor": "temperature"}')

        # 3. get data values from a sensor that does not exist
        case = 'Sensor does not exist'
        sensor = 'fake_sensor'
        start = 1637105911
        end = 9999999999
        controller_id = 1
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

# add a controller
# curl -X POST "http://localhost:8000/api/add_controller" -F "name=test_controller"
class AddController(TestCase):
    def setUp(self):
        self.client = Client()
        Controller.objects.create(name="test_controller")
        controller = Controller.objects.get(name="test_controller")

    def test(self):
        # 1. controller does not exist (normal situation)
        case = 'Normal - controller does not exist yet'
        response = self.client.post('/api/add_controller', {'name':'new_controller'})
        print(f'Case: {case}, response: {response.content}')
        self.assertTrue(response.content == b'{"result": "success", "name": "new_controller", "id": 2, "message": "Added new controller: name=new_controller, id=2"}')

        # 2. controller already exists
        case = 'Controller already exists'
        response = self.client.post('/api/add_controller', {'name':'test_controller'})
        print(f'Case: {case}, response: {response.content}')
        self.assertTrue(response.content == b'{"result": "failure", "message": "This controller already exists"}')


        # 3. controller name empty
        case = 'Controller name empty'
        response = self.client.post('/api/add_controller', {'name':''})
        print(f'Case: {case}, response: {response.content}')
        self.assertTrue(response.content == b'{"result": "failure", "message": "Controller name cannot be empty"}')

        # 4. controller name missing
        case = 'Controller name missing'
        response = self.client.post('/api/add_controller')
        print(f'Case: {case}, response: {response.content}')
        self.assertTrue(response.content == b'{"result": "failure", "message": "Controller name missing"}')

# get available controllers
# http://localhost:8000/api/get_available_controllers
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

# get all target params
# http://localhost:8000/api/target?id=1

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


# update a target param
# curl -X POST "http://localhost:8000/api/target" -F "controller=a" -F "device=temperature" -F "target=123"
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


# report a new device

# datastring too short
class PostWithDataStringTooShort(TestCase):
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
class PostWithDataStringNormal(TestCase):
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
class PostWithDataStringControllerMissing(TestCase):
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
class PostWithDataStringValueNotFloat(TestCase):
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
