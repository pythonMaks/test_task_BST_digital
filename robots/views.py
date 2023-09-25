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
            
            
            if not model or len(model) != 2:
                return JsonResponse({"error": "Invalid model"}, status=400)
            if not version or len(version) != 2:
                return JsonResponse({"error": "Invalid version"}, status=400)
            if not created_str:
                return JsonResponse({"error": "Invalid created"}, status=400)
            
            try:
                created = datetime.strptime(created_str, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                return JsonResponse({"error": "Invalid date format"}, status=400)

            serial = f"{model}-{version}"
            
            Robot.objects.create(serial=serial, model=model, version=version, created=created)
            
            return JsonResponse({"success": True}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
