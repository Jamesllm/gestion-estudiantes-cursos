from config.database import get_db_cursor


class Matricula:

    @staticmethod
    def get_all():
        with get_db_cursor() as cursor:
            cursor.execute(
                """
                SELECT 
                    m.id,
                    m.estudiante_id,
                    m.curso_id,
                    m.fecha_matricula,
                    m.estado,
                    e.nombre AS estudiante_nombre,
                    e.apellido AS estudiante_apellido,
                    c.codigo AS curso_codigo,
                    c.nombre AS curso_nombre,
                    c.creditos AS curso_creditos,
                    m.created_at
                FROM matriculas m
                INNER JOIN estudiantes e ON m.estudiante_id = e.id
                INNER JOIN cursos c ON m.curso_id = c.id
                ORDER BY m.created_at DESC
            """
            )
            return cursor.fetchall()

    @staticmethod
    def get_by_id(matricula_id):
        with get_db_cursor() as cursor:
            cursor.execute(
                """
                SELECT 
                    m.id,
                    m.estudiante_id,
                    m.curso_id,
                    m.fecha_matricula,
                    m.estado,
                    e.nombre AS estudiante_nombre,
                    e.apellido AS estudiante_apellido,
                    c.codigo AS curso_codigo,
                    c.nombre AS curso_nombre,
                    m.created_at
                FROM matriculas m
                INNER JOIN estudiantes e ON m.estudiante_id = e.id
                INNER JOIN cursos c ON m.curso_id = c.id
                WHERE m.id = %s
            """,
                (matricula_id,),
            )
            return cursor.fetchone()

    @staticmethod
    def create(estudiante_id, curso_id, fecha_matricula, estado="activo"):
        with get_db_cursor(commit=True) as cursor:
            cursor.execute(
                """
                INSERT INTO matriculas (estudiante_id, curso_id, fecha_matricula, estado) 
                VALUES (%s, %s, %s, %s)
            """,
                (estudiante_id, curso_id, fecha_matricula, estado),
            )
            return cursor.lastrowid

    @staticmethod
    def update(matricula_id, estudiante_id, curso_id, fecha_matricula, estado):
        with get_db_cursor(commit=True) as cursor:
            cursor.execute(
                """
                UPDATE matriculas 
                SET estudiante_id = %s, curso_id = %s, fecha_matricula = %s, estado = %s 
                WHERE id = %s
            """,
                (estudiante_id, curso_id, fecha_matricula, estado, matricula_id),
            )
            return cursor.rowcount

    @staticmethod
    def delete(matricula_id):
        with get_db_cursor(commit=True) as cursor:
            cursor.execute("DELETE FROM matriculas WHERE id = %s", (matricula_id,))
            return cursor.rowcount

    @staticmethod
    def exists(estudiante_id, curso_id):
        with get_db_cursor() as cursor:
            cursor.execute(
                """
                SELECT COUNT(*) as total 
                FROM matriculas 
                WHERE estudiante_id = %s AND curso_id = %s
            """,
                (estudiante_id, curso_id),
            )
            result = cursor.fetchone()
            return result["total"] > 0
