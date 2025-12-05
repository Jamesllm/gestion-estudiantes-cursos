CREATE DATABASE IF NOT EXISTS sistema_educativo CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE sistema_educativo;

-- ========== TABLA ESTUDIANTES ==========
CREATE TABLE IF NOT EXISTS estudiantes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    fecha_nacimiento DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_nombre_apellido (nombre, apellido)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ========== TABLA PROFESORES (NUEVA) ==========
CREATE TABLE IF NOT EXISTS profesores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    especialidad VARCHAR(200),
    telefono VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_nombre_apellido (nombre, apellido)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ========== TABLA CURSOS ==========
CREATE TABLE IF NOT EXISTS cursos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(20) NOT NULL UNIQUE,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    creditos INT NOT NULL DEFAULT 0,
    profesor_id INT DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (profesor_id) REFERENCES profesores(id) ON DELETE SET NULL,
    INDEX idx_codigo (codigo),
    INDEX idx_nombre (nombre),
    INDEX idx_profesor (profesor_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ========== TABLA MATRÍCULAS ==========
CREATE TABLE IF NOT EXISTS matriculas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    estudiante_id INT NOT NULL,
    curso_id INT NOT NULL,
    fecha_matricula DATE NOT NULL,
    estado ENUM('activo', 'inactivo', 'completado') DEFAULT 'activo',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (curso_id) REFERENCES cursos(id) ON DELETE CASCADE ON UPDATE CASCADE,
    UNIQUE KEY unique_matricula (estudiante_id, curso_id),
    INDEX idx_estudiante (estudiante_id),
    INDEX idx_curso (curso_id),
    INDEX idx_estado (estado)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ========== TABLA USUARIOS ==========
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    rol ENUM('admin', 'estudiante', 'profesor') NOT NULL DEFAULT 'estudiante',
    estudiante_id INT DEFAULT NULL,
    profesor_id INT DEFAULT NULL,
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id) ON DELETE CASCADE,
    FOREIGN KEY (profesor_id) REFERENCES profesores(id) ON DELETE CASCADE,
    INDEX idx_username (username),
    INDEX idx_rol (rol)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ========== STORED PROCEDURES ==========
DELIMITER $$

CREATE PROCEDURE sp_get_estudiante_cursos(IN est_id INT)
BEGIN
    SELECT c.id, c.codigo, c.nombre, m.fecha_matricula, m.estado
    FROM matriculas m
    INNER JOIN cursos c ON m.curso_id = c.id
    WHERE m.estudiante_id = est_id;
END$$

DELIMITER ;

