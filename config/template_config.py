"""
Configuración centralizada de Jinja2 con caché habilitado para mejor rendimiento
"""
from jinja2 import Environment, FileSystemLoader
import os

# Crear un único Environment de Jinja2 con caché habilitado
template_env = Environment(
    loader=FileSystemLoader("views"),
    auto_reload=False,  # Desactivar recarga automática en producción
    cache_size=400,     # Aumentar tamaño de caché (default: 400)
    bytecode_cache=None  # Puedes usar FileSystemBytecodeCache para mayor velocidad
)

# Si quieres caché de bytecode (aún más rápido), descomenta esto:
# from jinja2 import FileSystemBytecodeCache
# template_env.bytecode_cache = FileSystemBytecodeCache(
#     directory=os.path.join(os.path.dirname(__file__), '__pycache__', 'jinja2'),
#     pattern='__jinja2_%s.cache'
# )

def get_template(template_name):
    """
    Obtiene una plantilla del entorno de Jinja2 con caché
    """
    return template_env.get_template(template_name)
