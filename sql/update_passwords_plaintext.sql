-- Script para actualizar las contraseñas de los usuarios existentes
-- Ejecutar este script después de crear las tablas

USE sistema_educativo;

-- Actualizar contraseñas a texto plano
UPDATE usuarios SET password = 'admin123' WHERE username = 'admin';
UPDATE usuarios SET password = 'profesor123' WHERE username = 'roberto.garcia';
UPDATE usuarios SET password = 'profesor123' WHERE username = 'patricia.fernandez';
UPDATE usuarios SET password = 'profesor123' WHERE username = 'jorge.mendoza';
UPDATE usuarios SET password = 'profesor123' WHERE username = 'sandra.ponce';
UPDATE usuarios SET password = 'estudiante123' WHERE username = 'juan.perez';
UPDATE usuarios SET password = 'estudiante123' WHERE username = 'maria.gonzalez';
UPDATE usuarios SET password = 'estudiante123' WHERE username = 'carlos.rodriguez';
UPDATE usuarios SET password = 'estudiante123' WHERE username = 'ana.martinez';
UPDATE usuarios SET password = 'estudiante123' WHERE username = 'luis.lopez';

-- Verificar que las contraseñas se actualizaron correctamente
SELECT username, password, rol FROM usuarios;
