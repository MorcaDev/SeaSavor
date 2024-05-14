from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_503_SERVICE_UNAVAILABLE
# Create your views here.

@api_view(["GET"])
def home(request):

    try:
        return render(request,'home.html')
    
    except:
        return Response({
            "message"   :"error" , 
            "error"     :"Error en Servidores, intentar más tarde"}, 
            status=HTTP_503_SERVICE_UNAVAILABLE
        )