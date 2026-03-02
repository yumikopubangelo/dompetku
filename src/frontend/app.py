# ====================================================
# app.py
# Aplikasi Flask untuk frontend website keuangan pribadi
# Berfungsi untuk merender halaman-halaman HTML
# Setiap halaman akan memanggil API backend menggunakan JavaScript
# ====================================================

from flask import Flask, render_template
import os

# Inisialisasi aplikasi Flask
app = Flask(
    __name__,
    template_folder='.',
    static_folder='assets',
    static_url_path='/static'
)

# Konfigurasi (bisa diambil dari environment variable)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-ubah-di-production')
app.config['API_BASE_URL'] = os.environ.get('API_BASE_URL', 'http://localhost:5000/api')  # URL backend

# Context processor untuk membuat variabel tersedia di semua template
@app.context_processor
def inject_config():
    return dict(API_BASE_URL=app.config['API_BASE_URL'])

# ====================================================
# ROUTING UNTUK HALAMAN
# ====================================================

@app.route('/')
@app.route('/dashboard')
def dashboard():
    """
    Halaman utama dashboard.
    Menampilkan ringkasan statistik dan saldo.
    """
    return render_template('pages/dashboard.html')

@app.route('/login')
def login():
    """
    Halaman login user.
    """
    return render_template('pages/login.html')

@app.route('/register')
def register():
    """
    Halaman registrasi user baru.
    """
    return render_template('pages/register.html')

@app.route('/pemasukan')
def pemasukan():
    """
    Halaman manajemen pemasukan.
    Menampilkan daftar pemasukan, form tambah/edit.
    """
    return render_template('pages/pemasukan.html')

@app.route('/pengeluaran')
def pengeluaran():
    """
    Halaman manajemen pengeluaran.
    Menampilkan daftar pengeluaran, form tambah/edit.
    """
    return render_template('pages/pengeluaran.html')

@app.route('/kategori')
def kategori():
    """
    Halaman manajemen kategori.
    Menampilkan daftar kategori, form tambah.
    """
    return render_template('pages/kategori.html')

@app.route('/rekap')
def rekap():
    """
    Halaman rekap bulanan.
    Menampilkan rekap keuangan berdasarkan bulan dan tahun.
    """
    return render_template('pages/rekap.html')


@app.route('/login')
def login():
    """Halaman login frontend."""
    return render_template('pages/login.html')


@app.route('/register')
def register():
    """Halaman registrasi frontend."""
    return render_template('pages/register.html')

# ====================================================
# MENJALANKAN APLIKASI
# ====================================================
if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Jalankan di port 5001 untuk Menghindari konflik dengan backend Docker
