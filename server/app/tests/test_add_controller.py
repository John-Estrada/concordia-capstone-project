from django.test import TestCase, Client
from app.models import DataEntry, Controller, Device
import datetime

# default case - first new controller
class AddControllerNormal(TestCase):
    def setUp(self):
        self.client = Client()

    def test(self):
        # 1. controller does not exist yet (normal situation)
        case = 'Normal - controller does not exist yet'
        response = self.client.post('/api/add_controller', {'name':'new_controller'})
        print(f'Case: {case}, response: {response.content}')
        self.assertTrue(response.content == b'{"result": "success", "name": "new_controller", "id": 1, "message": "Added new controller: name=new_controller, id=1"}')
        self.assertTrue(Controller.objects.filter(name='new_controller').exists())


# 2. controller already exists
class AddControllerAlreadyExists(TestCase):
    def setUp(self):
        self.client = Client()
        Controller.objects.create(name="test_controller")
        controller = Controller.objects.get(name="test_controller")

    def test(self):
        case = 'Controller already exists'
        response = self.client.post('/api/add_controller', {'name':'test_controller'})
        print(f'Case: {case}, response: {response.content}')
        self.assertTrue(response.content == b'{"result": "failure", "message": "This controller already exists"}')
        self.assertTrue(len(Controller.objects.all()) == 1)

# 3. controller name empty
class AddControllerNameEmpty(TestCase):
    def setUp(self):
        self.client = Client()
        Controller.objects.create(name="test_controller")
        controller = Controller.objects.get(name="test_controller")

    def test(self):
        case = 'Controller name empty'
        response = self.client.post('/api/add_controller', {'name':''})
        print(f'Case: {case}, response: {response.content}')
        self.assertTrue(response.content == b'{"result": "failure", "message": "Controller name cannot be empty"}')

        # 4. controller name missing
        case = 'Controller name missing'
        response = self.client.post('/api/add_controller')
        print(f'Case: {case}, response: {response.content}')
        self.assertTrue(response.content == b'{"result": "failure", "message": "Controller name missing"}')
