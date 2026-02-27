"""Konfigurasi global pytest untuk unit test backend Dompetku."""

from pathlib import Path
import sys

import pytest
from flask import Flask


# Pastikan folder `src/backend` bisa di-import sebagai module Python saat test berjalan.
BACKEND_DIR = Path(__file__).resolve().parents[1] / "src" / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))


@pytest.fixture
def flask_app():
    """Membuat Flask app minimal untuk mengetes blueprint route."""
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.config["JWT_SECRET_KEY"] = "test-secret"
    return app


@pytest.fixture
def bypass_jwt(monkeypatch):
    """Menonaktifkan verifikasi JWT agar route bisa diuji sebagai unit test."""
    monkeypatch.setattr(
        "flask_jwt_extended.view_decorators.verify_jwt_in_request",
        lambda *args, **kwargs: None,
    )
