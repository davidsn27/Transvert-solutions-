from django.db import models
import uuid

class Envio(models.Model):
    numero_guia = models.CharField(max_length=20, unique=True)
    remitente_nombre = models.CharField(max_length=255)
    remitente_telefono = models.CharField(max_length=50)
    remitente_email = models.CharField(max_length=255, blank=True, null=True)

    destinatario_nombre = models.CharField(max_length=255)
    destinatario_telefono = models.CharField(max_length=50)
    destinatario_email = models.CharField(max_length=255, blank=True, null=True)

    tipo_envio = models.CharField(max_length=50)
    peso = models.FloatField()
    dimensiones = models.CharField(max_length=255, blank=True, null=True)

    origen = models.CharField(max_length=255)
    direccion_origen = models.CharField(max_length=255)

    destino = models.CharField(max_length=255)
    direccion_destino = models.CharField(max_length=255)

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.numero_guia
    