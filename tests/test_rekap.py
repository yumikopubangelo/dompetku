"""Unit test untuk fitur Rekap Bulanan (service + route)."""

from types import SimpleNamespace

import pytest
import src.backend.services.rekap_service as rekap_service


# Field palsu agar ekspresi `label()` pada query bisa dipanggil.
class LabelField:
    def label(self, _name):
        return self


class FakeFunc:
    """Meniru subset fungsi SQL (`sum`, `month`, `year`) yang dipakai service."""

    def sum(self, _value):
        return LabelField()

    def month(self, _value):
        return 1

    def year(self, _value):
        return 2026


class QueryResult:
    """Objek query chainable untuk `join -> filter -> group_by -> all/scalar`."""

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
    """Mengembalikan objek query sesuai urutan pemanggilan service."""

    def __init__(self, queries):
        self.queries = list(queries)
        self.index = 0

    def query(self, *_args, **_kwargs):
        if self.index >= len(self.queries):
            raise AssertionError("Jumlah query melebihi skenario test")
        query_obj = self.queries[self.index]
        self.index += 1
        return query_obj


def _build_rekap_client(flask_app):
    """Mendaftarkan blueprint rekap ke app test."""
    from src.backend.routes.rekap import rekap_bp

    flask_app.register_blueprint(rekap_bp, url_prefix="/api/rekap")
    return flask_app.test_client()


# ---------- Service tests ----------
def test_get_rekap_bulanan_service_success(monkeypatch):
    pemasukan_rows = [SimpleNamespace(kategori="Gaji", total=5000000)]
    pengeluaran_rows = [SimpleNamespace(kategori="Makan", total=1500000)]
    session = SequenceSession(
        [
            QueryResult(rows=pemasukan_rows),
            QueryResult(rows=pengeluaran_rows),
            QueryResult(scalar_value=5000000),
            QueryResult(scalar_value=1500000),
        ]
    )

    fake_db = SimpleNamespace(session=session, func=FakeFunc())
    fake_kategori = SimpleNamespace(id=1, nama=LabelField(), tipe="pemasukan")
    fake_pemasukan = SimpleNamespace(jumlah="jumlah", tanggal="tanggal", kategori_id="kategori_id")
    fake_pengeluaran = SimpleNamespace(jumlah="jumlah", tanggal="tanggal", kategori_id="kategori_id")

    monkeypatch.setattr(rekap_service, "db", fake_db)
    monkeypatch.setattr(rekap_service, "Kategori", fake_kategori)
    monkeypatch.setattr(rekap_service, "Pemasukan", fake_pemasukan)
    monkeypatch.setattr(rekap_service, "Pengeluaran", fake_pengeluaran)

    result = rekap_service.get_rekap_bulanan(2, 2026)

    assert result["bulan"] == 2
    assert result["tahun"] == 2026
    assert result["total_pemasukan"] == "5000000"
    assert result["total_pengeluaran"] == "1500000"
    assert result["saldo_akhir"] == "3500000"
    assert result["pemasukan_per_kategori"][0]["kategori"] == "Gaji"
    assert result["pengeluaran_per_kategori"][0]["kategori"] == "Makan"


def test_get_rekap_bulanan_service_raises_on_query_error(monkeypatch):
    class BrokenSession:
        def query(self, *_args, **_kwargs):
            raise RuntimeError("query gagal")

    fake_db = SimpleNamespace(session=BrokenSession(), func=FakeFunc())
    fake_kategori = SimpleNamespace(id=1, nama=LabelField(), tipe="pemasukan")
    fake_pemasukan = SimpleNamespace(jumlah="jumlah", tanggal="tanggal", kategori_id="kategori_id")
    fake_pengeluaran = SimpleNamespace(jumlah="jumlah", tanggal="tanggal", kategori_id="kategori_id")

    monkeypatch.setattr(rekap_service, "db", fake_db)
    monkeypatch.setattr(rekap_service, "Kategori", fake_kategori)
    monkeypatch.setattr(rekap_service, "Pemasukan", fake_pemasukan)
    monkeypatch.setattr(rekap_service, "Pengeluaran", fake_pengeluaran)

    with pytest.raises(RuntimeError, match="query gagal"):
        rekap_service.get_rekap_bulanan(2, 2026)


# ---------- Route tests ----------
def test_get_rekap_bulanan_route_returns_400_when_params_missing(flask_app, bypass_jwt):
    client = _build_rekap_client(flask_app)

    resp = client.get("/api/rekap/bulanan")

    assert resp.status_code == 400
    assert "wajib disediakan" in resp.get_json()["error"]


def test_get_rekap_bulanan_route_returns_200(flask_app, bypass_jwt, monkeypatch):
    import src.backend.routes.rekap as rekap_route

    monkeypatch.setattr(
        rekap_route,
        "get_rekap_bulanan",
        lambda bulan, tahun: {"bulan": bulan, "tahun": tahun, "saldo_akhir": "100000"},
    )
    client = _build_rekap_client(flask_app)

    resp = client.get("/api/rekap/bulanan?bulan=2&tahun=2026")

    assert resp.status_code == 200
    assert resp.get_json()["tahun"] == 2026


def test_get_rekap_bulanan_route_returns_500_on_invalid_number(flask_app, bypass_jwt):
    client = _build_rekap_client(flask_app)

    resp = client.get("/api/rekap/bulanan?bulan=abc&tahun=2026")

    assert resp.status_code == 500
    assert "invalid literal" in resp.get_json()["error"]


def test_get_rekap_bulanan_route_returns_500_when_service_error(flask_app, bypass_jwt, monkeypatch):
    import src.backend.routes.rekap as rekap_route

    def _raise_error(_bulan, _tahun):
        raise RuntimeError("service gagal")

    monkeypatch.setattr(rekap_route, "get_rekap_bulanan", _raise_error)
    client = _build_rekap_client(flask_app)

    resp = client.get("/api/rekap/bulanan?bulan=2&tahun=2026")

    assert resp.status_code == 500
    assert "service gagal" in resp.get_json()["error"]


