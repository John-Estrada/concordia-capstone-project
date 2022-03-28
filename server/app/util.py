from django.http import JsonResponse
from .models import Controller

def validate_params_missing(expected_parameters, actual_parameters):
    out = {}
    missing = []
    for param in expected_parameters:
        if param not in actual_parameters:
            missing.append(param)

    if len(missing) > 0:
        out['message'] = 'parameters missing'
        out['missing_parameters'] = missing
    else:
        out['message'] = 'normal'

    return out

def get_controller_or_none(request):
    try:
        name = request.POST['controller']
    except:
        name = request.GET['controller']

    if not Controller.objects.filter(name=name).exists():
        return None 
        
    controller = Controller.objects.get(name=name)

    return controller