"""Unit test untuk fitur Pengeluaran (service + route)."""

from types import SimpleNamespace

import services.pengeluaran_service as pengeluaran_service


# Spy session untuk mensimulasikan perilaku transaksi database.
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


def _build_pengeluaran_client(flask_app):
    """Mendaftarkan blueprint pengeluaran ke app test."""
    from routes.pengeluaran import pengeluaran_bp

    flask_app.register_blueprint(pengeluaran_bp, url_prefix="/api/pengeluaran")
    return flask_app.test_client()


# ---------- Service tests ----------
def test_get_pengeluaran_service_success(monkeypatch):
    rows = [
        SimpleNamespace(
            id=1,
            jumlah=25000,
            deskripsi="Makan siang",
            kategori_id=9,
            tanggal="2026-02-01",
            created_at="2026-02-01",
        )
    ]

    class DummyQuery:
        def all(self):
            return rows

    monkeypatch.setattr(pengeluaran_service, "Pengeluaran", SimpleNamespace(query=DummyQuery()))

    result = pengeluaran_service.get_pengeluaran()

    assert len(result) == 1
    assert result[0]["jumlah"] == "25000"
    assert result[0]["deskripsi"] == "Makan siang"


def test_get_pengeluaran_service_returns_empty_list_on_error(monkeypatch):
    class DummyQuery:
        def all(self):
            raise RuntimeError("database error")

    monkeypatch.setattr(pengeluaran_service, "Pengeluaran", SimpleNamespace(query=DummyQuery()))

    assert pengeluaran_service.get_pengeluaran() == []


def test_create_pengeluaran_service_success(monkeypatch):
    session = SessionSpy()
    monkeypatch.setattr(pengeluaran_service, "db", SimpleNamespace(session=session))

    class DummyPengeluaran:
        def __init__(self, jumlah, deskripsi=None, kategori_id=None, tanggal=None):
            self.id = 20
            self.jumlah = jumlah
            self.deskripsi = deskripsi
            self.kategori_id = kategori_id
            self.tanggal = tanggal
            self.created_at = "2026-02-01"

    monkeypatch.setattr(pengeluaran_service, "Pengeluaran", DummyPengeluaran)

    payload = {"jumlah": 120000, "deskripsi": "Belanja", "kategori_id": 4, "tanggal": "2026-02-01"}
    result = pengeluaran_service.create_pengeluaran(payload)

    assert session.committed is True
    assert result["id"] == 20
    assert result["jumlah"] == "120000"


def test_create_pengeluaran_service_rollback_on_error(monkeypatch):
    session = SessionSpy(fail_on_commit=True)
    monkeypatch.setattr(pengeluaran_service, "db", SimpleNamespace(session=session))

    class DummyPengeluaran:
        def __init__(self, jumlah, deskripsi=None, kategori_id=None, tanggal=None):
            self.id = 21
            self.jumlah = jumlah
            self.deskripsi = deskripsi
            self.kategori_id = kategori_id
            self.tanggal = tanggal
            self.created_at = "2026-02-02"

    monkeypatch.setattr(pengeluaran_service, "Pengeluaran", DummyPengeluaran)

    result = pengeluaran_service.create_pengeluaran({"jumlah": 1, "tanggal": "2026-02-01"})

    assert result is None
    assert session.rolled_back is True


def test_update_pengeluaran_service_success(monkeypatch):
    current = SimpleNamespace(
        id=8,
        jumlah=10000,
        deskripsi="Lama",
        kategori_id=1,
        tanggal="2026-02-01",
        created_at="2026-02-01",
    )

    class DummyQuery:
        def get(self, _id):
            return current

    session = SessionSpy()
    monkeypatch.setattr(pengeluaran_service, "Pengeluaran", SimpleNamespace(query=DummyQuery()))
    monkeypatch.setattr(pengeluaran_service, "db", SimpleNamespace(session=session))

    result = pengeluaran_service.update_pengeluaran(
        8,
        {"jumlah": 33000, "deskripsi": "Baru", "kategori_id": 6, "tanggal": "2026-02-03"},
    )

    assert session.committed is True
    assert result["jumlah"] == "33000"
    assert result["deskripsi"] == "Baru"


