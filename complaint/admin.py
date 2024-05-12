from django.contrib import admin
from .models import LibroRelamacion

# Register your models here.
class DisplayLibroRelamacio(admin.ModelAdmin):
    search_fields  = ["id","reclamante_nombre"]
    date_hierarchy = "reclamo_fecha"


admin.site.register(LibroRelamacion, DisplayLibroRelamacio)