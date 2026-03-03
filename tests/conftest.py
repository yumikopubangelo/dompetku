"""Konfigurasi global pytest untuk unit test backend Dompetku."""

from pathlib import Path
import sys

import pytest
from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token


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
    app.config["JWT_TOKEN_LOCATION"] = ["headers"]
    JWTManager(app)
    return app


@pytest.fixture
def bypass_jwt(monkeypatch):
    """Menonaktifkan verifikasi JWT agar route bisa diuji sebagai unit test."""
    from unittest.mock import MagicMock
    
    # Mock get_jwt to return a mock JWT with identity
    mock_jwt = MagicMock()
    mock_jwt.get.return_value = 1  # Return user_id for 'sub' claim
    
    # Patch verify_jwt_in_request to be a no-op
    import flask_jwt_extended.view_decorators as decorators
    monkeypatch.setattr(decorators, "verify_jwt_in_request", lambda *a, **kw: None)
    
    # Also patch get_jwt and get_jwt_identity
    import flask_jwt_extended.utils as utils
    monkeypatch.setattr(utils, "get_jwt_identity", lambda: 1)
    monkeypatch.setattr(utils, "get_jwt", lambda: mock_jwt)
