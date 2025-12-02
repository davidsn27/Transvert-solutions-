# core/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Envio, TrazaEnvio

@receiver(post_save, sender=TrazaEnvio)
def notificar_cambio_estado(sender, instance, created, **kwargs):
    """Envía notificaciones por email al actualizar el estado de un envío."""
    # Solo se notifica si es una traza nueva y el estado no es "Creado"
    if created and instance.estado_nuevo != 'Creado':
        envio = instance.envio
        
        # 1. Definir Contenido
        asunto = f"Actualización de Envío G- {envio.numero_guia}: {instance.estado_nuevo}"
        mensaje = (
            f"Estimado cliente,\n\nEl estado de su envío {envio.numero_guia} ha sido actualizado.\n"
            f"Nuevo estado: {instance.estado_nuevo}\nUbicación: {instance.ubicacion}\n"
            f"Detalle: {instance.descripcion}\n\n"
            f"Puede seguir su envío en: http://{settings.DEFAULT_DOMAIN}/seguimiento/?numero_guia={envio.numero_guia}"
        )
        
        # 2. Definir Destinatarios
        destinatarios = []
        if envio.remitente_email:
            destinatarios.append(envio.remitente_email)
        # Añade al destinatario solo si no es el mismo que el remitente
        if envio.destinatario_email and envio.destinatario_email not in destinatarios:
            destinatarios.append(envio.destinatario_email)
            
        # 3. Enviar (Requiere configuración en settings.py)
        if destinatarios:
            try:
                send_mail(
                    subject=asunto,
                    message=mensaje,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=destinatarios,
                    fail_silently=False,
                )
            except Exception as e:
                # Esto es útil para debug en la consola de Django
                print(f"Error al enviar correo para la guía {envio.numero_guia}: {e}")

