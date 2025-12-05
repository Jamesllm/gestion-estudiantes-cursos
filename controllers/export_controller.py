from models.estudiante import Estudiante
from models.curso import Curso
from models.matricula import Matricula
from utils.exporters import Exporters


def export_estudiantes_excel():
    estudiantes = Estudiante.get_all()
    return Exporters.export_estudiantes_excel(estudiantes)


def export_estudiantes_pdf():
    estudiantes = Estudiante.get_all()
    return Exporters.export_estudiantes_pdf(estudiantes)


def export_cursos_excel():
    cursos = Curso.get_all()
    return Exporters.export_cursos_excel(cursos)


def export_cursos_pdf():
    cursos = Curso.get_all()
    return Exporters.export_cursos_pdf(cursos)


def export_matriculas_excel():
    matriculas = Matricula.get_all()
    return Exporters.export_matriculas_excel(matriculas)
