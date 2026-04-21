import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import RegistroAcceso

@csrf_exempt
def registrar_click(request):

    if request.method == "POST":
        try:
            data = json.loads(request.body)

            RegistroAcceso.objects.create(
                email=data.get("email"),
                panel=data.get("panel"),
                tipo="acceso"
            )

            return JsonResponse({"status": "ok"})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Método no permitido"}, status=405)
