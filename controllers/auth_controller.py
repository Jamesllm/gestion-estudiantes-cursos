from config.template_config import get_template
from urllib.parse import parse_qs
from models.usuario import Usuario



def login_form(error=None):
    template = get_template("auth/login.html")
    return template.render(error=error)


def login(environ):
    try:
        content_length = int(environ.get("CONTENT_LENGTH", 0))
    except ValueError:
        content_length = 0

    post_data = environ["wsgi.input"].read(content_length).decode("utf-8")
    fields = parse_qs(post_data)

    username = fields.get("username", [""])[0].strip()
    password = fields.get("password", [""])[0]

    user = Usuario.authenticate(username, password)

    if user:
        return {"success": True, "user": user}
    else:
        return {"success": False, "error": "Usuario o contraseña incorrectos"}


def logout():
    return login_form()
