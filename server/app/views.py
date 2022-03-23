from os import times
from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt
import pytz
from .models import *
import datetime
from django.conf import settings
import csv
import pprint
import time
from django.db import connection
from .util import *

# Create your views here.


def test_view(request):
    return JsonResponse({'test': 'if you can see this, the server is running'})

# for getting and posting data from a user-defined generic sensor type


@csrf_exempt
def generic(request):
    out = {'status': 'failure'}
    missing_parameters = False

    # arduino uses this to send data to the server
    if request.method == 'POST':
        print(request.POST)
        server_time = datetime.datetime.now(pytz.timezone('US/Eastern'))

        expected_parameters = ['sensor', 'value', 'controller']
        for param in expected_parameters:
            if param not in request.POST:
                missing_parameters = True
                if 'message' not in out:
                    out['message'] = 'The following parameters are missing:'
                out['message'] = f"{out['message']} {param},"

        if missing_parameters:
            out['message'] = out['message'][:-1]
            return JsonResponse(out)

        data_type = request.POST['sensor']
        value = float(request.POST['value'])
        controller_name = request.POST['controller']  # name
        print(f'NAME: {Controller.objects.all()}')

        try:
            controller = Controller.objects.get(name=controller_name)
        except Controller.DoesNotExist:
            out['message'] = 'The specified controller does not exist'
            return JsonResponse(out)

        print(
            f"Controller found: id: {controller.id}, name: {controller.name}")

        print(
            f'type: {data_type}, value: {value}, timestamp: {server_time}, controller: {controller_name}')

        x = DataEntry.objects.create(
            data_type=data_type, value=value, timestamp=server_time, controller=controller)
        x.save()

        out['status'] = 'success'

    # client uses this to get data for the user
    elif request.method == 'GET':
        out['results'] = []

        data_type = request.GET.get('sensor')
        controller_name = request.GET.get('controller')
        start = datetime.datetime.fromtimestamp(int(request.GET.get('start')), pytz.timezone('US/Eastern'))
        end = datetime.datetime.fromtimestamp(int(request.GET.get('end')), pytz.timezone('US/Eastern'))

        print(
            f'-------- Parameters --------\ndata type: {data_type}, start: {start}, end: {end}, controller: {controller_name}\n-------- End Parameters --------')

        if Controller.objects.filter(name=controller_name).exists() == False:
            out['results'] = 'This controller does not exist'
            return JsonResponse(out)

        controller = Controller.objects.get(name=controller_name)

        res = DataEntry.objects.filter(data_type=data_type, timestamp__range=[
                                       start, end], controller=controller)

        print(f'-------- Results --------')

        if (res == None):
            print("No results found")

        for x in res:
            out['results'].append(
                [str(x.timestamp.astimezone(pytz.timezone("US/Eastern")))[0:-6], round(x.value, 2)])
            print(f'{str(x.timestamp.astimezone(pytz.timezone("US/Eastern")))[0:-6]}, value: {x.value}')

        print(f'-------- End Results --------')

        out['sensor'] = data_type

        out['status'] = 'success'

    response = JsonResponse(out)
    response['Access-Control-Allow-Origin'] = '*'

    return response

# for posting data in the format of a datastring
# "controller_name,timestamp,temperature,rh,ec,ph"
#   0                   1       2        3  4  5
# timestamp,temp1,temp2,temp3,temp4,rh1,rh2,rh3,rh4,efftemp,effec,turbidity

# timestamp,air_temp_1,air_temp_2,air_temp_3,air_temp_4,air_rh_1,air_rh_2,air_rh_3,air_rh_4,effluent_temp,effluent_ec25,effluent_ph,effluent_turb_ntu,status,elapsed time
# status is a string of 8 characters:
# //bit 0: bottom tank level (FULL=1)
# //bit 1: top tank level (FULL=1)
# //bit 2: pump (ON=1)
# //bit 3: peltier (ON=1)
# //bit 4: vent (ON=1)
# //bit 5: reserved for future use
# //bit 6: reserved for future use
# //bit 7: reserved, always 1 for printing purposes
# Where "bit 7" IS THE LEFTMOST (first) character


