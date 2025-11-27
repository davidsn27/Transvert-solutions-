from django.db import models
import uuid
from django.contrib.auth.models import User


class SoporteTicket(models.Model):
    PRIORIDAD_CHOICES = [
        ('Baja', 'Baja'),
        ('Media', 'Media'),
        ('Alta', 'Alta')
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    asunto = models.CharField(max_length=200)
    descripcion = models.TextField()
    correo = models.EmailField(max_length=255, blank=True, null=True)  # nuevo campo
    estado = models.CharField(max_length=20, default="ABIERTO")
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.asunto

class SoporteRespuesta(models.Model):
    ticket = models.ForeignKey(SoporteTicket, on_delete=models.CASCADE, related_name="respuestas")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Respuesta de {self.usuario.username} al ticket {self.ticket.id}"


class Envio(models.Model):
    numero_guia = models.CharField(max_length=20, unique=True)

    # Remitente
    remitente_nombre = models.CharField(max_length=100)
    remitente_telefono = models.CharField(max_length=20)
    remitente_email = models.EmailField(blank=True, null=True)

    # Destinatario
    destinatario_nombre = models.CharField(max_length=100)
    destinatario_telefono = models.CharField(max_length=20)
    destinatario_email = models.EmailField(blank=True, null=True)

    # Envío
    tipo_envio = models.CharField(max_length=20)
    peso = models.DecimalField(max_digits=10, decimal_places=2)
    dimensiones = models.CharField(max_length=100, blank=True, null=True)

    # Direcciones
    direccion_origen = models.CharField(max_length=200)
    direccion_destino = models.CharField(max_length=200)

    # Estado
    estado = models.CharField(max_length=20, default="Pendiente")

    fecha_creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.numero_guia



    