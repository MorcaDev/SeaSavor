import json
from datetime import date

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods 
from django.views.decorators.csrf import csrf_exempt

from .oop import Formulario
from .models import LibroRelamacion

# Create your views here.
@csrf_exempt
@require_http_methods(["GET", "POST"])
def book(request):

    if request.method == 'GET':
        return  render(request, 'book.html')

    if request.method  == 'POST':

        # request data
        query_dict = json.loads(request.body)
        formulario = Formulario(
            id                          = LibroRelamacion.objects.order_by("-id")[0].id + 1,
            reclamante_nombre           = query_dict["reclamante_nombre"],
            reclamante_domicilio        = query_dict["reclamante_domicilio"],
            reclamante_tipo_documento   = query_dict["reclamante_tipo_documento"],
            reclamante_numero_documento = query_dict["reclamante_numero_documento"],
            reclamante_correo           = query_dict["reclamante_correo"],
            reclamante_telefono_celular = query_dict["reclamante_telefono_celular"],
            reclamante_menor_edad       = query_dict["reclamante_menor_edad"],
            apoderado_nombre            = query_dict["apoderado_nombre"],
            apoderado_domicilio         = query_dict["apoderado_domicilio"],
            apoderado_correo            = query_dict["apoderado_correo"],
            apoderado_telefono_celular  = query_dict["apoderado_telefono_celular"],
            bien_tipo                   = query_dict["bien_tipo"],
            bien_monto                  = query_dict["bien_monto"],
            bien_descripcion            = query_dict["bien_descripcion"],
            reclamo_tipo                = query_dict["reclamo_tipo"],
            reclamo_descripcion         = query_dict["reclamo_descripcion"],
            reclamo_pedido              = query_dict["reclamo_pedido"],
            reclamo_fecha               = str(date.today())
        )

        # data format
        if not formulario.apply_validations() :
            return JsonResponse(
                {"message"  :"Service Not Available", 
                 "error"    : formulario.errors},
                safe=True,
                status=400)

        # no repetition
        previous = LibroRelamacion.objects.filter(
            reclamante_numero_documento = formulario.reclamante_numero_documento,
            reclamo_fecha = formulario.reclamo_fecha
        )
        if previous.exists():
            return JsonResponse(
                {"message"  :"Service Not Available", 
                 "error"    : "The Document has been used in the last 24 hrs"},
                safe=True,
                status=400)

        # db
        try :
            new_instance = LibroRelamacion(
                id                          = formulario.id,
                reclamante_nombre           = formulario.reclamante_nombre,
                reclamante_domicilio        = formulario.reclamante_domicilio,
                reclamante_tipo_documento   = formulario.reclamante_tipo_documento,
                reclamante_numero_documento = formulario.reclamante_numero_documento,
                reclamante_correo           = formulario.reclamante_correo,
                reclamante_telefono_celular = formulario.reclamante_telefono_celular,
                reclamante_menor_edad       = formulario.reclamante_menor_edad,
                apoderado_nombre            = formulario.apoderado_nombre,
                apoderado_domicilio         = formulario.apoderado_domicilio,
                apoderado_correo            = formulario.apoderado_correo,
                apoderado_telefono_celular  = formulario.apoderado_telefono_celular,
                bien_tipo                   = formulario.bien_tipo,
                bien_monto                  = formulario.bien_monto,
                bien_descripcion            = formulario.bien_descripcion,
                reclamo_tipo                = formulario.reclamo_tipo,
                reclamo_descripcion         = formulario.reclamo_descripcion,
                reclamo_pedido              = formulario.reclamo_pedido,
                reclamo_fecha               = formulario.reclamo_fecha,
                reclamo_pdf                 = formulario.reclamo_pdf,
            )
            new_instance.save()

        except:
            return JsonResponse(
                {"message"  :"Service Not Available", 
                 "error"    : formulario.errors},
                safe=True,
                status=503)
        
        # pdf 
        if not formulario.create_pdf() :
            return JsonResponse(
                {"message"  :"Service Not Available", 
                 "error"    : formulario.errors},
                safe=True,
                status=503)
        
        # email
        if not formulario.send_email() :
            return JsonResponse(
                {"message"  :"Service Not Available", 
                 "error"    : formulario.errors},
                safe=True,
                status=503)

        # feedback 
        return JsonResponse(
            {"message"  :"success"},
            safe=True,
            status=200)  
    
