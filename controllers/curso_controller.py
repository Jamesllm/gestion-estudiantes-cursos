from config.template_config import get_template
from urllib.parse import parse_qs
from models.curso import Curso



def index(user=None, request_path="/cursos"):
    cursos = Curso.get_all()
    for curso in cursos:
        curso["total_estudiantes"] = Curso.count_matriculas(curso["id"])
    template = get_template("curso/index.html")
    return template.render(cursos=cursos, user=user, request_path=request_path)


def create_form(user=None, request_path="/cursos/create"):
    template = get_template("curso/create.html")
    return template.render(action="create", curso=None, user=user, request_path=request_path)


def edit_form(curso_id, user=None, request_path=None):
    curso = Curso.get_by_id(curso_id)
    if not curso:
        return index(user, request_path or "/cursos")
    template = get_template("curso/create.html")
    return template.render(action="edit", curso=curso, user=user, request_path=request_path or f"/cursos/{curso_id}/edit")


def create(environ, user=None):
    try:
        content_length = int(environ.get("CONTENT_LENGTH", 0))
    except ValueError:
        content_length = 0

    post_data = environ["wsgi.input"].read(content_length).decode("utf-8")
    fields = parse_qs(post_data)

    codigo = fields.get("codigo", [""])[0].strip()
    nombre = fields.get("nombre", [""])[0].strip()
    descripcion = fields.get("descripcion", [""])[0].strip()
    creditos = fields.get("creditos", ["0"])[0]

    if codigo and nombre:
        Curso.create(codigo, nombre, descripcion, int(creditos))

    return index(user, "/cursos")


def update(environ, curso_id, user=None):
    try:
        content_length = int(environ.get("CONTENT_LENGTH", 0))
    except ValueError:
        content_length = 0

    post_data = environ["wsgi.input"].read(content_length).decode("utf-8")
    fields = parse_qs(post_data)

    codigo = fields.get("codigo", [""])[0].strip()
    nombre = fields.get("nombre", [""])[0].strip()
    descripcion = fields.get("descripcion", [""])[0].strip()
    creditos = fields.get("creditos", ["0"])[0]

    if codigo and nombre:
        Curso.update(curso_id, codigo, nombre, descripcion, int(creditos))

    return index(user, "/cursos")


def delete(curso_id, user=None):
    Curso.delete(curso_id)
    return index(user, "/cursos")
