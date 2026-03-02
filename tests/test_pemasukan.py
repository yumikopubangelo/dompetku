"""Unit test untuk fitur Pemasukan (service + route)."""

from types import SimpleNamespace

import src.backend.services.pemasukan_service as pemasukan_service

# Test user_id for all service calls
TEST_USER_ID = 1


# Spy session untuk memverifikasi add/commit/delete/rollback pada service.
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


def _build_pemasukan_client(flask_app):
    """Mendaftarkan blueprint pemasukan ke app test."""
    from src.backend.routes.pemasukan import pemasukan_bp

    flask_app.register_blueprint(pemasukan_bp, url_prefix="/api/pemasukan")
    return flask_app.test_client()


# ---------- Service tests ----------
def test_get_pemasukan_service_success(monkeypatch):
    rows = [
        SimpleNamespace(
            id=1,
            jumlah=1500000,
            deskripsi="Gaji Bulanan",
            kategori_id=3,
            tanggal="2026-02-01",
            created_at="2026-02-01",
        )
    ]

    class DummyQuery:
        def all(self):
            return rows

        def filter_by(self, user_id=None):
            return DummyQuery()

    monkeypatch.setattr(pemasukan_service, "Pemasukan", SimpleNamespace(query=DummyQuery()))

    result = pemasukan_service.get_pemasukan(TEST_USER_ID)

    assert len(result) == 1
    assert result[0]["jumlah"] == "1500000"
    assert result[0]["deskripsi"] == "Gaji Bulanan"


def test_get_pemasukan_service_returns_empty_list_on_error(monkeypatch):
    class DummyQuery:
        def all(self):
            raise RuntimeError("database error")

        def filter_by(self, user_id=None):
            return DummyQuery()

    monkeypatch.setattr(pemasukan_service, "Pemasukan", SimpleNamespace(query=DummyQuery()))

    assert pemasukan_service.get_pemasukan(TEST_USER_ID) == []


def test_create_pemasukan_service_success(monkeypatch):
    session = SessionSpy()
    monkeypatch.setattr(pemasukan_service, "db", SimpleNamespace(session=session))

    class DummyPemasukan:
        def __init__(self, jumlah, deskripsi=None, kategori_id=None, tanggal=None, user_id=None):
            self.id = 10
            self.jumlah = jumlah
            self.deskripsi = deskripsi
            self.kategori_id = kategori_id
            self.tanggal = tanggal
            self.user_id = user_id
            self.created_at = "2026-02-01"

    monkeypatch.setattr(pemasukan_service, "Pemasukan", DummyPemasukan)

    payload = {"jumlah": 500000, "deskripsi": "Freelance", "kategori_id": 2, "tanggal": "2026-02-01"}
    result = pemasukan_service.create_pemasukan(payload, TEST_USER_ID)

    assert session.committed is True
    assert result["id"] == 10
    assert result["jumlah"] == "500000"


def test_create_pemasukan_service_rollback_on_error(monkeypatch):
    session = SessionSpy(fail_on_commit=True)
    monkeypatch.setattr(pemasukan_service, "db", SimpleNamespace(session=session))

    class DummyPemasukan:
        def __init__(self, jumlah, deskripsi=None, kategori_id=None, tanggal=None, user_id=None):
            self.id = 11
            self.jumlah = jumlah
            self.deskripsi = deskripsi
            self.kategori_id = kategori_id
            self.tanggal = tanggal
            self.user_id = user_id
            self.created_at = "2026-02-02"

    monkeypatch.setattr(pemasukan_service, "Pemasukan", DummyPemasukan)

    result = pemasukan_service.create_pemasukan({"jumlah": 1000, "tanggal": "2026-02-01"}, TEST_USER_ID)

    assert result is None
    assert session.rolled_back is True


def test_update_pemasukan_service_success(monkeypatch):
    current = SimpleNamespace(
        id=8,
        jumlah=100000,
        deskripsi="Lama",
        kategori_id=1,
        tanggal="2026-02-01",
        created_at="2026-02-01",
    )

    class DummyQuery:
        def filter_by(self, id=None, user_id=None):
            return self

        def first(self):
            return current

    session = SessionSpy()
    monkeypatch.setattr(pemasukan_service, "Pemasukan", SimpleNamespace(query=DummyQuery()))
    monkeypatch.setattr(pemasukan_service, "db", SimpleNamespace(session=session))

    result = pemasukan_service.update_pemasukan(
        8,
        {"jumlah": 250000, "deskripsi": "Baru", "kategori_id": 4, "tanggal": "2026-02-02"},
        TEST_USER_ID,
    )

    assert session.committed is True
    assert result["jumlah"] == "250000"
    assert result["deskripsi"] == "Baru"


