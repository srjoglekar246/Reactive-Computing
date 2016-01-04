from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from reactive_compute.tasks import compute_nodes


@csrf_exempt
def input_values(request):
    #Get JSON-ed values dictionary
    value_dict = eval(request.GET.get('input'))
    #Make Celery call
    compute_nodes.delay(value_dict)

    return HttpResponse("OK")
