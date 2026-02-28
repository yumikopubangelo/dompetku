"""Unit test untuk fitur autentikasi dan util password."""

from types import SimpleNamespace

import src.backend.services.auth_service as auth_service
from src.backend.utils.password_utils import decrypt_password, hash_password, verify_password


def _build_auth_client(flask_app):
    """Mendaftarkan blueprint auth ke app test."""
    from src.backend.routes.auth import auth_bp

    flask_app.register_blueprint(auth_bp, url_prefix="/api/auth")
    return flask_app.test_client()


# ---------- Password util tests ----------
def test_hash_password_generates_hash_and_can_be_verified():
    hashed = hash_password("rahasia123")

    assert hashed != "rahasia123"
    assert verify_password("rahasia123", hashed) is True
    assert verify_password("salah", hashed) is False


def test_decrypt_password_alias_works_as_verify():
    hashed = hash_password("dompetku")

    # Fungsi ini memang alias verifikasi karena hash tidak bisa didekripsi.
    assert decrypt_password("dompetku", hashed) is True
    assert decrypt_password("wrong", hashed) is False


# ---------- Service tests ----------
def test_authenticate_user_success(monkeypatch):
    user_obj = SimpleNamespace(id=1, username="admin", is_active=True, password_hash=hash_password("admin123"))

    class DummyQuery:
        def filter_by(self, **_kwargs):
            return self

        def first(self):
            return user_obj

    monkeypatch.setattr(auth_service, "User", SimpleNamespace(query=DummyQuery()))

    result = auth_service.authenticate_user("admin", "admin123")

    assert result is user_obj


def test_authenticate_user_returns_none_when_password_invalid(monkeypatch):
    user_obj = SimpleNamespace(id=1, username="admin", is_active=True, password_hash=hash_password("admin123"))

    class DummyQuery:
        def filter_by(self, **_kwargs):
            return self

        def first(self):
            return user_obj

    monkeypatch.setattr(auth_service, "User", SimpleNamespace(query=DummyQuery()))

    assert auth_service.authenticate_user("admin", "salah") is None


def test_authenticate_user_returns_none_when_user_inactive(monkeypatch):
    user_obj = SimpleNamespace(id=1, username="admin", is_active=False, password_hash=hash_password("admin123"))

    class DummyQuery:
        def filter_by(self, **_kwargs):
            return self

        def first(self):
            return user_obj

    monkeypatch.setattr(auth_service, "User", SimpleNamespace(query=DummyQuery()))

    assert auth_service.authenticate_user("admin", "admin123") is None


def test_generate_auth_tokens(monkeypatch):
    user_obj = SimpleNamespace(id=7, username="joko")

    monkeypatch.setattr(auth_service, "create_access_token", lambda **_kwargs: "access-abc")
    monkeypatch.setattr(auth_service, "create_refresh_token", lambda **_kwargs: "refresh-xyz")

    tokens = auth_service.generate_auth_tokens(user_obj)

    assert tokens["access_token"] == "access-abc"
    assert tokens["refresh_token"] == "refresh-xyz"


def test_revoke_token_and_check_blocklist():
    jti = "test-jti-123"
    auth_service.REVOKED_TOKEN_JTI.discard(jti)

    assert auth_service.is_token_revoked(jti) is False
    auth_service.revoke_token(jti)
    assert auth_service.is_token_revoked(jti) is True


# ---------- Route tests ----------
def test_login_route_returns_400_when_payload_missing(flask_app):
    client = _build_auth_client(flask_app)

    resp = client.post("/api/auth/login", json={})

    assert resp.status_code == 400
    assert "wajib diisi" in resp.get_json()["error"]


def test_login_route_returns_401_when_credentials_invalid(flask_app, monkeypatch):
    import src.backend.routes.auth as auth_route

    monkeypatch.setattr(auth_route, "authenticate_user", lambda _u, _p: None)
    client = _build_auth_client(flask_app)

    resp = client.post("/api/auth/login", json={"username": "admin", "password": "salah"})

    assert resp.status_code == 401
    assert "salah" in resp.get_json()["error"]


def test_login_route_returns_200_when_credentials_valid(flask_app, monkeypatch):
    import src.backend.routes.auth as auth_route

    dummy_user = SimpleNamespace(id=10, username="admin")
    monkeypatch.setattr(auth_route, "authenticate_user", lambda _u, _p: dummy_user)
    monkeypatch.setattr(
        auth_route,
        "generate_auth_tokens",
        lambda _user: {"access_token": "access-ok", "refresh_token": "refresh-ok"},
    )
    client = _build_auth_client(flask_app)

    resp = client.post("/api/auth/login", json={"username": "admin", "password": "admin123"})

    assert resp.status_code == 200
    data = resp.get_json()
    assert data["access_token"] == "access-ok"
    assert data["refresh_token"] == "refresh-ok"
    assert data["user"]["username"] == "admin"


def test_logout_route_returns_200(flask_app, bypass_jwt, monkeypatch):
    import src.backend.routes.auth as auth_route

    captured = {}

    monkeypatch.setattr(auth_route, "get_jwt", lambda: {"jti": "jti-logout"})
    monkeypatch.setattr(auth_route, "revoke_token", lambda jti: captured.setdefault("jti", jti))
    client = _build_auth_client(flask_app)

    resp = client.post("/api/auth/logout")

    assert resp.status_code == 200
    assert resp.get_json()["message"] == "Logout berhasil"
    assert captured["jti"] == "jti-logout"
