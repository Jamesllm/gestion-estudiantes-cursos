from wsgiref.simple_server import make_server
from http.cookies import SimpleCookie
from controllers import (
    estudiante_controller,
    curso_controller,
    matricula_controller,
    auth_controller,
    dashboard_controller,
    export_controller,
    estudiante_view_controller,
)
import re
import json
import uuid

sessions = {}


def get_session(environ):
    """Obtiene la sesión del usuario desde las cookies"""
    cookie = SimpleCookie()
    cookie_header = environ.get("HTTP_COOKIE", "")
    
    if cookie_header:
        cookie.load(cookie_header)
        if "session_id" in cookie:
            session_id = cookie["session_id"].value
            session = sessions.get(session_id)
            
            # Debug logging
            if session:
                print(f"🔑 Sesión encontrada para ID: {session_id[:8]}... - Usuario: {session.get('username', 'N/A')}")
            else:
                print(f"⚠️  Session ID en cookie pero no en memoria: {session_id[:8]}...")
            
            return session
        else:
            print(f"⚠️  Cookie presente pero sin session_id")
    else:
        print(f"⚠️  No hay cookie en la petición a {environ.get('PATH_INFO', '/')}")
    
    return None


def create_session(user_data):
    """Crea una nueva sesión"""
    session_id = str(uuid.uuid4())
    sessions[session_id] = user_data
    return session_id


def delete_session(session_id):
    """Elimina una sesión"""
    if session_id in sessions:
        del sessions[session_id]


def require_auth(rol=None):
    """Decorador para rutas que requieren autenticación"""

    def decorator(func):
        def wrapper(environ, start_response, *args, **kwargs):
            session = get_session(environ)
            if not session:
                # Redirigir al login
                start_response("302 Found", [("Location", "/login")])
                return [b""]

            if rol and session.get("rol") != rol:
                # Sin permisos
                start_response(
                    "403 Forbidden", [("Content-Type", "text/html; charset=utf-8")]
                )
                return [b"<html><body><h1>403 - Acceso Denegado</h1></body></html>"]

            return func(environ, start_response, session, *args, **kwargs)

        return wrapper

    return decorator