-- ========== INSERTAR ESTUDIANTES (50) ==========
INSERT INTO estudiantes (nombre, apellido, email, fecha_nacimiento) VALUES
('Juan', 'Pérez', 'juan.perez@email.com', '2000-03-15'),
('María', 'González', 'maria.gonzalez@email.com', '1999-07-22'),
('Carlos', 'Rodríguez', 'carlos.rodriguez@email.com', '2001-01-10'),
('Ana', 'Martínez', 'ana.martinez@email.com', '2000-11-30'),
('Luis', 'López', 'luis.lopez@email.com', '1998-05-18'),
('Carmen', 'Sánchez', 'carmen.sanchez@email.com', '2001-09-25'),
('Pedro', 'Ramírez', 'pedro.ramirez@email.com', '1999-12-08'),
('Laura', 'Torres', 'laura.torres@email.com', '2000-06-14'),
('Diego', 'Flores', 'diego.flores@email.com', '2001-02-28'),
('Sofía', 'Rivera', 'sofia.rivera@email.com', '1999-08-19'),
('Miguel', 'Gómez', 'miguel.gomez@email.com', '2000-04-07'),
('Valentina', 'Díaz', 'valentina.diaz@email.com', '2001-10-12'),
('Andrés', 'Morales', 'andres.morales@email.com', '1998-11-23'),
('Isabella', 'Jiménez', 'isabella.jimenez@email.com', '2000-01-17'),
('Sebastián', 'Hernández', 'sebastian.hernandez@email.com', '1999-05-29'),
('Camila', 'Castro', 'camila.castro@email.com', '2001-07-04'),
('Mateo', 'Vargas', 'mateo.vargas@email.com', '2000-09-11'),
('Lucía', 'Ortiz', 'lucia.ortiz@email.com', '1999-03-26'),
('Daniel', 'Ruiz', 'daniel.ruiz@email.com', '2001-12-02'),
('Gabriela', 'Mendoza', 'gabriela.mendoza@email.com', '2000-08-15'),
('Alejandro', 'Silva', 'alejandro.silva@email.com', '1998-06-21'),
('Natalia', 'Rojas', 'natalia.rojas@email.com', '2001-04-09'),
('Fernando', 'Paredes', 'fernando.paredes@email.com', '1999-10-16'),
('Paula', 'Vega', 'paula.vega@email.com', '2000-02-27'),
('Ricardo', 'Navarro', 'ricardo.navarro@email.com', '2001-08-03'),
('Andrea', 'Campos', 'andrea.campos@email.com', '1999-01-14'),
('Javier', 'Reyes', 'javier.reyes@email.com', '2000-07-20'),
('Daniela', 'Guerrero', 'daniela.guerrero@email.com', '2001-11-06'),
('Ángel', 'Medina', 'angel.medina@email.com', '1998-09-18'),
('Mariana', 'Cruz', 'mariana.cruz@email.com', '2000-05-24'),
('Roberto', 'Peña', 'roberto.pena@email.com', '1999-12-31'),
('Carolina', 'Cortés', 'carolina.cortes@email.com', '2001-03-13'),
('Gustavo', 'Aguilar', 'gustavo.aguilar@email.com', '2000-10-22'),
('Elena', 'Luna', 'elena.luna@email.com', '1999-06-08'),
('Raúl', 'Ríos', 'raul.rios@email.com', '2001-01-29'),
('Adriana', 'Pacheco', 'adriana.pacheco@email.com', '2000-11-15'),
('Francisco', 'Salazar', 'francisco.salazar@email.com', '1998-08-05'),
('Verónica', 'Núñez', 'veronica.nunez@email.com', '2001-04-18'),
('Héctor', 'Domínguez', 'hector.dominguez@email.com', '1999-02-11'),
('Patricia', 'Gil', 'patricia.gil@email.com', '2000-09-27'),
('Óscar', 'Ibarra', 'oscar.ibarra@email.com', '2001-06-03'),
('Silvia', 'León', 'silvia.leon@email.com', '1999-11-19'),
('Manuel', 'Cabrera', 'manuel.cabrera@email.com', '2000-03-08'),
('Mónica', 'Figueroa', 'monica.figueroa@email.com', '2001-10-25'),
('Arturo', 'Sandoval', 'arturo.sandoval@email.com', '1998-07-12'),
('Rosa', 'Valencia', 'rosa.valencia@email.com', '2000-01-01'),
('Enrique', 'Zamora', 'enrique.zamora@email.com', '1999-08-28'),
('Gloria', 'Carrillo', 'gloria.carrillo@email.com', '2001-05-14'),
('Alberto', 'Miranda', 'alberto.miranda@email.com', '2000-12-20'),
('Beatriz', 'Mora', 'beatriz.mora@email.com', '1999-04-06');

-- ========== INSERTAR PROFESORES (15) ==========
INSERT INTO profesores (nombre, apellido, email, especialidad, telefono) VALUES
('Roberto', 'García', 'roberto.garcia@profesor.com', 'Ciencias de la Computación', '555-0101'),
('Patricia', 'Fernández', 'patricia.fernandez@profesor.com', 'Estructuras de Datos', '555-0102'),
('Jorge', 'Mendoza', 'jorge.mendoza@profesor.com', 'Algoritmos', '555-0103'),
('Sandra', 'Ponce', 'sandra.ponce@profesor.com', 'Programación Orientada a Objetos', '555-0104'),
('Martín', 'Vargas', 'martin.vargas@profesor.com', 'Base de Datos', '555-0105'),
('Claudia', 'Rojas', 'claudia.rojas@profesor.com', 'Desarrollo Web', '555-0106'),
('Fernando', 'Silva', 'fernando.silva@profesor.com', 'Inteligencia Artificial', '555-0107'),
('Mónica', 'Campos', 'monica.campos@profesor.com', 'Seguridad Informática', '555-0108'),
('Ricardo', 'Torres', 'ricardo.torres@profesor.com', 'Matemáticas', '555-0109'),
('Elena', 'Castro', 'elena.castro@profesor.com', 'Física', '555-0110'),
('Alberto', 'Herrera', 'alberto.herrera@profesor.com', 'Inglés', '555-0111'),
('Diana', 'Morales', 'diana.morales@profesor.com', 'Administración', '555-0112'),
('Felipe', 'Ruiz', 'felipe.ruiz@profesor.com', 'Sistemas Operativos', '555-0113'),
('Valeria', 'Ortiz', 'valeria.ortiz@profesor.com', 'Redes', '555-0114'),
('Gabriel', 'Luna', 'gabriel.luna@profesor.com', 'Desarrollo Móvil', '555-0115');

