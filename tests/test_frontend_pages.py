"""Test rendering halaman frontend pada Flask app."""

import os
from importlib import util
from pathlib import Path

import pytest


ROOT_DIR = Path(__file__).resolve().parents[1]
FRONTEND_APP_PATH = ROOT_DIR / "src" / "frontend" / "app.py"


@pytest.fixture(scope="module")
def frontend_client():
    """Memuat app frontend dari file dan mengembalikan test client."""
    original_cwd = Path.cwd()
    os.chdir(FRONTEND_APP_PATH.parent)

    spec = util.spec_from_file_location("dompetku_frontend_app", FRONTEND_APP_PATH)
    module = util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    spec.loader.exec_module(module)

    module.app.config["TESTING"] = True
    try:
        with module.app.test_client() as client:
            yield client
    finally:
        os.chdir(original_cwd)


@pytest.mark.parametrize(
    "route, expected_text",
    [
        ("/", "Transaksi Terbaru"),
        ("/dashboard", "Transaksi Terbaru"),
        ("/login", "Login Dompetku"),
        ("/register", "Daftar Akun Dompetku"),
        ("/pemasukan", "Daftar Pemasukan"),
        ("/pengeluaran", "Daftar Pengeluaran"),
        ("/kategori", "Daftar Kategori"),
        ("/rekap", "Rekap Keuangan Bulanan"),
    ],
)
def test_frontend_pages_render_success(frontend_client, route, expected_text):
    """Semua halaman utama frontend harus bisa dirender dengan status 200."""
    response = frontend_client.get(route)

    assert response.status_code == 200
    assert expected_text in response.get_data(as_text=True)
