from config.template_config import get_template
from urllib.parse import parse_qs
from models.curso import Curso
from models.matricula import Matricula
from datetime import date


def explorar_cursos(user):
    cursos = Curso.get_all()
    
    # Obtener cursos ya matriculados
    with __import__('config.database').database.get_db_cursor() as cursor:
        cursor.execute("""
            SELECT curso_id FROM matriculas 
            WHERE estudiante_id = %s
        """, (user['estudiante_id'],))
        matriculados_ids = [row['curso_id'] for row in cursor.fetchall()]
    
    # Marcar cursos ya matriculados
    for curso in cursos:
        curso['matriculado'] = curso['id'] in matriculados_ids
        curso['total_estudiantes'] = Curso.count_matriculas(curso['id'])
    
    template = get_template('estudiante/explorar_cursos.html')
    return template.render(user=user, cursos_disponibles=cursos, request_path='/explorar-cursos')

def matricular_estudiante(environ, user):
    try:
        content_length = int(environ.get('CONTENT_LENGTH', 0))
    except ValueError:
        content_length = 0
    
    post_data = environ['wsgi.input'].read(content_length).decode('utf-8')
    fields = parse_qs(post_data)
    
    curso_id = fields.get('curso_id', [''])[0]
    fecha_matricula = fields.get('fecha_matricula', [str(date.today())])[0]
    
    if curso_id:
        # Verificar si ya está matriculado
        if not Matricula.exists(user['estudiante_id'], int(curso_id)):
            Matricula.create(user['estudiante_id'], int(curso_id), fecha_matricula, 'activo')
    
    # Redirigir a mis cursos
    from controllers.dashboard_controller import estudiante_dashboard
    return estudiante_dashboard(user)

def mis_cursos(user):
    with __import__('config.database').database.get_db_cursor() as cursor:
        cursor.execute("""
            SELECT m.id, m.fecha_matricula, m.estado,
                   c.codigo, c.nombre, c.creditos, c.descripcion
            FROM matriculas m
            INNER JOIN cursos c ON m.curso_id = c.id
            WHERE m.estudiante_id = %s
            ORDER BY m.created_at DESC
        """, (user['estudiante_id'],))
        cursos = cursor.fetchall()
    
    template = get_template('estudiante/mis_cursos.html')
    return template.render(user=user, mis_cursos=cursos, request_path='/mis-cursos')