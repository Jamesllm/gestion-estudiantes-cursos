## 1. PARADIGMA DE PROGRAMACIÓN EMPLEADO

**Paradigma Orientado a Objetos (POO)**

El proyecto implementa el paradigma orientado a objetos mediante:

- **Clases como modelos de datos**: `Estudiante`, `Curso`, `Matricula`, `Usuario`, `Estadisticas`, `Exporters`
- **Métodos estáticos**: Todas las operaciones CRUD están encapsuladas en métodos de clase
- **Separación de responsabilidades**: Arquitectura MVC (Modelo-Vista-Controlador)
- **Encapsulamiento**: Cada clase maneja su propia lógica de negocio
- **Reutilización de código**: Context managers para gestión de base de datos

### Estructura POO del Proyecto:

```
Models (Clases de Negocio):
├── Estudiante (CRUD de estudiantes)
├── Curso (CRUD de cursos)
├── Matricula (CRUD de matrículas)
├── Usuario (Autenticación)
├── Estadisticas (Métricas del sistema)
└── Exporters (Generación de reportes)

Controllers (Lógica de Control):
├── estudiante_controller
├── curso_controller
├── matricula_controller
├── auth_controller
├── dashboard_controller
└── export_controller
```

---

## 2. DIAGRAMA LÓGICO DE LA BASE DE DATOS

```
┌─────────────────────────┐
│      ESTUDIANTES        │
├─────────────────────────┤
│ PK id (INT)             │
│    nombre (VARCHAR)     │
│    apellido (VARCHAR)   │
│    email (VARCHAR) UK   │
│    fecha_nacimiento     │
│    created_at           │
│    updated_at           │
└──────────┬──────────────┘
           │
           │ 1:N
           │
┌──────────▼──────────────┐         ┌─────────────────────────┐
│      MATRICULAS         │   N:1   │        CURSOS           │
├─────────────────────────┤◄────────┤─────────────────────────┤
│ PK id (INT)             │         │ PK id (INT)             │
│ FK estudiante_id (INT)  │         │    codigo (VARCHAR) UK  │
│ FK curso_id (INT)       │         │    nombre (VARCHAR)     │
│    fecha_matricula      │         │    descripcion (TEXT)   │
│    estado (ENUM)        │         │    creditos (INT)       │
│    created_at           │         │ FK profesor_id (INT)    │
│    updated_at           │         │    created_at           │
└─────────────────────────┘         │    updated_at           │
                                    └──────────┬──────────────┘
                                               │
                                               │ N:1
                                               │
┌─────────────────────────┐         ┌──────────▼──────────────┐
│       USUARIOS          │         │      PROFESORES         │
├─────────────────────────┤         ├─────────────────────────┤
│ PK id (INT)             │         │ PK id (INT)             │
│    username (VARCHAR)UK │         │    nombre (VARCHAR)     │
│    password (VARCHAR)   │         │    apellido (VARCHAR)   │
│    rol (ENUM)           │         │    email (VARCHAR) UK   │
│ FK estudiante_id (INT)  │         │    especialidad         │
│ FK profesor_id (INT)    │         │    telefono             │
│    activo (BOOLEAN)     │         │    created_at           │
│    created_at           │         │    updated_at           │
│    updated_at           │         └─────────────────────────┘
└──────────┬──────────────┘
           │
           │ 1:1
           │
           └──────────────────────────────────────┐
                                                  │
                                                  ▼
                                    (Relación con ESTUDIANTES)
```

### Relaciones:
- **ESTUDIANTES → MATRICULAS**: 1:N (Un estudiante puede tener múltiples matrículas)
- **CURSOS → MATRICULAS**: 1:N (Un curso puede tener múltiples matrículas)
- **PROFESORES → CURSOS**: 1:N (Un profesor puede impartir múltiples cursos)
- **USUARIOS → ESTUDIANTES**: 1:1 (Un usuario estudiante vinculado a un registro de estudiante)
- **USUARIOS → PROFESORES**: 1:1 (Un usuario profesor vinculado a un registro de profesor)

### Constraints:
- **UNIQUE**: `estudiante_id + curso_id` en MATRICULAS (evita matrículas duplicadas)
- **CASCADE**: DELETE CASCADE en relaciones de matrículas
- **ENUM**: Estado de matrícula ('activo', 'inactivo', 'completado')
- **ENUM**: Rol de usuario ('admin', 'estudiante', 'profesor')

---

## 3. FRAMEWORK CSS UTILIZADO

**DaisyUI + Tailwind CSS**

### Características implementadas:

