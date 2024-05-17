import json
from datetime import date

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods 
from django.views.decorators.csrf import csrf_exempt

from .oop import Formulario
from .models import LibroRelamacion

# Algorithms
def id_alogirhtm():

    query_id    = LibroRelamacion.objects.order_by("-id")
    new_id      = 1
    if query_id.exists() :
            new_id = query_id[0].id + 1

    return new_id

def post_algorithm(formulario):

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

    # pdf creation
    if not formulario.create_pdf() :
        return JsonResponse(
            {"message"  :"Service Not Available", 
             "error"    : formulario.errors},
            safe=True,
            status=503)
        
    # db insertion
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
        
    # send email
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

# Views
@require_http_methods(["POST"])
def form_api(request):

    # id value
    new_id      = id_alogirhtm()
    
    # query data
    formulario  = Formulario(
        id                          = new_id,
        reclamante_nombre           = request.POST.get("reclamante_nombre"),
        reclamante_domicilio        = request.POST.get("reclamante_domicilio"),
        reclamante_tipo_documento   = request.POST.get("reclamante_tipo_documento"),
        reclamante_numero_documento = request.POST.get("reclamante_numero_documento"),
        reclamante_correo           = request.POST.get("reclamante_correo"),
        reclamante_telefono_celular = request.POST.get("reclamante_telefono_celular"),
        reclamante_menor_edad       = request.POST.get("reclamante_menor_edad") or "mayor",
        apoderado_nombre            = request.POST.get("apoderado_nombre"),
        apoderado_domicilio         = request.POST.get("apoderado_domicilio"),
        apoderado_correo            = request.POST.get("apoderado_correo"),
        apoderado_telefono_celular  = request.POST.get("apoderado_telefono_celular"),
        bien_tipo                   = request.POST.get("bien_tipo"),
        bien_monto                  = request.POST.get("bien_monto"),
        bien_descripcion            = request.POST.get("bien_descripcion"),
        reclamo_tipo                = request.POST.get("reclamo_tipo"),
        reclamo_descripcion         = request.POST.get("reclamo_descripcion"),
        reclamo_pedido              = request.POST.get("reclamo_pedido"),
        reclamo_fecha               = str(date.today())
    )

    return post_algorithm(formulario)

@csrf_exempt
@require_http_methods(["POST"])
def rest_api(request):

    # json formater
    query_dict  = json.loads(request.body)

    # security level
    hash = "NZo5JECQEl"
    if query_dict.get("hash") == hash:

        # id value
        new_id      = id_alogirhtm()

        # quey data
        formulario  = Formulario(
            id                          = new_id,
            reclamante_nombre           = query_dict.get("reclamante_nombre"),
            reclamante_domicilio        = query_dict.get("reclamante_domicilio"),
            reclamante_tipo_documento   = query_dict.get("reclamante_tipo_documento"),
            reclamante_numero_documento = query_dict.get("reclamante_numero_documento"),
            reclamante_correo           = query_dict.get("reclamante_correo"),
            reclamante_telefono_celular = query_dict.get("reclamante_telefono_celular"),
            reclamante_menor_edad       = query_dict.get("reclamante_menor_edad"),
            apoderado_nombre            = query_dict.get("apoderado_nombre"),
            apoderado_domicilio         = query_dict.get("apoderado_domicilio"),
            apoderado_correo            = query_dict.get("apoderado_correo"),
            apoderado_telefono_celular  = query_dict.get("apoderado_telefono_celular"),
            bien_tipo                   = query_dict.get("bien_tipo"),
            bien_monto                  = query_dict.get("bien_monto"),
            bien_descripcion            = query_dict.get("bien_descripcion"),
            reclamo_tipo                = query_dict.get("reclamo_tipo"),
            reclamo_descripcion         = query_dict.get("reclamo_descripcion"),
            reclamo_pedido              = query_dict.get("reclamo_pedido"),
            reclamo_fecha               = str(date.today())
        )
        
        return post_algorithm(formulario)
    
    return JsonResponse(
        {"message":"Service Not Available",
        "error":"not security layer achieved"},
        safe=True,
        status=400) 