-- Seed user awal untuk kebutuhan development/testing autentikasi
USE dompetku;

-- Kredensial default:
-- username: admin
-- password: admin123
INSERT INTO users (username, password_hash, is_active)
SELECT
    'admin',
    'pbkdf2:sha256:600000$xFhA4jN3y5WszFO7$22fa16e98dc5847158e72814f2d5576c66a5f21ec4d1bdefe99ce64cb3444a6c',
    TRUE
WHERE NOT EXISTS (
    SELECT 1 FROM users WHERE username = 'admin'
);
