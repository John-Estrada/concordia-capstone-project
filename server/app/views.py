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

    # arduino uses this to send data to the server
    if request.method == 'POST':
        print(request.POST)
        server_time = datetime.datetime.now()
        data_type = request.POST['sensor']
        value = float(request.POST['value'])
        controller_name = request.POST['controller'] #name

        controller = Controller.objects.get(name=controller_name)

        print(f"Controller found: id: {controller.id}, name: {controller.name}")

        if controller == None:
            out['result'] = 'This controller does not exist'
            return JsonResponse(out)
        

        print(f'type: {data_type}, value: {value}, timestamp: {server_time}, controller: {controller_name}')


        x = DataEntry.objects.create(data_type = data_type, value=value, timestamp=server_time, controller = controller)
        x.save()

        out['status'] = 'success'

    # client uses this to get data for the user
    elif request.method == 'GET':
        out['results'] = []

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

@csrf_exempt
def add_controller(request):
    out = {'result': 'failure'}

    if request.method == 'POST':
        name = request.POST['name']

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
        print(request.POST)
        controller_id = request.POST['id']

        if Controller.objects.filter(id=controller_id).exists():
            controller = Controller.objects.get(id=controller_id)
            if Device.objects.filter(controller=controller).exists():
                device = Device.objects.filter(controller=controller, name=request.POST['name']).first()
                device.target = request.POST['target']
                device.save()

                out['message'] = 'change applied'

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

def home(request):
    out = {'test': 'answer'}

    return render(request, 'app/home.html')