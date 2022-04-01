#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script for testing Arduino-RaspberryPi serial communication.

Arduino prints lines of comma-separated data to a serial port.
This script reads user-fixed amount of entries from the serial port.
Each entry is formatted, timestamped, and appended to a .csv file.
"""

import serial
import datetime
import csv
import time
import requests
import os
import json

# variables
port = '/dev/ttyACM0'
bauds = 57600
filename = 'dump.csv'
numberOfReadings = 10000
controller_name = 'concordia_greenhouse'
url = 'http://johnestrada.org/api'
# url = 'http://localhost:8000/api'
targets_file_name = 'targets.csv'
targets_history_file = 'targets_log.csv'
column_headers = 'timestamp,air_temp_1,air_temp_2,air_temp_3,air_temp_4,air_rh_1,air_rh_2,air_rh_3,air_rh_4,effluent_temp,effluent_ec25,effluent_ph,effluent_turb_ntu,status,elapsed time'.split(
    ',')
default_temperature_target = 22.0
default_humidity_target = 85.0


def write_from_arduino():
    counter = 0
    data_list = []
    with serial.Serial(port, bauds) as arduino:
        while True:
            arduino_rx = str(arduino.readline())  # read serial from arduino
            data = arduino_rx[2:len(arduino_rx)-5]  # remove header
            data_list = data.split(",")  # split data by comma into entries
            timestamp = int(datetime.datetime.now().timestamp())
            data_list.insert(0, str(timestamp))  # add a timestamp

            arduino.flush()

            create_file()  # check if file exists, if not write the file

            write_data(data_list)  # write data to the csv file

            check_in(counter, 6)  # check in approx every 3 minutes

            # send datastring approx every 3 minutes
            send_datastring(data_list, counter, 1)

            params_to_write = fetch_targets(
                counter, 1)  # fetch targets every minute

            # add writing targets to serial here
            arduino.write(params_to_write.encode('utf-8'))

            arduino.flush()

            counter += 1


def create_file():
    folder_name = 'DataReadings'
    today_date = time.strftime("%Y-%m-%d")
    file_name = time.strftime("%Y-%m-%d_%H")
    file_path = f'{folder_name}/{today_date}/{file_name}.csv'

    if not os.path.exists(f'{folder_name}/{today_date}'):
        os.makedirs(f'{folder_name}/{today_date}')

    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(column_headers)


def write_data(data_list):
    folder_name = 'DataReadings'
    today_date = time.strftime("%Y-%m-%d")
    file_name = time.strftime("%Y-%m-%d_%H")
    file_path = f'{folder_name}/{today_date}/{file_name}.csv'

    if not os.path.exists(file_path):
        print('error - file does not exist')
        return

    with open(file_path, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(data_list)


def send_datastring(datastring, counter, interval):
    if not counter % interval == 0:
        return

    ds_as_string = ''
    for x in datastring:
        ds_as_string = f'{ds_as_string},{x}'

    ds_as_string = ds_as_string[1:]
    print(f'''
    --- begin sending datastring
    {ds_as_string}
    
    ''')

    if counter % interval == 0:
        try:
            requests.post(
                url + '/datastring', data={'controller': controller_name, 'datastring': ds_as_string})
            print('successfully sent datastring')
        except:
            log_error(
                f"{datetime.datetime.now().isoformat()} Cound not complete sending datastring - likely problem with web request")
            print('error sending datastring')


def check_in(counter, interval):
    if counter % interval == 0:
        try:
            requests.post('http://johnestrada.org/api/generic',
                          data={'controller': controller_name, 'sensor': 'check_in', 'value': '0.0'})
        except:
            log_error(
                "Could not complete check in - likely problem with web request")


def fetch_targets(counter, interval):
    if counter % interval != 0:
        return

    targets = {}
    try:
        data = requests.get(
            url + f'/all_targets?controller={controller_name}')
    except:
        log_error(
            f'{datetime.datetime.now().isoformat()} could not fetch targets')

    targets = json.loads(data.content)['results']

    headers = []
    data_list = []
    for param_type in targets:
        headers.append(param_type)
        data_list.append(targets[param_type])

    with open(targets_history_file, 'a') as file:
        writer = csv.writer(file)
        data_list.insert(
            0, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        writer.writerow(data_list)

    params_to_write = ''
    params_to_write += format_float_for_writing(targets['temperature'])
    params_to_write += format_float_for_writing(targets['humidity'])
    params_to_write += '\n'

    print(params_to_write)

    return params_to_write


def log_error(text):
    timestamp = datetime.datetime.now().isoformat(sep=' ', timespec='seconds')
    if not os.path.exists('error_log.txt'):
        with open('error_log.txt', 'w') as f:
            f.write('---- Error Log ----\n')

    with open('error_log.txt', 'a') as f:
        f.write(f'{timestamp} {text}\n')


def format_float_for_writing(input):
    input_string = str(input)
    x = input_string.split('.')

    if (len(x[0])) < 2:
        x[0] = f'0{x[0]}'

    if len(x[1]) < 2:
        x[1] = f'{x[1]}0'

    output = f'{x[0]}.{x[1]}'

    return output


if __name__ == '__main__':
    write_from_arduino()
