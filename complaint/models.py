from django.db import models

# Create your models here.
class LibroRelamacion(models.Model):

    # del formato
    id                             = models.AutoField(primary_key=True, blank=False, null=False)

    # del reclamante
    reclamante_nombre              = models.CharField(max_length=50, blank=False, null=False)
    reclamante_domicilio           = models.CharField(max_length=50, blank=False, null=False)
    reclamante_tipo_documento      = models.CharField(max_length=9, blank=False, null=False, choices=[
        ("dni","DNI"),
        ("pasaporte","PASAPORTE"),
    ])
    reclamante_numero_documento    = models.CharField(max_length=12, blank=False, null=False) 
    reclamante_correo              = models.EmailField(max_length=50, blank=False, null=False) 
    reclamante_telefono_celular    = models.CharField(max_length=9, blank=False, null=False) 
    reclamante_menor_edad          = models.CharField(max_length=5, blank=False, null=False, choices=[
        ("menor","MENOR"),
        ("mayor","MAYOR"),
    ]) 

    # del apoderado
    apoderado_nombre              = models.CharField(max_length=50,blank=True,null=True) 
    apoderado_domicilio           = models.CharField(max_length=50,blank=True,null=True) 
    apoderado_correo              = models.EmailField(max_length=50,blank=True,null=True) 
    apoderado_telefono_celular    = models.CharField(max_length=9, blank=True, null=True)  
    
    # del bien contratado
    bien_tipo           = models.CharField(max_length=8, blank=False, null=False,choices=[
        ("producto","PRODUCTO"),
        ("servicio","SERVICIO"),
    ])
    bien_monto          = models.CharField(max_length=7, blank=False, null=False)   
    bien_descripcion    = models.TextField(max_length=255,blank=False, null=False) 
    
    # del reclamo
    reclamo_tipo        = models.CharField(max_length=7, blank=False, null=False, choices=[
        ("reclamo","RECLAMO"),
        ("queja","QUEJA"),
    ])
    reclamo_descripcion = models.TextField(max_length=255,blank=False, null=False)
    reclamo_pedido      = models.TextField(max_length=255,blank=False, null=False)
    reclamo_fecha       = models.DateField(blank=False, null=False)

    # del seguimiento
    reclamo_pdf         = models.FileField(upload_to="reclamos/", blank=False, null=False)
    solucion_pdf        = models.FileField(upload_to="soluciones/", blank=True, null=True)

    class Meta:
        db_table = "LibroRelamacion"

    def  __str__(self):
        return f'n°{self.id} ,  {self.reclamante_nombre},  {self.reclamo_fecha}'