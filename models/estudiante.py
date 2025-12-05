from config.database import get_db_cursor


class Estudiante:

    @staticmethod
    def get_all():
        with get_db_cursor() as cursor:
            cursor.execute(
                """
                SELECT id, nombre, apellido, email, fecha_nacimiento, created_at 
                FROM estudiantes 
                ORDER BY created_at DESC
            """
            )
            return cursor.fetchall()

    @staticmethod
    def get_by_id(estudiante_id):
        with get_db_cursor() as cursor:
            cursor.execute(
                """
                SELECT id, nombre, apellido, email, fecha_nacimiento, created_at 
                FROM estudiantes 
                WHERE id = %s
            """,
                (estudiante_id,),
            )
            return cursor.fetchone()

    @staticmethod
    def create(nombre, apellido, email, fecha_nacimiento):
        with get_db_cursor(commit=True) as cursor:
            cursor.execute(
                """
                INSERT INTO estudiantes (nombre, apellido, email, fecha_nacimiento) 
                VALUES (%s, %s, %s, %s)
            """,
                (nombre, apellido, email, fecha_nacimiento),
            )
            return cursor.lastrowid

    @staticmethod
    def update(estudiante_id, nombre, apellido, email, fecha_nacimiento):
        with get_db_cursor(commit=True) as cursor:
            cursor.execute(
                """
                UPDATE estudiantes 
                SET nombre = %s, apellido = %s, email = %s, fecha_nacimiento = %s 
                WHERE id = %s
            """,
                (nombre, apellido, email, fecha_nacimiento, estudiante_id),
            )
            return cursor.rowcount

    @staticmethod
    def delete(estudiante_id):
        with get_db_cursor(commit=True) as cursor:
            cursor.execute("DELETE FROM estudiantes WHERE id = %s", (estudiante_id,))
            return cursor.rowcount

    @staticmethod
    def count_matriculas(estudiante_id):
        with get_db_cursor() as cursor:
            cursor.execute(
                """
                SELECT COUNT(*) as total 
                FROM matriculas 
                WHERE estudiante_id = %s
            """,
                (estudiante_id,),
            )
            result = cursor.fetchone()
            return result["total"] if result else 0
