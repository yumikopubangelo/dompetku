<<<<<<< HEAD
# main.py - Entry point aplikasi backend Dompetku
# Jalankan file ini untuk memulai server

# TODO: Inisialisasi aplikasi di sini
=======
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config import DB_CONFIG, APP_PORT, APP_DEBUG, SECRET_KEY

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@"
    f"{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = SECRET_KEY

# Initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Import routes
# from routes.kategori import kategori_bp
# from routes.pemasukan import pemasukan_bp
# from routes.pengeluaran import pengeluaran_bp
# from routes.rekap import rekap_bp
# from routes.saldo import saldo_bp
# from routes.statistik import statistik_bp

# Register blueprints
# app.register_blueprint(kategori_bp, url_prefix='/api/kategori')
# app.register_blueprint(pemasukan_bp, url_prefix='/api/pemasukan')
# app.register_blueprint(pengeluaran_bp, url_prefix='/api/pengeluaran')
# app.register_blueprint(rekap_bp, url_prefix='/api/rekap')
# app.register_blueprint(saldo_bp, url_prefix='/api/saldo')
# app.register_blueprint(statistik_bp, url_prefix='/api/statistik')

@app.route('/')
def home():
    return "Dompetku API is running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=APP_PORT, debug=APP_DEBUG)
>>>>>>> 4631ec9 (chore: initialize project structure with src, tests, docs, and configuration)
