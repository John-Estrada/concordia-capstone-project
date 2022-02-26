from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Controller, DataEntry, Device
import datetime
from django.conf import settings
import csv
import pprint

# Create your views here.
def test_view(request):
    return JsonResponse({'test': 'answer'})

# for getting and posting data from a user-defined generic sensor type
@csrf_exempt 
def generic(request):
    out = {'status':'failure'}
    missing_parameters = False

    # arduino uses this to send data to the server
    if request.method == 'POST':
        print(request.POST)
        server_time = datetime.datetime.now()

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
        controller_name = request.POST['controller'] #name
        print(f'NAME: {Controller.objects.all()}')
        

        try:
            controller = Controller.objects.get(name=controller_name)
        except Controller.DoesNotExist:
            out['message'] = 'The specified controller does not exist'
            return JsonResponse(out)

        print(f"Controller found: id: {controller.id}, name: {controller.name}")

        print(f'type: {data_type}, value: {value}, timestamp: {server_time}, controller: {controller_name}')


        x = DataEntry.objects.create(data_type = data_type, value=value, timestamp=server_time, controller = controller)
        x.save()

        out['status'] = 'success'

    # client uses this to get data for the user
    elif request.method == 'GET':
        out['results'] = []

        data_type = request.GET.get('sensor')
        controller_name = request.GET.get('controller')
        start = datetime.datetime.fromtimestamp(int(request.GET.get('start')))
        end = datetime.datetime.fromtimestamp(int(request.GET.get('end')))

        print(f'-------- Parameters --------\ndata type: {data_type}, start: {start}, end: {end}, controller: {controller_name}\n-------- End Parameters --------')

        if Controller.objects.filter(name=controller_name).exists() == False:
            out['results'] = 'This controller does not exist'
            return JsonResponse(out)

        controller = Controller.objects.get(name=controller_name)           

        res = DataEntry.objects.filter(data_type = data_type, timestamp__range=[start, end], controller = controller)

        print(f'-------- Results --------')

        if (res == None):
            print("No results found")

        for x in res:
            out['results'].append([x.timestamp, round(x.value, settings.DATA_DECIMAL_PLACES)])
            print(f'{x.timestamp}, value: {x.value}')

        print(f'-------- End Results --------')

        out['sensor'] = data_type

        out['status'] = 'success'
    
    response = JsonResponse(out)
    response['Access-Control-Allow-Origin'] = '*'

    return response

# for posting data in the format of a datastring
# "controller_name,timestamp,temperature,rh,ec,ph"
#   0                   1       2        3  4  5
@csrf_exempt
def post_with_datastring(request):
    out = {'result': 'failure'}
    data_titles = ['timestamp', 'controller_name', 'temperature', 'humidity', 'conductivity', 'ph']


    if request.method == 'POST':
        try:
            data = request.POST['datastring'].split(',')
        except:
            out['message'] = 'Datastring missing'
            return JsonResponse(out)


        if len(data) < len(data_titles):
            out['message'] = 'Data string is too short - check whether any values are missing. Expected format is: controller_name,timestamp,temperature,rh,ec,ph'
            return JsonResponse(out)

        if not Controller.objects.filter(name=data[0]).exists():
            out['message'] = f'The controller {data[0]} does not exist'
            return JsonResponse(out)

        controller = Controller.objects.get(name=data[0])
        timestamp = datetime.datetime.fromtimestamp(int(data[1]))

        # check if all data is in the correct format before inserting anything
        for i in range(2, len(data_titles)):
            try:
                float(data[i])
            except ValueError:
                out['message'] = 'One of the values is not a float - check datastring format'
                return JsonResponse(out)
            except:
                out['message']  = 'Unknown error at data validation step - check format of datastring'
                return JsonResponse(out)

        for i in range(2, len(data_titles)):    # start at 2 to skip timestamp and controller name
            if data[i] != None and data[i].lower() != 'none':
                data_type = data_titles[i]
                value = float(data[i])
                DataEntry.objects.create(data_type=data_type, value = value, timestamp = timestamp, controller=controller)
        
        out['result'] = 'success'
    else:
        out['message'] = 'This endpoint can only handle POST requests'

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

            print(f'Added new controller: name={controller.name}, id={controller.id}')

    response = JsonResponse(out)
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Headers'] = 'Content-Type'

    return response

