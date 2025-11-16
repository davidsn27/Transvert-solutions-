#!/usr/bin/env python
"""Script de línea de comandos para tareas administrativas de Django."""

import os
import sys

def main():
    """Punto de entrada principal para las tareas administrativas de Django."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "No se pudo importar Django. Asegúrate de que esté instalado "
            "y disponible en tu entorno de Python."
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