-- ========== INSERTAR CURSOS (30) CON PROFESORES ASIGNADOS ==========
INSERT INTO cursos (codigo, nombre, descripcion, creditos, profesor_id) VALUES
('CS101', 'Introducción a la Programación', 'Fundamentos de programación con Python y estructuras de datos básicas', 4, 1),
('CS102', 'Estructuras de Datos', 'Estudio avanzado de estructuras de datos: árboles, grafos, pilas y colas', 5, 2),
('CS201', 'Algoritmos y Complejidad', 'Análisis de algoritmos, notación Big-O y optimización', 5, 3),
('CS202', 'Programación Orientada a Objetos', 'POO con Java: clases, herencia, polimorfismo y patrones de diseño', 4, 4),
('CS301', 'Base de Datos', 'Diseño de bases de datos relacionales, SQL y normalización', 4, 5),
('CS302', 'Desarrollo Web', 'HTML, CSS, JavaScript y frameworks modernos', 5, 6),
('CS401', 'Inteligencia Artificial', 'Machine Learning, redes neuronales y procesamiento de lenguaje natural', 5, 7),
('CS402', 'Seguridad Informática', 'Criptografía, hacking ético y protección de sistemas', 4, 8),
('MAT101', 'Cálculo I', 'Límites, derivadas e integrales', 5, 9),
('MAT102', 'Cálculo II', 'Integrales múltiples y series infinitas', 5, 9),
('MAT201', 'Álgebra Lineal', 'Vectores, matrices y transformaciones lineales', 4, 9),
('MAT202', 'Probabilidad y Estadística', 'Teoría de probabilidades y estadística inferencial', 4, 9),
('FIS101', 'Física I', 'Mecánica clásica y cinemática', 5, 10),
('FIS102', 'Física II', 'Electromagnetismo y óptica', 5, 10),
('ENG101', 'Inglés Técnico I', 'Vocabulario técnico y lectura de documentación', 3, 11),
('ENG102', 'Inglés Técnico II', 'Redacción técnica y presentaciones', 3, 11),
('ADM101', 'Administración de Proyectos', 'Metodologías ágiles, Scrum y gestión de equipos', 4, 12),
('ADM102', 'Emprendimiento Digital', 'Startups tecnológicas y modelos de negocio', 3, 12),
('CS303', 'Sistemas Operativos', 'Procesos, memoria, sistemas de archivos y concurrencia', 5, 13),
('CS304', 'Redes de Computadoras', 'Protocolos TCP/IP, arquitectura de redes y seguridad', 4, 14),
('CS305', 'Compiladores', 'Análisis léxico, sintáctico y generación de código', 5, 3),
('CS306', 'Computación en la Nube', 'AWS, Azure, Docker y Kubernetes', 4, 6),
('CS307', 'Desarrollo Móvil', 'Android y iOS con React Native', 4, 15),
('CS308', 'Big Data', 'Hadoop, Spark y análisis de grandes volúmenes de datos', 5, 7),
('CS403', 'Robótica', 'Programación de robots y sistemas embebidos', 4, 1),
('CS404', 'Computación Gráfica', 'OpenGL, modelado 3D y animación', 5, 6),
('HUM101', 'Ética Profesional', 'Responsabilidad social y dilemas éticos en tecnología', 3, 12),
('HUM102', 'Comunicación Efectiva', 'Oratoria, redacción y trabajo en equipo', 3, 11),
('CS405', 'DevOps', 'CI/CD, automatización e infraestructura como código', 4, 8),
('CS406', 'Blockchain', 'Criptomonedas, contratos inteligentes y aplicaciones descentralizadas', 4, 7);