#### DaisyUI (v4.4.19)
- **Componentes preconstruidos**: Botones, cards, modals, dropdowns, navbar
- **Sistema de temas**: Tema light configurado
- **Drawer responsive**: Sidebar colapsable para móviles
- **Componentes utilizados**:
  - `drawer` y `drawer-toggle` (navegación lateral)
  - `navbar` (barra superior)
  - `btn` (botones con variantes)
  - `card` (tarjetas de información)
  - `dropdown` (menú de usuario)
  - `menu` (navegación sidebar)
  - `stat-card` (tarjetas de estadísticas)

#### Tailwind CSS
- **Utility-first CSS**: Clases utilitarias para estilos rápidos
- **Responsive design**: Breakpoints (`lg:`, `md:`, `sm:`)
- **Flexbox y Grid**: Layout moderno
- **Spacing system**: Padding y margin consistentes

#### Font Awesome (v6.4.0)
- **Iconografía**: Íconos para navegación y acciones
- Ejemplos: `fa-graduation-cap`, `fa-user-graduate`, `fa-book`, `fa-chart-line`

#### Google Fonts
- **Tipografía**: Inter (weights 300-700)
- Mejora la legibilidad y estética moderna

### Variables CSS personalizadas:
```css
--primary-color: #1e3a8a
--primary-dark: #1e293b
--secondary-color: #475569
--accent-color: #3b82f6
--bg-primary: #f8fafc
--bg-secondary: #ffffff
```

---

## 4. OBJETIVOS DEL PROYECTO

### Objetivo General
Desarrollar un sistema web de gestión educativa que permita administrar estudiantes, cursos y matrículas de manera eficiente, con autenticación de usuarios y generación de reportes.

### Objetivos Específicos

1. **Gestión de Estudiantes**
   - Crear, leer, actualizar y eliminar registros de estudiantes
   - Validación de datos (email único, fechas válidas)
   - Visualización de matrículas por estudiante

2. **Gestión de Cursos**
   - Administración completa de cursos académicos
   - Asignación de profesores a cursos
   - Control de créditos y códigos únicos

3. **Sistema de Matrículas**
   - Registro de matrículas estudiante-curso
   - Control de estados (activo, inactivo, completado)
   - Prevención de matrículas duplicadas

4. **Autenticación y Autorización**
   - Sistema de login con sesiones
   - Roles diferenciados (admin, estudiante, profesor)
   - Control de acceso basado en roles

5. **Dashboard Interactivo**
   - Estadísticas en tiempo real
   - Visualización de métricas clave
   - Interfaces diferenciadas por rol

6. **Generación de Reportes**
   - Exportación a Excel (estudiantes, cursos, matrículas)
   - Exportación a PDF con diseño profesional
   - Descarga directa de archivos

7. **Arquitectura Escalable**
   - Patrón MVC implementado
   - Separación de responsabilidades
   - Código modular y reutilizable

---

## 5. APORTE A LA INVESTIGACIÓN

### 5.1 Implementación de WSGI Puro (Sin Frameworks)

**Innovación**: El proyecto demuestra que es posible construir aplicaciones web completas sin depender de frameworks pesados como Django o Flask.

**Ventajas demostradas**:
- Control total sobre el flujo de la aplicación
- Menor overhead y mejor rendimiento
- Comprensión profunda del protocolo HTTP
- Implementación manual de routing, sesiones y middleware

**Código relevante**:
```python
def application(environ, start_response):
    path = environ.get("PATH_INFO", "/")
    method = environ.get("REQUEST_METHOD", "GET")
    # Routing manual y gestión de sesiones
```

### 5.2 Gestión de Sesiones sin Redis/Memcached

**Innovación**: Sistema de sesiones en memoria con cookies HTTP-only.

**Implementación**:
```python
sessions = {}  # Almacenamiento en memoria

def create_session(user_data):
    session_id = str(uuid.uuid4())
    sessions[session_id] = user_data
    return session_id
```

**Seguridad implementada**:
- Cookies con flag `httponly=True`
- Expiración de sesiones (24 horas)
- Validación de sesiones en cada request

### 5.3 Patrón MVC sin ORM

**Innovación**: Implementación de MVC usando SQL puro en lugar de ORMs como SQLAlchemy.

**Ventajas**:
- Queries optimizadas manualmente
- Mejor control sobre transacciones
- Uso de stored procedures
- Context managers para gestión de conexiones

**Ejemplo**:
```python
@contextmanager
def get_db_cursor(commit=False):
    with get_db_connection() as connection:
        cursor = connection.cursor(dictionary=True)
        try:
            yield cursor
            if commit:
                connection.commit()
        except Exception as e:
            connection.rollback()
            raise
```

