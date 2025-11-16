from django.db import models

class Envio(models.Model):
    numero_guia = models.CharField(max_length=255)
    cliente = models.CharField(max_length=255)
    descripcion = models.TextField()
    estado = models.CharField(max_length=255)
    direccion_origen = models.CharField(max_length=255, blank=True, null=True)
    direccion_destino = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.numero_guia