import requests
import json

# url = 'http://johnestrada.org/api'
url = 'http://localhost:8000/api'
controller_name = 'a'

values = ['temperature']
targets = {}

for device in values:
  data = requests.get(url + f'/target?controller={controller_name}&type={device}')
  target = json.loads(data.content)['target']
  targets[device] = target

for x in targets:
  print(f'{x} : {targets[x]}')

