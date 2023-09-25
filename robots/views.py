from django.http import JsonResponse
#from django.views.decorators.csrf import csrf_exempt
from .models import Robot
import json
from datetime import datetime

#@csrf_exempt
def create_robot(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            model = data.get('model')
            version = data.get('version')
            created_str = data.get('created')
            
            
            if not (model and version and created_str):
                return JsonResponse({"error": "Invalid data"}, status=400)
            
            
            created = datetime.strptime(created_str, '%Y-%m-%d %H:%M:%S')            
            
            serial = f"{model}-{version}"
            
            Robot.objects.create(serial=serial, model=model, version=version, created=created)
            
            return JsonResponse({"success": True}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
