# core/apps.py
from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        # <<<< ESTA LÍNEA CONECTA EL ARCHIVO signals.py AL INICIAR DJANGO
        import core.signals 
