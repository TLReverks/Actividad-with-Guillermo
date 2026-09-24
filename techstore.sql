-- ============================================================
-- TechStore - Script de base de datos
-- ============================================================

CREATE DATABASE IF NOT EXISTS techstore DEFAULT CHARACTER SET = 'utf8mb4';

USE techstore;

-- ------------------------------------------------------------
-- Tabla usuarios
-- ------------------------------------------------------------
CREATE TABLE usuarios(
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(80) NOT NULL,
    correo VARCHAR(100) UNIQUE NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    password VARCHAR(255) NOT NULL,
    rol ENUM('Administrador','Cliente') DEFAULT 'Cliente',
    estado ENUM('Activo','Inactivo') DEFAULT 'Activo'
);

-- Usuarios administradores (contraseñas guardadas encriptadas con
-- werkzeug.security.generate_password_hash, método pbkdf2:sha256)
-- Admin 1 -> correo: admin1@techstore.com | contraseña: admin123
-- Admin 2 -> correo: admin2@techstore.com | contraseña: admin456
INSERT INTO usuarios (nombre, correo, telefono, password, rol, estado) VALUES
('Administrador Uno', 'admin1@techstore.com', '3000000001',
 'pbkdf2:sha256:1000000$JH2Yu89HrjTKGnac$1f331609463a3c71170555e223b15200552f4935becbe6222fc72f7c058e22a2',
 'Administrador', 'Activo'),
('Administrador Dos', 'admin2@techstore.com', '3000000002',
 'pbkdf2:sha256:1000000$LMGQwi4BTCjEskkG$47bb476ce72ee6f33dbe41d2a72e3fcf0639b5958050acfe0a4b7cb9dab84ce5',
 'Administrador', 'Activo');

-- ------------------------------------------------------------
-- Tabla productos
-- ------------------------------------------------------------
CREATE TABLE productos(
    codigo VARCHAR(20) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    precio DECIMAL(12,2) NOT NULL,
    categoria VARCHAR(50),
    imagen VARCHAR(255)
);

INSERT INTO productos (codigo, nombre, precio, categoria, imagen) VALUES
('P001','Laptop Lenovo',3500000,'Computadores', NULL),
('P002','Mouse Logitech',85000,'Accesorios', NULL),
('P003','Monitor Samsung',890000,'Monitores', NULL),
('P004','Portátil Lenovo IdeaPad 3', 2850000, 'Computadores', NULL);

SELECT * FROM usuarios;
SELECT * FROM productos;

-- ============================================================
-- Migración para una base de datos ya existente (estructura
-- anterior). Ejecutar solo si la tabla usuarios/productos ya
-- existía con la estructura antigua y no se va a recrear desde
-- cero con el script de arriba.
-- ============================================================
-- ALTER TABLE usuarios ADD telefono VARCHAR(20) NOT NULL;
-- ALTER TABLE usuarios MODIFY rol ENUM('Administrador','Cliente') DEFAULT 'Cliente';
-- ALTER TABLE productos ADD imagen VARCHAR(255);
