from django.test import TestCase
from app.models import DataEntry, Controller, Device
import datetime

# Create your tests here.+
class FirstTestCase(TestCase):
    def setUp(self):
        Controller.objects.create(name="test_controller")
        controller = Controller.objects.get(name="test_controller")
        
        

    def test_that_tests_are_working(self):
        controller = Controller.objects.get(name="test_controller")
        test = 'test'
        
        self.assertTrue(test == 'test')
        self.assertTrue(controller!=None)