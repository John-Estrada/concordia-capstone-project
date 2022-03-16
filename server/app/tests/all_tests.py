from django.test import TestCase, Client
from app.models import DataEntry, Controller, Device
import datetime

# post data value
# curl -X POST -F "sensor=temperature" -F "value=32.50" -F "controller=a" "http://localhost:8000/api/generic"
# 0. all values correct
# 1. controller does not exist
# 2. controller does not have the given sensor type
# 3. sensor value empty/not exist
# 4. data value empty/not exist
# 5. controller value empty/not exist

# get data values

# add a controller
# curl -X POST "http://localhost:8000/api/add_controller" -F "name=test_controller"

# get available controllers
# http://localhost:8000/api/get_available_controllers

# get all target params
# http://localhost:8000/api/target?id=1



# update a target param
# curl -X POST "http://localhost:8000/api/target" -F "controller=a" -F "device=temperature" -F "target=123"


# report a new device

