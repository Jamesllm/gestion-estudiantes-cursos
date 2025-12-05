from config.template_config import get_template
from models.estadisticas import Estadisticas
from models.matricula import Matricula



def admin_dashboard(user):
    totales = Estadisticas.get_totales()
    cursos_populares = Estadisticas.get_cursos_populares()
    matriculas_recientes = Matricula.get_all()[:10]

    template = get_template("dashboard/admin.html")
    return template.render(
        user=user,
        totales=totales,
        cursos_populares=cursos_populares,
        matriculas_recientes=matriculas_recientes,
    )


def estudiante_dashboard(user):
    stats = Estadisticas.get_estudiante_stats(user["estudiante_id"])

    with __import__("config.database").database.get_db_cursor() as cursor:
        cursor.execute(
            """
            SELECT m.id, m.fecha_matricula, m.estado,
                   c.codigo, c.nombre, c.creditos, c.descripcion
            FROM matriculas m
            INNER JOIN cursos c ON m.curso_id = c.id
            WHERE m.estudiante_id = %s
            ORDER BY m.created_at DESC
        """,
            (user["estudiante_id"],),
        )
        mis_cursos = cursor.fetchall()

    template = get_template("dashboard/estudiante.html")
    return template.render(user=user, stats=stats, mis_cursos=mis_cursos)