-- ========== INSERTAR MATRÍCULAS (150) ==========
INSERT INTO matriculas (estudiante_id, curso_id, fecha_matricula, estado) VALUES
(1, 1, '2024-01-15', 'completado'), (1, 2, '2024-05-20', 'completado'), (1, 9, '2024-01-15', 'completado'),
(1, 13, '2024-05-20', 'activo'), (1, 15, '2024-01-15', 'completado'),
(2, 1, '2024-01-15', 'completado'), (2, 3, '2024-05-20', 'activo'), (2, 9, '2024-01-15', 'completado'),
(2, 11, '2024-05-20', 'activo'), (2, 15, '2024-01-15', 'completado'),
(3, 1, '2024-01-18', 'completado'), (3, 2, '2024-06-01', 'activo'), (3, 5, '2024-01-18', 'completado'),
(3, 10, '2024-06-01', 'activo'), (3, 16, '2024-01-18', 'completado'),
(4, 1, '2024-01-20', 'completado'), (4, 4, '2024-06-05', 'activo'), (4, 9, '2024-01-20', 'completado'),
(4, 12, '2024-06-05', 'activo'), (4, 15, '2024-01-20', 'completado'),
(5, 2, '2024-02-10', 'completado'), (5, 3, '2024-06-15', 'activo'), (5, 11, '2024-02-10', 'completado'),
(5, 19, '2024-06-15', 'activo'), (5, 27, '2024-02-10', 'completado'),
(6, 1, '2024-02-12', 'completado'), (6, 5, '2024-06-20', 'activo'), (6, 9, '2024-02-12', 'completado'),
(6, 13, '2024-06-20', 'activo'), (6, 15, '2024-02-12', 'completado'),
(7, 1, '2024-02-14', 'completado'), (7, 2, '2024-07-01', 'activo'), (7, 10, '2024-02-14', 'completado'),
(7, 14, '2024-07-01', 'activo'), (7, 16, '2024-02-14', 'completado'),
(8, 1, '2024-02-16', 'completado'), (8, 6, '2024-07-05', 'activo'), (8, 9, '2024-02-16', 'completado'),
(8, 15, '2024-07-05', 'activo'), (8, 17, '2024-02-16', 'completado'),
(9, 2, '2024-03-01', 'completado'), (9, 4, '2024-07-10', 'activo'), (9, 11, '2024-03-01', 'completado'),
(9, 20, '2024-07-10', 'activo'), (9, 28, '2024-03-01', 'completado'),
(10, 1, '2024-03-05', 'completado'), (10, 3, '2024-07-15', 'activo'), (10, 9, '2024-03-05', 'completado'),
(10, 12, '2024-07-15', 'activo'), (10, 15, '2024-03-05', 'completado'),
(11, 1, '2024-03-08', 'completado'), (11, 5, '2024-08-01', 'activo'), (11, 10, '2024-03-08', 'completado'),
(11, 13, '2024-08-01', 'activo'), (11, 16, '2024-03-08', 'completado'),
(12, 2, '2024-03-10', 'completado'), (12, 6, '2024-08-05', 'activo'), (12, 11, '2024-03-10', 'completado'),
(12, 14, '2024-08-05', 'activo'), (12, 17, '2024-03-10', 'completado'),
(13, 3, '2024-03-12', 'completado'), (13, 7, '2024-08-10', 'activo'), (13, 11, '2024-03-12', 'completado'),
(13, 19, '2024-08-10', 'activo'), (13, 27, '2024-03-12', 'completado'),
(14, 1, '2024-03-15', 'completado'), (14, 2, '2024-08-15', 'activo'), (14, 9, '2024-03-15', 'completado'),
(14, 15, '2024-08-15', 'activo'), (14, 18, '2024-03-15', 'completado'),
(15, 1, '2024-03-18', 'completado'), (15, 4, '2024-08-20', 'activo'), (15, 10, '2024-03-18', 'completado'),
(15, 12, '2024-08-20', 'activo'), (15, 16, '2024-03-18', 'completado'),
(16, 2, '2024-04-01', 'completado'), (16, 5, '2024-09-01', 'activo'), (16, 11, '2024-04-01', 'completado'),
(16, 20, '2024-09-01', 'activo'), (16, 28, '2024-04-01', 'completado'),
(17, 1, '2024-04-05', 'completado'), (17, 3, '2024-09-05', 'activo'), (17, 9, '2024-04-05', 'completado'),
(17, 13, '2024-09-05', 'activo'), (17, 15, '2024-04-05', 'completado'),
(18, 1, '2024-04-08', 'completado'), (18, 6, '2024-09-10', 'activo'), (18, 10, '2024-04-08', 'completado'),
(18, 14, '2024-09-10', 'activo'), (18, 17, '2024-04-08', 'completado'),
(19, 2, '2024-04-10', 'completado'), (19, 7, '2024-09-15', 'activo'), (19, 11, '2024-04-10', 'completado'),
(19, 21, '2024-09-15', 'activo'), (19, 27, '2024-04-10', 'completado'),
(20, 1, '2024-04-12', 'completado'), (20, 2, '2024-09-20', 'activo'), (20, 9, '2024-04-12', 'completado'),
(20, 15, '2024-09-20', 'activo'), (20, 18, '2024-04-12', 'completado'),
(21, 3, '2024-04-15', 'completado'), (21, 4, '2024-10-01', 'activo'), (21, 11, '2024-04-15', 'completado'),
(21, 19, '2024-10-01', 'activo'), (21, 28, '2024-04-15', 'completado'),
(22, 1, '2024-04-18', 'completado'), (22, 5, '2024-10-05', 'activo'), (22, 10, '2024-04-18', 'completado'),
(22, 12, '2024-10-05', 'activo'), (22, 16, '2024-04-18', 'completado'),
(23, 2, '2024-04-20', 'completado'), (23, 6, '2024-10-10', 'activo'), (23, 11, '2024-04-20', 'completado'),
(23, 20, '2024-10-10', 'activo'), (23, 17, '2024-04-20', 'completado'),
(24, 1, '2024-04-22', 'completado'), (24, 3, '2024-10-15', 'activo'), (24, 9, '2024-04-22', 'completado'),
(24, 13, '2024-10-15', 'activo'), (24, 15, '2024-04-22', 'completado'),
(25, 1, '2024-04-25', 'completado'), (25, 7, '2024-10-20', 'activo'), (25, 10, '2024-04-25', 'completado'),
(25, 14, '2024-10-20', 'activo'), (25, 18, '2024-04-25', 'completado');