@csrf_exempt
def post_with_datastring(request):
    out = {'result': 'failure'}

    print(f'post by datastring')
    print(f'datastring: {request.POST["datastring"]}')

    expected_format = 'timestamp,air_temp_1,air_temp_2,air_temp_3,air_temp_4,air_rh_1,air_rh_2,air_rh_3,air_rh_4,effluent_temp,effluent_ec25,effluent_ph,effluent_turb_ntu,status,elapsed_time'.split(
        ',')

    status_titles = ['format', 'reserved', 'reserved', 'vent', 'peltier', 'pump', 'top_tank', 'bottom_tank']
    

    if request.method == 'POST':
        try:
            values = request.POST['datastring'].split(',')
        except:
            out['message'] = 'datastring missing'
            return JsonResponse(out)

        if len(values) < len(expected_format):
            print(len(values))
            print(len(expected_format))
            out['message'] = 'datastring too short - check for missing values'
            return JsonResponse(out)
        
        if len(values) > len(expected_format):
            print(len(values))
            print(len(expected_format))
            print(expected_format[len(expected_format)-1])
            print(values[len(values)-1])
            out['message'] = 'datastring too long - check for extra values'
            return JsonResponse(out)

        controller = get_controller_or_none(request)
        if controller == None:
            out['message'] = 'this controller does not exist'
            return JsonResponse(out)
        
        timestamp = datetime.datetime.fromisoformat(int(values[0]))
        
        print(timestamp.astimezone(pytz.timezone('Canada/Eastern')))

        data_to_add = []

        for x in range(1, len(expected_format)-2):
            # print(f'title: {expected_format[x]}, value: {values[x]}')
            data_to_add.append(DataEntry(timestamp = timestamp, value = float(values[x]), controller=controller, data_type=expected_format[x]))

        status = values[len(expected_format)-2]
        for x in range(3, len(status)):
            # print(f'{status_titles[x]}, {status[x]}')
            data_to_add.append(DataEntry(timestamp=timestamp, value=float(status[x]), controller=controller, data_type=status_titles[x]))


        for x in data_to_add:
            print(f'{x.value}, {x.data_type}')

        DataEntry.objects.bulk_create(data_to_add)

    out['result'] = 'success'

    return JsonResponse(out)


@csrf_exempt
def add_controller(request):
    out = {'result': 'failure'}

    if request.method == 'POST':
        name = None
        try:
            name = request.POST['name']
        except:
            out['message'] = 'Controller name missing'
            return JsonResponse(out)

        if Controller.objects.filter(name=name).exists():
            out['message'] = 'This controller already exists'
            print('this controller already exists')
        elif name == '':
            out['message'] = 'Controller name cannot be empty'
        else:
            Controller.objects.create(name=name)
            controller = Controller.objects.get(name=name)
            out['name'] = controller.name
            out['id'] = controller.id
            out['result'] = 'success'
            out['message'] = f'Added new controller: name={controller.name}, id={controller.id}'

            print(
                f'Added new controller: name={controller.name}, id={controller.id}')

    response = JsonResponse(out)
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Headers'] = 'Content-Type'

    return response


@csrf_exempt
def get_available_controllers(request):
    out = {'result': 'failure'}

    controllers = Controller.objects.all()

    if controllers != None:
        out['result'] = 'success'

    controllers_list = []

    for x in controllers:
        controllers_list.append([x.id, x.name])

    out['controllers'] = controllers_list

    response = JsonResponse(out)
    response['Access-Control-Allow-Origin'] = '*'

    return response


@csrf_exempt
def get_data_as_csv(request):
    out = {'result': 'failure'}

    data_type = request.GET.get('sensor')
    controller_name = request.GET.get('controller')
    start = datetime.datetime.fromtimestamp(int(request.GET.get('start')))
    end = datetime.datetime.fromtimestamp(int(request.GET.get('end')))

    print(
        f'-------- Parameters --------\ndata type: {data_type}, start: {start}, end: {end}, controller: {controller_name}\n-------- End Parameters --------')

    if Controller.objects.filter(name=controller_name).exists() == False:
        out['results'] = 'This controller does not exist'
        return JsonResponse(out)

    controller = Controller.objects.get(name=controller_name)

    res = DataEntry.objects.filter(data_type=data_type, timestamp__range=[
                                   start, end], controller=controller)

    response = HttpResponse(
        content_type='text/csv',
    )

    response['Content-Disposition'] = 'attachment; filename="data.csv"'

    writer = csv.writer(response)

    writer.writerow(['Type', data_type])
    writer.writerow(['Controller', controller_name])
    writer.writerow('')
    writer.writerow(['timestamp', 'value'])

    for x in res:
        writer.writerow([x.timestamp, x.value])

    return response

# Get and set target parameters


@csrf_exempt
def target_parameter(request):
    out = {'status': 'failed'}

    if request.method == "GET":
        # get in the form ?controller=a&type=temperature
        # expected return is value=22.0
        expected_parameters = ['controller', 'type']
        params_missing_status = validate_params_missing(
            expected_parameters, request.GET)
        if params_missing_status['message'] != 'normal':
            return JsonResponse(params_missing_status)

        try:
            controller_name = request.GET.get('controller')
            type = request.GET.get('type')

        except:
            out['message'] = 'parameter not in correct format'
            return JsonResponse(out)

        if not Controller.objects.filter(name=controller_name).exists():
            out['message'] = 'controller does not exist'
            return JsonResponse(out)

        controller = Controller.objects.get(name=controller_name)

        if not Target.objects.filter(controller=controller, type=type).exists():
            out['message'] = 'no target set'
            return JsonResponse(out)

        target_value = Target.objects.get(
            controller=controller, type=type).value

        out['status'] = 'success'
        out['target'] = target_value

        print('get')

    elif request.method == "POST":
        # send in the form controller=a, type=temperature, value=22.0
        pprint.pprint(request.POST)
        expected_parameters = ['controller', 'type', 'value']
        missing = []
        for param in expected_parameters:
            if param not in request.POST:
                missing.append(param)

        if len(missing) > 0:
            out['message'] = 'parameters missing'
            out['missing_parameters'] = missing
            return JsonResponse(out)

        try:
            controller_name = request.POST['controller']
            parameter_name = request.POST['type']
            value = float(request.POST['value'])
        except:
            out['message'] = 'parameter in incorrect format'
            return JsonResponse(out)

        # check if controller exists
        if not Controller.objects.filter(name=controller_name).exists():
            out['message'] = 'this controller does not exist'
            return JsonResponse(out)

        controller = Controller.objects.get(name=controller_name)

        Target.objects.create(controller=controller,
                              type=parameter_name, value=value)

    out['status'] = 'success'

    print(f'-------- Output --------')
    pprint.pprint(out)
    print(f'-------- End Output --------')

    response = JsonResponse(out)
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Headers'] = 'Content-Type'

    return response


