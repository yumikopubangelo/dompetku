"""Unit test untuk fitur Kategori (service + route)."""

from types import SimpleNamespace

import src.backend.services.kategori_service as kategori_service


# Spy sederhana untuk memantau interaksi ke db.session tanpa database asli.
class SessionSpy:
    def __init__(self, fail_on_commit=False):
        self.fail_on_commit = fail_on_commit
        self.added = []
        self.deleted = []
        self.committed = False
        self.rolled_back = False

    def add(self, obj):
        self.added.append(obj)

    def delete(self, obj):
        self.deleted.append(obj)

    def commit(self):
        if self.fail_on_commit:
            raise RuntimeError("commit gagal")
        self.committed = True

    def rollback(self):
        self.rolled_back = True


def _build_kategori_client(flask_app):
    """Mendaftarkan blueprint kategori ke app test dan mengembalikan test client."""
    from src.backend.routes.kategori import kategori_bp

    flask_app.register_blueprint(kategori_bp, url_prefix="/api/kategori")
    return flask_app.test_client()


# ---------- Service tests ----------
# Test user_id for all service calls
TEST_USER_ID = 1


def test_get_kategori_service_success(monkeypatch):
    rows = [
        SimpleNamespace(id=1, nama="Gaji", tipe="pemasukan", created_at="2026-02-01"),
        SimpleNamespace(id=2, nama="Makan", tipe="pengeluaran", created_at="2026-02-02"),
    ]

    class DummyQuery:
        def all(self):
            return rows

        def filter_by(self, user_id=None):
            return DummyQuery()

    monkeypatch.setattr(kategori_service, "Kategori", SimpleNamespace(query=DummyQuery()))

    result = kategori_service.get_kategori(TEST_USER_ID)

    assert len(result) == 2
    assert result[0]["nama"] == "Gaji"
    assert result[1]["tipe"] == "pengeluaran"


def test_get_kategori_service_returns_empty_list_on_error(monkeypatch):
    class DummyQuery:
        def all(self):
            raise RuntimeError("database error")

        def filter_by(self, user_id=None):
            return DummyQuery()

    monkeypatch.setattr(kategori_service, "Kategori", SimpleNamespace(query=DummyQuery()))

    assert kategori_service.get_kategori(TEST_USER_ID) == []


def test_create_kategori_service_success(monkeypatch):
    session = SessionSpy()
    monkeypatch.setattr(kategori_service, "db", SimpleNamespace(session=session))

    # Dummy model meniru object ORM yang dibuat oleh service.
    class DummyKategori:
        def __init__(self, nama, tipe, user_id=None):
            self.id = 10
            self.nama = nama
            self.tipe = tipe
            self.user_id = user_id
            self.created_at = "2026-02-10"

    monkeypatch.setattr(kategori_service, "Kategori", DummyKategori)

    payload = {"nama": "Bonus", "tipe": "pemasukan"}
    result = kategori_service.create_kategori(payload, TEST_USER_ID)

    assert session.committed is True
    assert session.added[0].nama == "Bonus"
    assert result["id"] == 10


def test_create_kategori_service_rollback_on_error(monkeypatch):
    session = SessionSpy(fail_on_commit=True)
    monkeypatch.setattr(kategori_service, "db", SimpleNamespace(session=session))

    class DummyKategori:
        def __init__(self, nama, tipe, user_id=None):
            self.id = 11
            self.nama = nama
            self.tipe = tipe
            self.user_id = user_id
            self.created_at = "2026-02-10"

    monkeypatch.setattr(kategori_service, "Kategori", DummyKategori)

    result = kategori_service.create_kategori({"nama": "Freelance", "tipe": "pemasukan"}, TEST_USER_ID)

    assert result is None
    assert session.rolled_back is True


def test_update_kategori_service_success(monkeypatch):
    current = SimpleNamespace(id=3, nama="Lama", tipe="pemasukan", created_at="2026-02-11")

    class DummyQuery:
        def filter_by(self, id=None, user_id=None):
            return self

        def first(self):
            return current

    session = SessionSpy()
    monkeypatch.setattr(kategori_service, "Kategori", SimpleNamespace(query=DummyQuery()))
    monkeypatch.setattr(kategori_service, "db", SimpleNamespace(session=session))

    result = kategori_service.update_kategori(3, {"nama": "Baru", "tipe": "pengeluaran"}, TEST_USER_ID)

    assert session.committed is True
    assert result["nama"] == "Baru"
    assert result["tipe"] == "pengeluaran"