def test_update_pemasukan_service_not_found(monkeypatch):
    class DummyQuery:
        def filter_by(self, id=None, user_id=None):
            return self

        def first(self):
            return None

    session = SessionSpy()
    monkeypatch.setattr(pemasukan_service, "Pemasukan", SimpleNamespace(query=DummyQuery()))
    monkeypatch.setattr(pemasukan_service, "db", SimpleNamespace(session=session))

    assert pemasukan_service.update_pemasukan(404, {"jumlah": 1}, TEST_USER_ID) is None
    assert session.committed is False


def test_delete_pemasukan_service_success(monkeypatch):
    current = SimpleNamespace(id=2)

    class DummyQuery:
        def filter_by(self, id=None, user_id=None):
            return self

        def first(self):
            return current

    session = SessionSpy()
    monkeypatch.setattr(pemasukan_service, "Pemasukan", SimpleNamespace(query=DummyQuery()))
    monkeypatch.setattr(pemasukan_service, "db", SimpleNamespace(session=session))

    assert pemasukan_service.delete_pemasukan(2, TEST_USER_ID) is True
    assert session.deleted == [current]
    assert session.committed is True


def test_delete_pemasukan_service_not_found(monkeypatch):
    class DummyQuery:
        def filter_by(self, id=None, user_id=None):
            return self

        def first(self):
            return None

    session = SessionSpy()
    monkeypatch.setattr(pemasukan_service, "Pemasukan", SimpleNamespace(query=DummyQuery()))
    monkeypatch.setattr(pemasukan_service, "db", SimpleNamespace(session=session))

    assert pemasukan_service.delete_pemasukan(999, TEST_USER_ID) is False
    assert session.committed is False


# ---------- Route tests ----------
def test_get_pemasukan_route_returns_200(flask_app, bypass_jwt, monkeypatch):
    import src.backend.routes.pemasukan as pemasukan_route

    monkeypatch.setattr(pemasukan_route, "get_pemasukan", lambda user_id: [{"id": 1, "jumlah": "100"}])
    client = _build_pemasukan_client(flask_app)

    resp = client.get("/api/pemasukan/")

    assert resp.status_code == 200
    assert resp.get_json()[0]["jumlah"] == "100"


def test_create_pemasukan_route_returns_400_for_empty_payload(flask_app, bypass_jwt):
    client = _build_pemasukan_client(flask_app)

    resp = client.post("/api/pemasukan/", json={})

    assert resp.status_code == 400
    assert resp.get_json()["error"] == "No data provided"


def test_create_pemasukan_route_returns_201(flask_app, bypass_jwt, monkeypatch):
    import src.backend.routes.pemasukan as pemasukan_route

    monkeypatch.setattr(
        pemasukan_route,
        "create_pemasukan",
        lambda data, user_id: {"id": 9, "jumlah": str(data["jumlah"]), "tanggal": data["tanggal"]},
    )
    client = _build_pemasukan_client(flask_app)

    resp = client.post("/api/pemasukan/", json={"jumlah": 70000, "tanggal": "2026-02-01"})

    assert resp.status_code == 201
    assert resp.get_json()["id"] == 9


def test_update_pemasukan_route_returns_404_when_not_found(flask_app, bypass_jwt, monkeypatch):
    import src.backend.routes.pemasukan as pemasukan_route

    monkeypatch.setattr(pemasukan_route, "update_pemasukan", lambda _id, _data, _user_id: None)
    client = _build_pemasukan_client(flask_app)

    resp = client.put("/api/pemasukan/123", json={"jumlah": 1000})

    assert resp.status_code == 404
    assert resp.get_json()["error"] == "Pemasukan not found"


def test_delete_pemasukan_route_returns_200(flask_app, bypass_jwt, monkeypatch):
    import src.backend.routes.pemasukan as pemasukan_route

    monkeypatch.setattr(pemasukan_route, "delete_pemasukan", lambda _id, _user_id: True)
    client = _build_pemasukan_client(flask_app)

    resp = client.delete("/api/pemasukan/10")

    assert resp.status_code == 200
    assert resp.get_json()["message"] == "Pemasukan deleted successfully"


