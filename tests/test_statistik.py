"""Unit test untuk fitur Statistik Keuangan (service + route)."""

from types import SimpleNamespace

import pytest
import src.backend.services.statistik_service as statistik_service

# Test user_id for all service calls
TEST_USER_ID = 1


# Field palsu agar API `label()` bisa dipakai di ekspresi query SQLAlchemy.
class LabelField:
    def label(self, _name):
        return self


class FakeFunc:
    """Meniru fungsi SQL yang dipakai service statistik."""

    def sum(self, _value):
        return LabelField()

    def month(self, _value):
        return 1

    def year(self, _value):
        return 2026


class QueryResult:
    """Objek query chainable untuk skenario all/scalar."""

    def __init__(self, rows=None, scalar_value=None):
        self.rows = rows or []
        self.scalar_value = scalar_value

    def join(self, *_args, **_kwargs):
        return self

    def filter(self, *_args, **_kwargs):
        return self

    def group_by(self, *_args, **_kwargs):
        return self

    def all(self):
        return self.rows

    def scalar(self):
        return self.scalar_value


class SequenceSession:
    """Session yang mengeluarkan objek query sesuai urutan pemanggilan."""

    def __init__(self, queries):
        self.queries = list(queries)
        self.index = 0

    def query(self, *_args, **_kwargs):
        if self.index >= len(self.queries):
            raise AssertionError("Jumlah query melebihi skenario test")
        query_obj = self.queries[self.index]
        self.index += 1
        return query_obj


def _build_statistik_queries(
    monthly_income,
    monthly_expense,
    distribusi_pemasukan,
    distribusi_pengeluaran,
    total_pemasukan,
    total_pengeluaran,
):
    """Membuat urutan hasil query yang cocok dengan alur service statistik."""
    queries = []

    # Service melakukan 2 query scalar per bulan selama 12 bulan.
    for month in range(12):
        queries.append(QueryResult(scalar_value=monthly_income[month]))
        queries.append(QueryResult(scalar_value=monthly_expense[month]))

    # Setelah itu service mengambil distribusi kategori dan total tahunan.
    queries.append(QueryResult(rows=distribusi_pemasukan))
    queries.append(QueryResult(rows=distribusi_pengeluaran))
    queries.append(QueryResult(scalar_value=total_pemasukan))
    queries.append(QueryResult(scalar_value=total_pengeluaran))

    return queries


def _build_statistik_client(flask_app):
    """Mendaftarkan blueprint statistik ke app test."""
    from src.backend.routes.statistik import statistik_bp

    flask_app.register_blueprint(statistik_bp, url_prefix="/api/statistik")
    return flask_app.test_client()


def _patch_statistik_dependencies(monkeypatch, session):
    """Menyuntikkan dependency palsu untuk service statistik."""
    fake_db = SimpleNamespace(session=session, func=FakeFunc())
    fake_kategori = SimpleNamespace(id=1, nama=LabelField(), tipe="pemasukan")
    fake_pemasukan = SimpleNamespace(jumlah="jumlah", tanggal="tanggal", kategori_id="kategori_id")
    fake_pengeluaran = SimpleNamespace(jumlah="jumlah", tanggal="tanggal", kategori_id="kategori_id")

    monkeypatch.setattr(statistik_service, "db", fake_db)
    monkeypatch.setattr(statistik_service, "Kategori", fake_kategori)
    monkeypatch.setattr(statistik_service, "Pemasukan", fake_pemasukan)
    monkeypatch.setattr(statistik_service, "Pengeluaran", fake_pengeluaran)


