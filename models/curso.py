from config.database import get_db_cursor


class Curso:

    @staticmethod
    def get_all():
        with get_db_cursor() as cursor:
            cursor.execute(
                """
                SELECT id, codigo, nombre, descripcion, creditos, created_at 
                FROM cursos 
                ORDER BY created_at DESC
            """
            )
            return cursor.fetchall()

    @staticmethod
    def get_by_id(curso_id):
        with get_db_cursor() as cursor:
            cursor.execute(
                """
                SELECT id, codigo, nombre, descripcion, creditos, created_at 
                FROM cursos 
                WHERE id = %s
            """,
                (curso_id,),
            )
            return cursor.fetchone()

    @staticmethod
    def create(codigo, nombre, descripcion, creditos):
        with get_db_cursor(commit=True) as cursor:
            cursor.execute(
                """
                INSERT INTO cursos (codigo, nombre, descripcion, creditos) 
                VALUES (%s, %s, %s, %s)
            """,
                (codigo, nombre, descripcion, creditos),
            )
            return cursor.lastrowid

    @staticmethod
    def update(curso_id, codigo, nombre, descripcion, creditos):
        with get_db_cursor(commit=True) as cursor:
            cursor.execute(
                """
                UPDATE cursos 
                SET codigo = %s, nombre = %s, descripcion = %s, creditos = %s 
                WHERE id = %s
            """,
                (codigo, nombre, descripcion, creditos, curso_id),
            )
            return cursor.rowcount

    @staticmethod
    def delete(curso_id):
        with get_db_cursor(commit=True) as cursor:
            cursor.execute("DELETE FROM cursos WHERE id = %s", (curso_id,))
            return cursor.rowcount

    @staticmethod
    def count_matriculas(curso_id):
        with get_db_cursor() as cursor:
            cursor.execute(
                """
                SELECT COUNT(*) as total 
                FROM matriculas 
                WHERE curso_id = %s
            """,
                (curso_id,),
            )
            result = cursor.fetchone()
            return result["total"] if result else 0