def application(environ, start_response):
    path = environ.get("PATH_INFO", "/")
    method = environ.get("REQUEST_METHOD", "GET")
    session = get_session(environ)

    try:
        # ========== RUTAS PÚBLICAS (SIN AUTENTICACIÓN) ==========
        if path == "/login" and method == "GET":
            response_body = auth_controller.login_form()
            status = "200 OK"
            headers = [("Content-Type", "text/html; charset=utf-8")]
            start_response(status, headers)
            return [response_body.encode("utf-8")]

        elif path == "/login" and method == "POST":
            result = auth_controller.login(environ)
            if result["success"]:
                session_id = create_session(result["user"])
                cookie = SimpleCookie()
                cookie["session_id"] = session_id
                cookie["session_id"]["path"] = "/"
                cookie["session_id"]["max-age"] = 86400  # 24 horas
                cookie["session_id"]["httponly"] = True  # Seguridad adicional
                
                # Debug: imprimir información de la sesión
                print(f"✅ Login exitoso - Usuario: {result['user']['username']}")
                print(f"✅ Session ID creado: {session_id}")
                print(f"✅ Sesión almacenada: {session_id in sessions}")

                headers = [
                    ("Set-Cookie", cookie["session_id"].OutputString()),
                    ("Location", "/dashboard"),
                ]
                start_response("302 Found", headers)
                return [b""]
            else:
                response_body = auth_controller.login_form(error=result["error"])
                status = "200 OK"
                headers = [("Content-Type", "text/html; charset=utf-8")]
                start_response(status, headers)
                return [response_body.encode("utf-8")]

        elif path == "/logout":
            cookie_header = environ.get("HTTP_COOKIE", "")
            if cookie_header:
                cookie = SimpleCookie()
                cookie.load(cookie_header)
                if "session_id" in cookie:
                    delete_session(cookie["session_id"].value)

            cookie = SimpleCookie()
            cookie["session_id"] = ""
            cookie["session_id"]["path"] = "/"
            cookie["session_id"]["max-age"] = 0

            headers = [
                ("Content-Type", "text/html; charset=utf-8"),
                ("Location", "/login"),
                ("Set-Cookie", cookie["session_id"].OutputString()),
            ]
            start_response("302 Found", headers)
            return [b""]

        # ========== VERIFICAR AUTENTICACIÓN PARA OTRAS RUTAS ==========
        if not session:
            headers = [
                ("Content-Type", "text/html; charset=utf-8"),
                ("Location", "/login"),
            ]
            start_response("302 Found", headers)
            return [b""]

        # Agregar session a environ para acceso en controllers
        environ["session"] = session
        environ["request_path"] = path

        # ========== DASHBOARD ==========
        if path == "/dashboard" and method == "GET":
            if session["rol"] == "admin":
                response_body = dashboard_controller.admin_dashboard(session)
            else:
                response_body = dashboard_controller.estudiante_dashboard(session)
            status = "200 OK"

        # ========== RUTAS DE ADMINISTRADOR ==========
        elif session["rol"] == "admin":
            # ESTUDIANTES
            if path == "/estudiantes" and method == "GET":
                response_body = estudiante_controller.index(session, path)
                status = "200 OK"
            elif path == "/estudiantes/create" and method == "GET":
                response_body = estudiante_controller.create_form(session, path)
                status = "200 OK"
            elif path == "/estudiantes/create" and method == "POST":
                response_body = estudiante_controller.create(environ, session)
                status = "200 OK"
            elif re.match(r"^/estudiantes/(\d+)/edit$", path) and method == "GET":
                estudiante_id = int(
                    re.match(r"^/estudiantes/(\d+)/edit$", path).group(1)
                )
                response_body = estudiante_controller.edit_form(estudiante_id, session, path)
                status = "200 OK"
            elif re.match(r"^/estudiantes/(\d+)/update$", path) and method == "POST":
                estudiante_id = int(
                    re.match(r"^/estudiantes/(\d+)/update$", path).group(1)
                )
                response_body = estudiante_controller.update(environ, estudiante_id, session)
                status = "200 OK"
            elif re.match(r"^/estudiantes/(\d+)/delete$", path) and method == "POST":
                estudiante_id = int(
                    re.match(r"^/estudiantes/(\d+)/delete$", path).group(1)
                )
                response_body = estudiante_controller.delete(estudiante_id, session)
                status = "200 OK"

            # CURSOS
            elif path == "/cursos" and method == "GET":
                response_body = curso_controller.index(session, path)
                status = "200 OK"
            elif path == "/cursos/create" and method == "GET":
                response_body = curso_controller.create_form(session, path)
                status = "200 OK"
            elif path == "/cursos/create" and method == "POST":
                response_body = curso_controller.create(environ, session)
                status = "200 OK"
            elif re.match(r"^/cursos/(\d+)/edit$", path) and method == "GET":
                curso_id = int(re.match(r"^/cursos/(\d+)/edit$", path).group(1))
                response_body = curso_controller.edit_form(curso_id, session, path)
                status = "200 OK"
            elif re.match(r"^/cursos/(\d+)/update$", path) and method == "POST":
                curso_id = int(re.match(r"^/cursos/(\d+)/update$", path).group(1))
                response_body = curso_controller.update(environ, curso_id, session)
                status = "200 OK"
            elif re.match(r"^/cursos/(\d+)/delete$", path) and method == "POST":
                curso_id = int(re.match(r"^/cursos/(\d+)/delete$", path).group(1))
                response_body = curso_controller.delete(curso_id, session)
                status = "200 OK"

            # MATRÍCULAS
            elif path == "/matriculas" and method == "GET":
                response_body = matricula_controller.index(session, path)
                status = "200 OK"
            elif path == "/matriculas/create" and method == "POST":
                response_body = matricula_controller.create(environ, session)
                status = "200 OK"
            elif re.match(r"^/matriculas/(\d+)/edit$", path) and method == "GET":
                matricula_id = int(re.match(r"^/matriculas/(\d+)/edit$", path).group(1))
                response_body = matricula_controller.edit_form(matricula_id, session, path)
                status = "200 OK"
            elif re.match(r"^/matriculas/(\d+)/update$", path) and method == "POST":
                matricula_id = int(
                    re.match(r"^/matriculas/(\d+)/update$", path).group(1)
                )
                response_body = matricula_controller.update(environ, matricula_id, session)
                status = "200 OK"
            elif re.match(r"^/matriculas/(\d+)/delete$", path) and method == "POST":
                matricula_id = int(
                    re.match(r"^/matriculas/(\d+)/delete$", path).group(1)
                )
                response_body = matricula_controller.delete(matricula_id, session)
                status = "200 OK"

            # EXPORTACIÓN
            elif path == "/export/estudiantes/excel":
                buffer = export_controller.export_estudiantes_excel()
                headers = [
                    (
                        "Content-Type",
                        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    ),
                    ("Content-Disposition", "attachment; filename=estudiantes.xlsx"),
                ]
                start_response("200 OK", headers)
                return [buffer.read()]
            elif path == "/export/cursos/excel":
                buffer = export_controller.export_cursos_excel()
                headers = [
                    (
                        "Content-Type",
                        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    ),
                    ("Content-Disposition", "attachment; filename=cursos.xlsx"),
                ]
                start_response("200 OK", headers)
                return [buffer.read()]
            elif path == "/export/matriculas/excel":
                buffer = export_controller.export_matriculas_excel()
                headers = [
                    (
                        "Content-Type",
                        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    ),
                    ("Content-Disposition", "attachment; filename=matriculas.xlsx"),
                ]
                start_response("200 OK", headers)
                return [buffer.read()]
            elif path == "/export/estudiantes/pdf":
                buffer = export_controller.export_estudiantes_pdf()
                headers = [
                    ("Content-Type", "application/pdf"),
                    ("Content-Disposition", "attachment; filename=estudiantes.pdf"),
                ]
                start_response("200 OK", headers)
                return [buffer.read()]
            elif path == "/export/cursos/pdf":
                buffer = export_controller.export_cursos_pdf()
                headers = [
                    ("Content-Type", "application/pdf"),
                    ("Content-Disposition", "attachment; filename=cursos.pdf"),
                ]
                start_response("200 OK", headers)
                return [buffer.read()]
            else:
                status = "404 Not Found"
                response_body = (
                    "<html><body><h1>404 - Página no encontrada</h1></body></html>"
                )

        # ========== RUTAS DE ESTUDIANTE ==========
        elif session["rol"] == "estudiante":
            if path == "/explorar-cursos" and method == "GET":
                response_body = estudiante_view_controller.explorar_cursos(session)
                status = "200 OK"
            elif path == "/mis-cursos" and method == "GET":
                response_body = estudiante_view_controller.mis_cursos(session)
                status = "200 OK"
            elif path == "/estudiante/matricular" and method == "POST":
                response_body = estudiante_view_controller.matricular_estudiante(
                    environ, session
                )
                status = "200 OK"
            else:
                status = "404 Not Found"
                response_body = (
                    "<html><body><h1>404 - Página no encontrada</h1></body></html>"
                )

        # HOME
        elif path == "/" or path == "":
            headers = [
                ("Content-Type", "text/html; charset=utf-8"),
                ("Location", "/dashboard"),
            ]
            start_response("302 Found", headers)
            return [b""]

        else:
            status = "404 Not Found"
            response_body = (
                "<html><body><h1>404 - Página no encontrada</h1></body></html>"
            )

    except Exception as e:
        status = "500 Internal Server Error"
        response_body = (
            f"<html><body><h1>Error del servidor</h1><p>{str(e)}</p></body></html>"
        )

    headers = [("Content-Type", "text/html; charset=utf-8")]
    start_response(status, headers)
    return [response_body.encode("utf-8")]


if __name__ == "__main__":
    with make_server("", 8000, application) as httpd:
        print("=" * 60)
        print("🚀 SERVIDOR CORRIENDO")
        print("=" * 60)
        print("📍 URL: http://localhost:8000")
        print("👤 Admin: admin / admin123")
        print("🎓 Estudiante: juan.perez / estudiante123")
        print("⚡ Presiona CTRL+C para detener")
        print("=" * 60)
        httpd.serve_forever()