@csrf_exempt 
def get_available_controllers(request):
    out = {'result':'failure'}

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
    controller_id = int(request.GET.get('controller'))
    start = datetime.datetime.fromtimestamp(int(request.GET.get('start')))
    end = datetime.datetime.fromtimestamp(int(request.GET.get('end')))

    print(f'-------- Parameters --------\ndata type: {data_type}, start: {start}, end: {end}, controller: {controller_id}\n-------- End Parameters --------')

    if Controller.objects.filter(id=controller_id).exists() == False:
        out['results'] = 'This controller does not exist'
        return JsonResponse(out)

    controller = Controller.objects.get(id=controller_id)           

    res = DataEntry.objects.filter(data_type = data_type, timestamp__range=[start, end], controller = controller)

    response = HttpResponse(
        content_type='text/csv', 
    )

    response['Content-Disposition'] = 'attachment; filename="data.csv"'

    writer = csv.writer(response)

    writer.writerow(['Type', 'temp'])
    writer.writerow(['Controller_id', 1])
    writer.writerow(['controller_name', 'temp_name'])
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
        # controller_name = (request.GET.get('controller'))
        controller_id = request.GET.get('id')
        print(f'-------- Input --------')
        print(f'Request type - GET\nSearching for controller {controller_id}')
        print('-------- End Input --------')
        if Controller.objects.filter(id=controller_id).exists():
            controller = Controller.objects.get(id = controller_id)
            out['controller'] = controller.name
            out['devices'] = []

            if Device.objects.filter(controller = controller).exists():
                out['status'] = 'success'
                all_devices = (Device.objects.filter(controller=controller).all())
                for x in all_devices:
                    out['devices'].append({'name': x.name, 'target': x.target})

            else: 
                out['message'] = 'This controller has no devices'
        else: 
            out['message'] = 'This controller does not exist'
    
    elif request.method == "POST":  #TODO more consistent handling of ID versus name to access controllers
        # controller_name = request.POST['controller']
        print('abcde')
        print(request.POST)
        target = request.POST['target']
        controller_id = request.POST['id']
        name=request.POST['name']
        print(f'target: {target}, id: {controller_id}, name: {name}')

        if Controller.objects.filter(id=controller_id).exists():
            controller = Controller.objects.get(id=controller_id)
            if Device.objects.filter(controller=controller).exists():
                device = Device.objects.get(controller=controller, name=request.POST['name'])
                print(f'device is : {device.target}')
                device.target = target
                device.save()

                out['message'] = 'change applied'
                out['status'] = 'success'

            else:
                out['message'] = 'This controller does not have this device type'

        else:
            out['message'] = 'This controller does not exist'

    print(f'-------- Output --------')
    pprint.pprint(out)
    print(f'-------- End Output --------')

    response = JsonResponse(out)
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Headers'] = 'Content-Type'

    return response 

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

        controller = Controller.objects.filter(id = controller_id).first()
        # if controller does not exist, return error message
        if controller == None:
            out['message'] = 'Controller does not exist'
            return JsonResponse(out)

        # create a new device and save it
        device = Device.objects.filter(controller = controller, name=device_name).first()

        if device == None:
            Device.objects.create(controller=controller, name=device_name, target = target)
            out['message'] = 'success'
            return JsonResponse(out)

        # if device with same name and controller exists, inform client
        else:
            out['message'] = 'This device already exists'


    return JsonResponse(out)


def home(request):
    out = {'test': 'answer'}

    return render(request, 'app/home.html')
