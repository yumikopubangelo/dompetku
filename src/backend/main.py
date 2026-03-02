"""Entry point backend Dompetku."""

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from sqlalchemy import inspect, text
from config import DB_CONFIG, APP_PORT, APP_DEBUG, SECRET_KEY, db

# Membuat instance aplikasi Flask.
app = Flask(__name__)

# Mengaktifkan CORS agar API dapat diakses dari domain frontend lain.
CORS(app)

# Menyusun URL koneksi SQLAlchemy dari konfigurasi environment.
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@"
    f"{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
)

# Menonaktifkan tracking perubahan objek untuk mengurangi overhead.
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Secret key dipakai oleh JWT untuk proses sign/verify token.
app.config["JWT_SECRET_KEY"] = SECRET_KEY

# Inisialisasi extension yang dipakai di seluruh aplikasi.
db.init_app(app)
jwt = JWTManager(app)

# Import blueprint setelah app dibuat agar dependensi ter-load dengan benar.
from routes.auth import auth_bp
from routes.kategori import kategori_bp
from routes.pemasukan import pemasukan_bp
from routes.pengeluaran import pengeluaran_bp
from routes.rekap import rekap_bp
from routes.saldo import saldo_bp
from routes.statistik import statistik_bp
from services.auth_service import is_token_revoked

# Registrasi semua endpoint API per domain fitur.
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(kategori_bp, url_prefix="/api/kategori")
app.register_blueprint(pemasukan_bp, url_prefix="/api/pemasukan")
app.register_blueprint(pengeluaran_bp, url_prefix="/api/pengeluaran")
app.register_blueprint(rekap_bp, url_prefix="/api/rekap")
app.register_blueprint(saldo_bp, url_prefix="/api/saldo")
app.register_blueprint(statistik_bp, url_prefix="/api/statistik")


def initialize_database():
    """Memastikan seluruh tabel model tersedia sebelum request pertama diproses."""
    with app.app_context():
        # Import model di sini agar metadata SQLAlchemy lengkap saat create_all dieksekusi.
        import models  # noqa: F401
        db.create_all()


initialize_database()


def sync_legacy_schema():
    """Menambahkan kolom wajib yang mungkin belum ada pada database lama."""
    with app.app_context():
        inspector = inspect(db.engine)
        required_columns = {
            "kategori": {"user_id"},
            "pemasukan": {"user_id"},
            "pengeluaran": {"user_id"},
        }

        for table_name, columns in required_columns.items():
            if not inspector.has_table(table_name):
                continue

            existing_columns = {col["name"] for col in inspector.get_columns(table_name)}
            missing_columns = columns - existing_columns

            for column_name in missing_columns:
                # Kompatibilitas untuk schema lama tanpa kolom multi-user.
                db.session.execute(
                    text(f"ALTER TABLE {table_name} ADD COLUMN {column_name} INT NULL")
                )

        db.session.commit()


sync_legacy_schema()


@jwt.token_in_blocklist_loader
def check_if_token_revoked(_jwt_header, jwt_payload):
    """Hook JWT untuk memblokir token yang sudah di-logout."""
    return is_token_revoked(jwt_payload["jti"])


@app.route("/")
def home():
    """Health endpoint sederhana untuk memastikan API hidup."""
    return "Dompetku API is running!"


if __name__ == "__main__":
    # Menjalankan server Flask saat file dieksekusi langsung.
    app.run(host="0.0.0.0", port=APP_PORT, debug=APP_DEBUG)
