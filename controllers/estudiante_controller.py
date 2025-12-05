from config.template_config import get_template
from urllib.parse import parse_qs
from models.estudiante import Estudiante
import json



def index(user=None, request_path="/estudiantes"):
    estudiantes = Estudiante.get_all()
    for est in estudiantes:
        est["total_cursos"] = Estudiante.count_matriculas(est["id"])
    template = get_template("estudiante/index.html")
    return template.render(estudiantes=estudiantes, user=user, request_path=request_path)


def create_form(user=None, request_path="/estudiantes/create"):
    template = get_template("estudiante/create.html")
    return template.render(action="create", estudiante=None, user=user, request_path=request_path)


def edit_form(estudiante_id, user=None, request_path=None):
    estudiante = Estudiante.get_by_id(estudiante_id)
    if not estudiante:
        return index(user, request_path or "/estudiantes")
    template = get_template("estudiante/create.html")
    return template.render(action="edit", estudiante=estudiante, user=user, request_path=request_path or f"/estudiantes/{estudiante_id}/edit")


def create(environ, user=None):
    try:
        content_length = int(environ.get("CONTENT_LENGTH", 0))
    except ValueError:
        content_length = 0

    post_data = environ["wsgi.input"].read(content_length).decode("utf-8")
    fields = parse_qs(post_data)

    nombre = fields.get("nombre", [""])[0].strip()
    apellido = fields.get("apellido", [""])[0].strip()
    email = fields.get("email", [""])[0].strip()
    fecha_nacimiento = fields.get("fecha_nacimiento", [""])[0]

    if nombre and apellido and email and fecha_nacimiento:
        Estudiante.create(nombre, apellido, email, fecha_nacimiento)

    return index(user, "/estudiantes")


def update(environ, estudiante_id, user=None):
    try:
        content_length = int(environ.get("CONTENT_LENGTH", 0))
    except ValueError:
        content_length = 0

    post_data = environ["wsgi.input"].read(content_length).decode("utf-8")
    fields = parse_qs(post_data)

    nombre = fields.get("nombre", [""])[0].strip()
    apellido = fields.get("apellido", [""])[0].strip()
    email = fields.get("email", [""])[0].strip()
    fecha_nacimiento = fields.get("fecha_nacimiento", [""])[0]

    if nombre and apellido and email and fecha_nacimiento:
        Estudiante.update(estudiante_id, nombre, apellido, email, fecha_nacimiento)

    return index(user, "/estudiantes")


def delete(estudiante_id, user=None):
    Estudiante.delete(estudiante_id)
    return index(user, "/estudiantes")