def test_update_kategori_service_not_found(monkeypatch):
    class DummyQuery:
        def filter_by(self, id=None, user_id=None):
            return self

        def first(self):
            return None

    session = SessionSpy()
    monkeypatch.setattr(kategori_service, "Kategori", SimpleNamespace(query=DummyQuery()))
    monkeypatch.setattr(kategori_service, "db", SimpleNamespace(session=session))

    assert kategori_service.update_kategori(99, {"nama": "Tidak Ada"}, TEST_USER_ID) is None
    assert session.committed is False


def test_delete_kategori_service_success(monkeypatch):
    current = SimpleNamespace(id=4, nama="Transport", tipe="pengeluaran", created_at="2026-02-11")

    class DummyQuery:
        def filter_by(self, id=None, user_id=None):
            return self

        def first(self):
            return current

    session = SessionSpy()
    monkeypatch.setattr(kategori_service, "Kategori", SimpleNamespace(query=DummyQuery()))
    monkeypatch.setattr(kategori_service, "db", SimpleNamespace(session=session))

    assert kategori_service.delete_kategori(4, TEST_USER_ID) is True
    assert session.committed is True
    assert session.deleted == [current]


def test_delete_kategori_service_not_found(monkeypatch):
    class DummyQuery:
        def filter_by(self, id=None, user_id=None):
            return self

        def first(self):
            return None

    session = SessionSpy()
    monkeypatch.setattr(kategori_service, "Kategori", SimpleNamespace(query=DummyQuery()))
    monkeypatch.setattr(kategori_service, "db", SimpleNamespace(session=session))

    assert kategori_service.delete_kategori(404, TEST_USER_ID) is False
    assert session.committed is False


# ---------- Route tests ----------
def test_get_kategori_route_returns_200(flask_app, bypass_jwt, monkeypatch):
    import src.backend.routes.kategori as kategori_route

    monkeypatch.setattr(kategori_route, "get_kategori", lambda user_id: [{"id": 1, "nama": "Gaji"}])
    client = _build_kategori_client(flask_app)

    resp = client.get("/api/kategori/")

    assert resp.status_code == 200
    assert resp.get_json()[0]["nama"] == "Gaji"


def test_create_kategori_route_returns_400_for_empty_payload(flask_app, bypass_jwt):
    client = _build_kategori_client(flask_app)

    resp = client.post("/api/kategori/", json={})

    assert resp.status_code == 400
    assert resp.get_json()["error"] == "No data provided"


def test_create_kategori_route_returns_201(flask_app, bypass_jwt, monkeypatch):
    import src.backend.routes.kategori as kategori_route

    monkeypatch.setattr(
        kategori_route,
        "create_kategori",
        lambda data, user_id: {"id": 5, "nama": data["nama"], "tipe": data["tipe"]},
    )
    client = _build_kategori_client(flask_app)

    resp = client.post("/api/kategori/", json={"nama": "Investasi", "tipe": "pemasukan"})

    assert resp.status_code == 201
    assert resp.get_json()["nama"] == "Investasi"


def test_update_kategori_route_returns_404_when_not_found(flask_app, bypass_jwt, monkeypatch):
    import src.backend.routes.kategori as kategori_route

    monkeypatch.setattr(kategori_route, "update_kategori", lambda _id, _data, _user_id: None)
    client = _build_kategori_client(flask_app)

    resp = client.put("/api/kategori/99", json={"nama": "Update"})

    assert resp.status_code == 404
    assert resp.get_json()["error"] == "Kategori not found"


def test_delete_kategori_route_returns_200(flask_app, bypass_jwt, monkeypatch):
    import src.backend.routes.kategori as kategori_route

    monkeypatch.setattr(kategori_route, "delete_kategori", lambda _id, _user_id: True)
    client = _build_kategori_client(flask_app)

    resp = client.delete("/api/kategori/7")

    assert resp.status_code == 200
    assert resp.get_json()["message"] == "Kategori deleted successfully"