@csrf_exempt
def remove_target(request):
    out = {'status': 'failed'}
    if request.method == 'POST':
        type = request.POST['type']
        controller_name = request.POST['controller']
        controller = Controller.objects.get(name=controller_name)

        Target.objects.filter(controller=controller, type=type).delete()

        out['status'] = 'success'
        return JsonResponse(out)

    return JsonResponse(out)


@csrf_exempt
def all_targets(request):
    out = {'status': 'failed'}

    params_status = validate_params_missing(['controller'], request.GET)
    print(params_status)
    if (params_status['message'] != 'normal'):
        out['message'] = 'controller name missing'
        return JsonResponse(out)

    if not Controller.objects.filter(name=request.GET.get('controller')).exists():
        out['message'] = 'this controller does not exist'
        return JsonResponse(out)

    controller = Controller.objects.get(name=request.GET.get('controller'))

    targets = Target.objects.filter(controller=controller)

    targets_dict = {}
    for x in targets:
        targets_dict[x.type] = x.value

    out['results'] = targets_dict
    out['status'] = 'success'

    return JsonResponse(out)


# For arduino to report available devices to the server
'''
Sample input
{
    controller: 1,
    name: 'temperature', 
    target: 25.0,
}
'''


@csrf_exempt
def report_device(request):
    out = {'message': 'failure'}

    # input : controller id, [(device name, target), ...]

    # post
    if request.method == 'POST':
        controller_id = request.POST['controller']
        device_name = request.POST['name']
        target = request.POST['target']

        controller = Controller.objects.filter(id=controller_id).first()
        # if controller does not exist, return error message
        if controller == None:
            out['message'] = 'Controller does not exist'
            return JsonResponse(out)

        # create a new device and save it
        device = Device.objects.filter(
            controller=controller, name=device_name).first()

        if device == None:
            Device.objects.create(controller=controller,
                                  name=device_name, target=target)
            out['message'] = 'success'
            return JsonResponse(out)

        # if device with same name and controller exists, inform client
        else:
            out['message'] = 'This device already exists'

    return JsonResponse(out)


@csrf_exempt
def post_as_csv(request):
    # controller doesn't exist / not right format
    out = {'status': 'failure'}

    if request.method == 'POST':
        file = (request.FILES['data'].read().decode('utf-8'))
        controller = Controller.objects.get(name=request.POST["controller"])
        lines = file.splitlines()
        print(lines)

        reader = csv.reader(lines)
        parsed = list(reader)
        entries = []

        for column in range(1, len(parsed[0])):
            column_name = parsed[0][column]

            print(f'column: {column_name}')
            for row in parsed[1:]:
                timestamp = datetime.datetime.fromisoformat(row[0])
                print(
                    f'type: {column_name}, time: {row[0]}, data: {row[column]}')

                entries.append(DataEntry(data_type=column_name, value=float(
                    row[column]), timestamp=timestamp, controller=controller))

        DataEntry.objects.bulk_create(entries)

    out['status'] = 'success'

    return JsonResponse(out)


'''
input : {controller: a}
output : {data_types: [temperature, humidity, ph], controller: a}
'''


@csrf_exempt
def controller_has_data(request):
    out = {'result': 'failure'}

    # handle missing parameters
    if (request.GET.get('controller')) == None or request.GET.get('controller') == '':
        out['message'] = 'controller name missing'
        return JsonResponse(out)

    # check if controller exists
    if not (Controller.objects.filter(name=request.GET.get('controller')).exists()):
        out['message'] = 'this controller does note exist'
        return JsonResponse(out)

    controller_name = Controller.objects.get(
        name=request.GET.get('controller')).name
    print(f'name is {controller_name}')

    # get list of data types that this controller has and return to the user
    data_types = []
    results = DataEntry.objects.filter(
        controller=Controller.objects.get(name=controller_name))

    for x in results:
        if x.data_type not in data_types:
            data_types.append(x.data_type)

    out['data_types'] = data_types
    out['result'] = 'success'

    return JsonResponse(out)


def db_testing(request):
    out = {'db': 'done'}
    start = time.time()

    print(DataEntry.objects.filter(controller=Controller.objects.get(id=1)))

    end = time.time()
    print(f"time: {end-start}")
    return JsonResponse(out)


def home(request):
    out = {'test': 'answer'}

    return render(request, 'app/home.html')
