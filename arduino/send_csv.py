import requests

url = 'http://johnestrada.org/api'
controller_name = 'a'
filename = 'data.csv'

with open(filename, 'rb') as file:
    requests.post(url + '/csv', data = {'controller': controller_name}, files = {'data': file})
