from django.shortcuts import render
from django.http import JsonResponse
from .oop import Formulario
from .models import LibroRelamacion
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK,HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_503_SERVICE_UNAVAILABLE

# Create your views here.
@api_view(["GET", "POST"])
def libro(request):

    if request.method == 'GET':
        return  render(request, 'book.html')

    if request.method  == 'POST':

        # request
        formulario = Formulario(
            id = LibroRelamacion.objects.order_by("-id")[0].id + 1,
            reclamante_nombre = request.data.get("reclamante_nombre",None),
            reclamante_domicilio = request.data.get("reclamante_domicilio",None),
            reclamante_tipo_documento = request.data.get("reclamante_tipo_documento",None),
            reclamante_numero_documento = request.data.get("reclamante_numero_documento",None),
            reclamante_correo = request.data.get("reclamante_correo",None),
            reclamante_telefono_celular = request.data.get("reclamante_telefono_celular",None),
            reclamante_menor_edad =request.data.get("reclamante_menor_edad","mayor"),
            apoderado_nombre = request.data.get("apoderado_nombre",None),
            apoderado_domicilio = request.data.get("apoderado_domicilio",None),
            apoderado_correo = request.data.get("apoderado_correo",None),
            apoderado_telefono_celular = request.data.get("apoderado_telefono_celular",None),
            bien_tipo = request.data.get("bien_tipo",None),
            bien_monto = request.data.get("bien_monto",None),
            bien_descripcion = request.data.get("bien_descripcion",None),
            reclamo_tipo  = request.data.get("reclamo_tipo",None),
            reclamo_descripcion = request.data.get("reclamo_descripcion",None),
            reclamo_pedido = request.data.get("reclamo_pedido",None),
        )

        # validations
        if not formulario.apply_validations() :
            return Response({
                "message"   :"error",
                "error"     :formulario.errors}, 
                status=HTTP_400_BAD_REQUEST
            )

        # no repetition
        previous = LibroRelamacion.objects.filter(
            reclamante_numero_documento = formulario.reclamante_numero_documento,
            reclamante_correo = formulario.reclamante_correo,
            reclamo_fecha = formulario.reclamo_fecha
        )
        if previous.exists():
            return Response({   
                "message"   :"error",
                "error"     :"Tiene un registro existente hace menos de 24hr"}, 
                status=HTTP_400_BAD_REQUEST
            )   

        # pdf 
        if not formulario.create_pdf() :
            return Response({
                "message"   :"error",
                "error"     :formulario.errors}, 
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        # db
        try :
            new_instance = LibroRelamacion(
                id = formulario.id,
                reclamante_nombre = formulario.reclamante_nombre,
                reclamante_domicilio = formulario.reclamante_domicilio,
                reclamante_tipo_documento = formulario.reclamante_tipo_documento,
                reclamante_numero_documento = formulario.reclamante_numero_documento,
                reclamante_correo = formulario.reclamante_correo,
                reclamante_telefono_celular = formulario.reclamante_telefono_celular,
                reclamante_menor_edad = formulario.reclamante_menor_edad,
                apoderado_nombre = formulario.apoderado_nombre,
                apoderado_domicilio = formulario.apoderado_domicilio,
                apoderado_correo = formulario.apoderado_correo,
                apoderado_telefono_celular = formulario.apoderado_telefono_celular,
                bien_tipo = formulario.bien_tipo,
                bien_monto = formulario.bien_monto,
                bien_descripcion = formulario.bien_descripcion,
                reclamo_tipo = formulario.reclamo_tipo,
                reclamo_descripcion = formulario.reclamo_descripcion,
                reclamo_pedido = formulario.reclamo_pedido,
                reclamo_fecha=formulario.reclamo_fecha,
                reclamo_pdf = formulario.reclamo_pdf,
            )

            new_instance.save()

        except:

            return Response({
                "message"   :"error",
                "error"     :formulario.errors},
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        # email
        if not formulario.send_email() :
            return Response({
                "message"   :"error",
                "error"     :formulario.errors}, 
                status=HTTP_503_SERVICE_UNAVAILABLE
            )

        # feedback 
        return  Response({"message":"success"},status = HTTP_200_OK)
    
