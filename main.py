"""
Archivo principal para iniciar la aplicación del Sistema de Gestión Académica
Ejecutar este archivo para iniciar la aplicación
"""

import sys
import os

# Ajustar la ruta para importar los módulos desde las carpetas
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from views.mainView import iniciar_app

if __name__ == "__main__":
    iniciar_app()

