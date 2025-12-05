from config.database import get_db_cursor

class Usuario:
    
    @staticmethod
    def authenticate(username, password):
        """Autentica un usuario con contraseña en texto plano"""
        try:
            with get_db_cursor() as cursor:
                cursor.execute("""
                    SELECT u.id, u.username, u.password, u.rol, u.estudiante_id, u.profesor_id,
                           e.nombre as est_nombre, e.apellido as est_apellido,
                           p.nombre as prof_nombre, p.apellido as prof_apellido
                    FROM usuarios u
                    LEFT JOIN estudiantes e ON u.estudiante_id = e.id
                    LEFT JOIN profesores p ON u.profesor_id = p.id
                    WHERE u.username = %s AND u.activo = TRUE
                """, (username,))
                user = cursor.fetchone()
                
                if not user:
                    print(f"❌ Usuario '{username}' no encontrado")
                    return None
                
                # Comparar contraseña en texto plano
                print(f"🔍 Debug - Usuario: {user['username']}")
                print(f"🔍 Debug - Contraseña ingresada: {password}")
                print(f"🔍 Debug - Contraseña en BD: {user['password']}")
                print(f"🔍 Debug - Coinciden: {password == user['password']}")
                
                if password == user['password']:
                    # Determinar nombre y apellido según el tipo de usuario
                    if user.get('est_nombre'):
                        nombre = user['est_nombre']
                        apellido = user['est_apellido']
                    elif user.get('prof_nombre'):
                        nombre = user['prof_nombre']
                        apellido = user['prof_apellido']
                    else:
                        nombre = 'Admin'
                        apellido = 'Sistema'
                    
                    return {
                        'id': user['id'],
                        'username': user['username'],
                        'rol': user['rol'],
                        'estudiante_id': user.get('estudiante_id'),
                        'profesor_id': user.get('profesor_id'),
                        'nombre': nombre,
                        'apellido': apellido
                    }
                else:
                    print(f"❌ Contraseña incorrecta para '{username}'")
                    return None
                    
        except Exception as e:
            print(f"❌ Error en authenticate: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    @staticmethod
    def get_all():
        with get_db_cursor() as cursor:
            cursor.execute("""
                SELECT u.id, u.username, u.rol, u.estudiante_id, u.activo,
                       e.nombre, e.apellido
                FROM usuarios u
                LEFT JOIN estudiantes e ON u.estudiante_id = e.id
                ORDER BY u.created_at DESC
            """)
            return cursor.fetchall()
    
    @staticmethod
    def create(username, password, rol, estudiante_id=None):
        """Crea un usuario con contraseña en texto plano"""
        with get_db_cursor(commit=True) as cursor:
            cursor.execute("""
                INSERT INTO usuarios (username, password, rol, estudiante_id) 
                VALUES (%s, %s, %s, %s)
            """, (username, password, rol, estudiante_id))
            return cursor.lastrowid
    
    @staticmethod
    def get_by_id(user_id):
        with get_db_cursor() as cursor:
            cursor.execute("""
                SELECT u.*, e.nombre, e.apellido
                FROM usuarios u
                LEFT JOIN estudiantes e ON u.estudiante_id = e.id
                WHERE u.id = %s
            """, (user_id,))
            return cursor.fetchone()