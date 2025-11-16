from django.db import models
from django.utils import timezone
import uuid

class Envio(models.Model):
    cliente = models.CharField(max_length=100)
    direccion_origen = models.CharField(max_length=255)
    direccion_destino = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    fecha_envio = models.DateTimeField(default=timezone.now)
    estado = models.CharField(max_length=50, default='Pendiente')
    numero_guia = models.CharField(max_length=20, unique=True, blank=True)

    def save(self, *args, **kwargs):
        # Generar número de guía si no existe
        if not self.numero_guia:
            codigo = str(uuid.uuid4())[:6].upper()
            fecha = timezone.now().strftime('%Y%m%d')
            self.numero_guia = f"TRV-{fecha}-{codigo}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.numero_guia} - {self.estado}"
