from django.http import JsonResponse

def home(request):
    return JsonResponse({
        "status": "success",
        "message": "API is running 🚀 - version 1"
    })
