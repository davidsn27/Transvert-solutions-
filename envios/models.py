from django.db import models
from django.contrib.auth.models import User
import uuid

class Envio(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('en_transito', 'En tránsito'),
        ('entregado', 'Entregado'),
    ]

    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    numero_guia = models.CharField(max_length=20, unique=True, editable=False)
    origen = models.CharField(max_length=100)
    destino = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.numero_guia:
            self.numero_guia = f"TRV-{uuid.uuid4().hex[:9].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.numero_guia} - {self.cliente.username}"