### 5.4 Sistema de Exportación Dual (Excel + PDF)

**Innovación**: Generación de reportes profesionales con formato personalizado.

**Librerías utilizadas**:
- **Pandas + OpenPyXL**: Exportación Excel con auto-ajuste de columnas
- **ReportLab**: PDFs con tablas estilizadas y branding

**Características**:
- Ajuste automático de anchos de columna
- Estilos personalizados (colores, fuentes)
- Metadatos (fecha de generación)
- Descarga directa desde el navegador

### 5.5 Arquitectura de Plantillas con Jinja2

**Innovación**: Sistema de templates sin framework web completo.

**Implementación**:
```python
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('views'))
template = env.get_template('base.html')
html = template.render(user=session, data=data)
```

**Ventajas**:
- Herencia de templates (`{% extends %}`)
- Reutilización de componentes
- Separación de lógica y presentación

### 5.6 Routing Basado en Expresiones Regulares

**Innovación**: Sistema de routing manual con regex para URLs dinámicas.

**Ejemplo**:
```python
if re.match(r"^/estudiantes/(\d+)/edit$", path):
    estudiante_id = int(re.match(r"^/estudiantes/(\d+)/edit$", path).group(1))
    response_body = estudiante_controller.edit_form(estudiante_id, session, path)
```

**Beneficios**:
- URLs RESTful
- Extracción de parámetros de URL
- Validación de formato de IDs

### 5.7 Diseño Responsive con DaisyUI

**Innovación**: UI moderna sin escribir CSS personalizado extenso.

**Características**:
- Drawer colapsable para móviles
- Grid responsive automático
- Componentes accesibles (ARIA)
- Tema consistente en toda la aplicación

### 5.8 Validación de Datos a Nivel de Base de Datos

**Innovación**: Uso de constraints SQL para integridad de datos.

**Implementaciones**:
- `UNIQUE KEY` en email de estudiantes
- `UNIQUE KEY` compuesta en matrículas (estudiante_id, curso_id)
- `ENUM` para estados y roles
- `FOREIGN KEY` con `ON DELETE CASCADE`
- Índices para optimización de consultas

### 5.9 Stored Procedures para Lógica Compleja

**Innovación**: Encapsulación de lógica en la base de datos.

**Ejemplo**:
```sql
CREATE PROCEDURE sp_get_estudiante_cursos(IN est_id INT)
BEGIN
    SELECT c.id, c.codigo, c.nombre, m.fecha_matricula, m.estado
    FROM matriculas m
    INNER JOIN cursos c ON m.curso_id = c.id
    WHERE m.estudiante_id = est_id;
END
```

### 5.10 Sistema de Autenticación Multinivel

**Innovación**: Tres roles con permisos diferenciados.

**Roles implementados**:
1. **Admin**: Acceso completo (CRUD de todo)
2. **Estudiante**: Vista de cursos y matrículas propias
3. **Profesor**: Gestión de cursos asignados

**Decorador de autorización**:
```python
def require_auth(rol=None):
    def decorator(func):
        def wrapper(environ, start_response, *args, **kwargs):
            session = get_session(environ)
            if not session:
                # Redirigir a login
            if rol and session.get("rol") != rol:
                # Acceso denegado
            return func(environ, start_response, session, *args, **kwargs)
        return wrapper
    return decorator
```

---

## CONCLUSIONES

Este proyecto demuestra que es posible construir aplicaciones web robustas y profesionales sin depender de frameworks monolíticos. La implementación manual de componentes clave como routing, sesiones, autenticación y MVC proporciona un aprendizaje profundo de los fundamentos del desarrollo web.

### Tecnologías Clave:
- **Backend**: Python puro con WSGI
- **Base de Datos**: MySQL con SQL puro
- **Frontend**: HTML + DaisyUI + Tailwind CSS + JavaScript
- **Reportes**: Pandas, OpenPyXL, ReportLab
- **Plantillas**: Jinja2

### Métricas del Proyecto:
- **5 modelos** de datos
- **7 controladores** de lógica
- **11 vistas** HTML
- **30 cursos** de ejemplo
- **50 estudiantes** de ejemplo
- **150 matrículas** de ejemplo
- **Arquitectura MVC** completa
- **Sistema de autenticación** con 3 roles
- **Exportación** a 2 formatos (Excel, PDF)

### Aplicabilidad:
Este proyecto es ideal para:
- Instituciones educativas pequeñas y medianas
- Aprendizaje de arquitecturas web sin frameworks
- Base para sistemas más complejos
- Demostración de buenas prácticas de programación
