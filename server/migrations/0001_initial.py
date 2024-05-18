# Generated by Django 5.0.6 on 2024-05-18 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LibroRelamacion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('reclamante_nombre', models.CharField(max_length=50)),
                ('reclamante_domicilio', models.CharField(max_length=50)),
                ('reclamante_tipo_documento', models.CharField(choices=[('dni', 'DNI'), ('pasaporte', 'PASAPORTE')], max_length=9)),
                ('reclamante_numero_documento', models.CharField(max_length=12)),
                ('reclamante_correo', models.EmailField(max_length=50)),
                ('reclamante_telefono_celular', models.CharField(max_length=9)),
                ('reclamante_menor_edad', models.CharField(choices=[('menor', 'MENOR'), ('mayor', 'MAYOR')], max_length=5)),
                ('apoderado_nombre', models.CharField(blank=True, max_length=50, null=True)),
                ('apoderado_domicilio', models.CharField(blank=True, max_length=50, null=True)),
                ('apoderado_correo', models.EmailField(blank=True, max_length=50, null=True)),
                ('apoderado_telefono_celular', models.CharField(blank=True, max_length=9, null=True)),
                ('bien_tipo', models.CharField(choices=[('producto', 'PRODUCTO'), ('servicio', 'SERVICIO')], max_length=8)),
                ('bien_monto', models.CharField(max_length=7)),
                ('bien_descripcion', models.TextField(max_length=255)),
                ('reclamo_tipo', models.CharField(choices=[('reclamo', 'RECLAMO'), ('queja', 'QUEJA')], max_length=7)),
                ('reclamo_pedido', models.TextField(max_length=100)),
                ('reclamo_descripcion', models.TextField(max_length=255)),
                ('reclamo_fecha', models.DateField()),
                ('reclamo_pdf', models.FileField(blank=True, null=True, upload_to='complaints/')),
                ('solucion_pdf', models.FileField(blank=True, null=True, upload_to='answers/')),
            ],
            options={
                'db_table': 'LibroRelamacion',
            },
        ),
    ]