from django.shortcuts import render
from django.views.decorators.http import require_http_methods 
from django.http import JsonResponse

# Create your views here.
@require_http_methods(["GET"])
def home(request):

    try:
        return render(request,'home.html')
    
    except:
        return JsonResponse(
            {"message":"Service Not Available"},
            safe=True,
            status=500)

@require_http_methods(["GET"])
def book(request):

    try:
        return render(request, 'book.html')
    
    except:
        return JsonResponse(
            {"message":"Service Not Available"},
            safe=True,
            status=500)