-- ========== INSERTAR USUARIOS CON SHA256 ==========
-- admin / admin123
-- Profesores: roberto.garcia / profesor123, patricia.fernandez / profesor123
-- Estudiantes: juan.perez / estudiante123, maria.gonzalez / estudiante123

INSERT INTO usuarios (username, password, rol, estudiante_id, profesor_id) VALUES
-- ADMIN (sin estudiante ni profesor)
('admin', 'admin123', 'admin', NULL, NULL),

-- PROFESORES (admin con profesor_id)
('roberto.garcia', 'profesor123', 'admin', NULL, 1),
('patricia.fernandez', 'profesor123', 'admin', NULL, 2),
('jorge.mendoza', 'profesor123', 'admin', NULL, 3),
('sandra.ponce', 'profesor123', 'admin', NULL, 4),

-- ESTUDIANTES
('juan.perez', 'estudiante123', 'estudiante', 1, NULL),
('maria.gonzalez', 'estudiante123', 'estudiante', 2, NULL),
('carlos.rodriguez', 'estudiante123', 'estudiante', 3, NULL),
('ana.martinez', 'estudiante123', 'estudiante', 4, NULL),
('luis.lopez', 'estudiante123', 'estudiante', 5, NULL);

-- ========== VERIFICAR DATOS ==========
SELECT '=== ESTUDIANTES ===' as info;
SELECT COUNT(*) as total FROM estudiantes;

SELECT '=== PROFESORES ===' as info;
SELECT COUNT(*) as total FROM profesores;

SELECT '=== CURSOS ===' as info;
SELECT COUNT(*) as total FROM cursos;

SELECT '=== MATRÍCULAS ===' as info;
SELECT COUNT(*) as total FROM matriculas;

SELECT '=== USUARIOS ===' as info;
SELECT id, username, rol, 
       CASE 
           WHEN estudiante_id IS NOT NULL THEN CONCAT('Estudiante ID: ', estudiante_id)
           WHEN profesor_id IS NOT NULL THEN CONCAT('Profesor ID: ', profesor_id)
           ELSE 'Admin puro'
       END as tipo
FROM usuarios;