from config.template_config import get_template
from urllib.parse import parse_qs
from models.matricula import Matricula
from models.estudiante import Estudiante
from models.curso import Curso



def index(user=None, request_path="/matriculas"):
    matriculas = Matricula.get_all()
    estudiantes = Estudiante.get_all()
    cursos = Curso.get_all()
    template = get_template("matricula/index.html")
    return template.render(
        matriculas=matriculas,
        estudiantes=estudiantes,
        cursos=cursos,
        action="create",
        matricula_edit=None,
        user=user,
        request_path=request_path,
    )


def edit_form(matricula_id, user=None, request_path=None):
    matricula = Matricula.get_by_id(matricula_id)
    matriculas = Matricula.get_all()
    estudiantes = Estudiante.get_all()
    cursos = Curso.get_all()
    template = get_template("matricula/index.html")
    return template.render(
        matriculas=matriculas,
        estudiantes=estudiantes,
        cursos=cursos,
        action="edit",
        matricula_edit=matricula,
        user=user,
        request_path=request_path or f"/matriculas/{matricula_id}/edit",
    )


def create(environ, user=None):
    try:
        content_length = int(environ.get("CONTENT_LENGTH", 0))
    except ValueError:
        content_length = 0

    post_data = environ["wsgi.input"].read(content_length).decode("utf-8")
    fields = parse_qs(post_data)

    estudiante_id = fields.get("estudiante_id", [""])[0]
    curso_id = fields.get("curso_id", [""])[0]
    fecha_matricula = fields.get("fecha_matricula", [""])[0]
    estado = fields.get("estado", ["activo"])[0]

    if estudiante_id and curso_id and fecha_matricula:
        if not Matricula.exists(int(estudiante_id), int(curso_id)):
            Matricula.create(int(estudiante_id), int(curso_id), fecha_matricula, estado)

    return index(user, "/matriculas")


def update(environ, matricula_id, user=None):
    try:
        content_length = int(environ.get("CONTENT_LENGTH", 0))
    except ValueError:
        content_length = 0

    post_data = environ["wsgi.input"].read(content_length).decode("utf-8")
    fields = parse_qs(post_data)

    estudiante_id = fields.get("estudiante_id", [""])[0]
    curso_id = fields.get("curso_id", [""])[0]
    fecha_matricula = fields.get("fecha_matricula", [""])[0]
    estado = fields.get("estado", ["activo"])[0]

    if estudiante_id and curso_id and fecha_matricula:
        Matricula.update(
            matricula_id, int(estudiante_id), int(curso_id), fecha_matricula, estado
        )

    return index(user, "/matriculas")


def delete(matricula_id, user=None):
    Matricula.delete(matricula_id)
    return index(user, "/matriculas")