def test_update_pengeluaran_service_not_found(monkeypatch):
    class DummyQuery:
        def get(self, _id):
            return None

    session = SessionSpy()
    monkeypatch.setattr(pengeluaran_service, "Pengeluaran", SimpleNamespace(query=DummyQuery()))
    monkeypatch.setattr(pengeluaran_service, "db", SimpleNamespace(session=session))

    assert pengeluaran_service.update_pengeluaran(404, {"jumlah": 1}) is None
    assert session.committed is False


def test_delete_pengeluaran_service_success(monkeypatch):
    current = SimpleNamespace(id=2)

    class DummyQuery:
        def get(self, _id):
            return current

    session = SessionSpy()
    monkeypatch.setattr(pengeluaran_service, "Pengeluaran", SimpleNamespace(query=DummyQuery()))
    monkeypatch.setattr(pengeluaran_service, "db", SimpleNamespace(session=session))

    assert pengeluaran_service.delete_pengeluaran(2) is True
    assert session.deleted == [current]
    assert session.committed is True


def test_delete_pengeluaran_service_not_found(monkeypatch):
    class DummyQuery:
        def get(self, _id):
            return None

    session = SessionSpy()
    monkeypatch.setattr(pengeluaran_service, "Pengeluaran", SimpleNamespace(query=DummyQuery()))
    monkeypatch.setattr(pengeluaran_service, "db", SimpleNamespace(session=session))

    assert pengeluaran_service.delete_pengeluaran(999) is False
    assert session.committed is False


# ---------- Route tests ----------
def test_get_pengeluaran_route_returns_200(flask_app, bypass_jwt, monkeypatch):
    import routes.pengeluaran as pengeluaran_route

    monkeypatch.setattr(pengeluaran_route, "get_pengeluaran", lambda: [{"id": 1, "jumlah": "100"}])
    client = _build_pengeluaran_client(flask_app)

    resp = client.get("/api/pengeluaran/")

    assert resp.status_code == 200
    assert resp.get_json()[0]["jumlah"] == "100"


def test_create_pengeluaran_route_returns_400_for_empty_payload(flask_app, bypass_jwt):
    client = _build_pengeluaran_client(flask_app)

    resp = client.post("/api/pengeluaran/", json={})

    assert resp.status_code == 400
    assert resp.get_json()["error"] == "No data provided"


def test_create_pengeluaran_route_returns_201(flask_app, bypass_jwt, monkeypatch):
    import routes.pengeluaran as pengeluaran_route

    monkeypatch.setattr(
        pengeluaran_route,
        "create_pengeluaran",
        lambda data: {"id": 9, "jumlah": str(data["jumlah"]), "tanggal": data["tanggal"]},
    )
    client = _build_pengeluaran_client(flask_app)

    resp = client.post("/api/pengeluaran/", json={"jumlah": 70000, "tanggal": "2026-02-01"})

    assert resp.status_code == 201
    assert resp.get_json()["id"] == 9


def test_update_pengeluaran_route_returns_404_when_not_found(flask_app, bypass_jwt, monkeypatch):
    import routes.pengeluaran as pengeluaran_route

    monkeypatch.setattr(pengeluaran_route, "update_pengeluaran", lambda _id, _data: None)
    client = _build_pengeluaran_client(flask_app)

    resp = client.put("/api/pengeluaran/123", json={"jumlah": 1000})

    assert resp.status_code == 404
    assert resp.get_json()["error"] == "Pengeluaran not found"


def test_delete_pengeluaran_route_returns_200(flask_app, bypass_jwt, monkeypatch):
    import routes.pengeluaran as pengeluaran_route

    monkeypatch.setattr(pengeluaran_route, "delete_pengeluaran", lambda _id: True)
    client = _build_pengeluaran_client(flask_app)

    resp = client.delete("/api/pengeluaran/10")

    assert resp.status_code == 200
    assert resp.get_json()["message"] == "Pengeluaran deleted successfully"
