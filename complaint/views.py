from django.shortcuts import render,redirect
from django.views.decorators.http import require_http_methods
from .oop import Formulario
from .models import LibroRelamacion

from django.http import HttpResponse
from datetime import date

# Create your views here.
@require_http_methods(["GET", "POST"])
def libro(request):

    # http request method
    method = request.method 

    # catch data from form
    if method == 'POST' :

        # catch data
        id         = LibroRelamacion.objects.order_by("-id")[0].id + 1
        formulario = Formulario(
            id,
            request.POST.get("reclamante_nombre"),
            request.POST.get("reclamante_domicilio"),
            request.POST.get("reclamante_tipo_documento"),
            request.POST.get("reclamante_numero_documento"),
            request.POST.get("reclamante_correo"),
            request.POST.get("reclamante_telefono_celular"),
            request.POST.get("reclamante_menor_edad"),
            request.POST.get("apoderado_nombre"),
            request.POST.get("apoderado_domicilio"),
            request.POST.get("apoderado_correo"),
            request.POST.get("apoderado_telefono_celular"),
            request.POST.get("bien_tipo"),
            request.POST.get("bien_monto"),
            request.POST.get("bien_descripcion"),
            request.POST.get("reclamo_tipo"),
            request.POST.get("reclamo_descripcion"),
            request.POST.get("reclamo_pedido"),
        )

        # no previous insert
        previous = LibroRelamacion.objects.filter(
            reclamante_numero_documento = formulario.reclamante_numero_documento,
            reclamo_fecha = date.today()
        )

        if previous.exists():
            return HttpResponse("<h1>ERROR REPITITION</h1>")   

        # apply filters
        if not formulario.apply_filters() :
            return HttpResponse("<h1>ERROR PDF</h1>")
        
        # create pdf
        if not formulario.create_pdf() :
            return HttpResponse("<h1>ERROR PDF</h1>")
        
        # create and save  instance
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

            return HttpResponse("<h1>ERROR INSTANCE</h1>")
        
        # send email
        if not formulario.send_email() :
            return HttpResponse("<h1>OBSERVATION EMAIL</h1>")

        # feedback 
        return  HttpResponse("<h1>GOOD FEEDBACK</h1>")
    
    # load form page
    return  render(request, 'book.html')

@require_http_methods("GET")
def feedback(request):

    return render(request, 'feedback.html',{})