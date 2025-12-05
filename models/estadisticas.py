from config.database import get_db_cursor


class Estadisticas:

    @staticmethod
    def get_totales():
        with get_db_cursor() as cursor:
            cursor.execute("SELECT COUNT(*) as total FROM estudiantes")
            total_estudiantes = cursor.fetchone()["total"]

            cursor.execute("SELECT COUNT(*) as total FROM cursos")
            total_cursos = cursor.fetchone()["total"]

            cursor.execute(
                "SELECT COUNT(*) as total FROM matriculas WHERE estado = 'activo'"
            )
            total_matriculas = cursor.fetchone()["total"]

            cursor.execute(
                "SELECT SUM(c.creditos) as total FROM matriculas m INNER JOIN cursos c ON m.curso_id = c.id WHERE m.estado = 'activo'"
            )
            result = cursor.fetchone()
            total_creditos = result["total"] if result["total"] else 0

            return {
                "estudiantes": total_estudiantes,
                "cursos": total_cursos,
                "matriculas": total_matriculas,
                "creditos": total_creditos,
            }

    @staticmethod
    def get_cursos_populares(limit=5):
        with get_db_cursor() as cursor:
            cursor.execute(
                """
                SELECT c.nombre, c.codigo, COUNT(m.id) as total_matriculas
                FROM cursos c
                LEFT JOIN matriculas m ON c.id = m.curso_id
                GROUP BY c.id
                ORDER BY total_matriculas DESC
                LIMIT %s
            """,
                (limit,),
            )
            return cursor.fetchall()

    @staticmethod
    def get_matriculas_por_mes():
        with get_db_cursor() as cursor:
            cursor.execute(
                """
                SELECT 
                    DATE_FORMAT(fecha_matricula, '%Y-%m') as mes,
                    COUNT(*) as total
                FROM matriculas
                GROUP BY mes
                ORDER BY mes DESC
                LIMIT 12
            """
            )
            return cursor.fetchall()

    @staticmethod
    def get_estudiante_stats(estudiante_id):
        with get_db_cursor() as cursor:
            cursor.execute(
                """
                SELECT COUNT(*) as total_cursos,
                       SUM(c.creditos) as total_creditos
                FROM matriculas m
                INNER JOIN cursos c ON m.curso_id = c.id
                WHERE m.estudiante_id = %s AND m.estado = 'activo'
            """,
                (estudiante_id,),
            )
            return cursor.fetchone()