# ---------- Service tests ----------
def test_get_statistik_keuangan_service_success(monkeypatch):
    monthly_income = [100000 * m for m in range(1, 13)]
    monthly_expense = [50000 * m for m in range(1, 13)]
    distribusi_pemasukan = [SimpleNamespace(kategori="Gaji", total=6000000)]
    distribusi_pengeluaran = [SimpleNamespace(kategori="Makan", total=2000000)]
    queries = _build_statistik_queries(
        monthly_income=monthly_income,
        monthly_expense=monthly_expense,
        distribusi_pemasukan=distribusi_pemasukan,
        distribusi_pengeluaran=distribusi_pengeluaran,
        total_pemasukan=7800000,
        total_pengeluaran=3900000,
    )
    session = SequenceSession(queries)
    _patch_statistik_dependencies(monkeypatch, session)

    result = statistik_service.get_statistik_keuangan(2026, TEST_USER_ID)

    assert result["tahun"] == 2026
    assert result["total_pemasukan"] == "7800000"
    assert result["total_pengeluaran"] == "3900000"
    assert result["total_saldo"] == "3900000"
    assert len(result["tren_bulanan"]) == 12
    assert result["tren_bulanan"][0]["bulan"] == 1
    assert result["tren_bulanan"][0]["pemasukan"] == "100000"
    assert result["distribusi_pemasukan"][0]["kategori"] == "Gaji"


def test_get_statistik_keuangan_service_uses_current_year_when_none(monkeypatch):
    # Patch datetime agar nilai tahun bisa dipastikan dan deterministic.
    class FakeDatetime:
        @staticmethod
        def now():
            return SimpleNamespace(year=2031)

    queries = _build_statistik_queries(
        monthly_income=[0] * 12,
        monthly_expense=[0] * 12,
        distribusi_pemasukan=[],
        distribusi_pengeluaran=[],
        total_pemasukan=0,
        total_pengeluaran=0,
    )
    session = SequenceSession(queries)
    _patch_statistik_dependencies(monkeypatch, session)
    monkeypatch.setattr(statistik_service, "datetime", FakeDatetime)

    result = statistik_service.get_statistik_keuangan(None, TEST_USER_ID)

    assert result["tahun"] == 2031


def test_get_statistik_keuangan_service_raises_on_error(monkeypatch):
    class BrokenSession:
        def query(self, *_args, **_kwargs):
            raise RuntimeError("query gagal")

    _patch_statistik_dependencies(monkeypatch, BrokenSession())

    with pytest.raises(RuntimeError, match="query gagal"):
        statistik_service.get_statistik_keuangan(2026, TEST_USER_ID)


# ---------- Route tests ----------
def test_get_statistik_route_returns_200(flask_app, bypass_jwt, monkeypatch):
    import src.backend.routes.statistik as statistik_route

    monkeypatch.setattr(
        statistik_route,
        "get_statistik_keuangan",
        lambda tahun=None, user_id=None: {"tahun": tahun, "total_saldo": "100000"},
    )
    client = _build_statistik_client(flask_app)

    resp = client.get("/api/statistik/?tahun=2026")

    assert resp.status_code == 200
    assert resp.get_json()["tahun"] == 2026


def test_get_statistik_route_passes_none_when_no_year(flask_app, bypass_jwt, monkeypatch):
    import src.backend.routes.statistik as statistik_route

    captured = {}

    def _fake_service(tahun=None, user_id=None):
        captured["tahun"] = tahun
        return {"tahun": 2030}

    monkeypatch.setattr(statistik_route, "get_statistik_keuangan", _fake_service)
    client = _build_statistik_client(flask_app)

    resp = client.get("/api/statistik/")

    assert resp.status_code == 200
    assert captured["tahun"] is None


def test_get_statistik_route_returns_500_on_invalid_year(flask_app, bypass_jwt):
    client = _build_statistik_client(flask_app)

    resp = client.get("/api/statistik/?tahun=bukan-angka")

    assert resp.status_code == 500
    assert "invalid literal" in resp.get_json()["error"]


def test_get_statistik_route_returns_500_when_service_error(flask_app, bypass_jwt, monkeypatch):
    import src.backend.routes.statistik as statistik_route

    def _raise_error(_tahun=None, _user_id=None):
        raise RuntimeError("service gagal")

    monkeypatch.setattr(statistik_route, "get_statistik_keuangan", _raise_error)
    client = _build_statistik_client(flask_app)

    resp = client.get("/api/statistik/?tahun=2026")

    assert resp.status_code == 500
    assert "service gagal" in resp.get_json()["error"]



