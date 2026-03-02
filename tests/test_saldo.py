"""Unit test untuk fitur Saldo (service + route)."""

from types import SimpleNamespace

import pytest
import src.backend.services.saldo_service as saldo_service

# Test user_id for all service calls
TEST_USER_ID = 1


# Query palsu untuk mengembalikan nilai aggregate scalar.
class ScalarQuery:
    def __init__(self, value):
        self.value = value

    def scalar(self):
        return self.value


# Session palsu yang mengeluarkan hasil query secara berurutan.
class SequenceSession:
    def __init__(self, values):
        self.values = list(values)
        self.index = 0

    def query(self, *_args, **_kwargs):
        if self.index >= len(self.values):
            raise AssertionError("Jumlah query melebihi skenario test")
        value = self.values[self.index]
        self.index += 1
        return ScalarQuery(value)


class DummyFunc:
    def sum(self, _value):
        return "sum_expr"


def _build_saldo_client(flask_app):
    """Mendaftarkan blueprint saldo ke app test."""
    from src.backend.routes.saldo import saldo_bp

    flask_app.register_blueprint(saldo_bp, url_prefix="/api/saldo")
    return flask_app.test_client()


# ---------- Service tests ----------
def test_get_saldo_akhir_service_success(monkeypatch):
    session = SequenceSession([1000000, 250000])
    fake_db = SimpleNamespace(session=session, func=DummyFunc())

    monkeypatch.setattr(saldo_service, "db", fake_db)
    monkeypatch.setattr(saldo_service, "Pemasukan", SimpleNamespace(jumlah="jumlah_pemasukan"))
    monkeypatch.setattr(saldo_service, "Pengeluaran", SimpleNamespace(jumlah="jumlah_pengeluaran"))

    assert saldo_service.get_saldo_akhir(TEST_USER_ID) == 750000


def test_get_saldo_akhir_service_treats_none_as_zero(monkeypatch):
    session = SequenceSession([None, 125000])
    fake_db = SimpleNamespace(session=session, func=DummyFunc())

    monkeypatch.setattr(saldo_service, "db", fake_db)
    monkeypatch.setattr(saldo_service, "Pemasukan", SimpleNamespace(jumlah="jumlah_pemasukan"))
    monkeypatch.setattr(saldo_service, "Pengeluaran", SimpleNamespace(jumlah="jumlah_pengeluaran"))

    assert saldo_service.get_saldo_akhir(TEST_USER_ID) == -125000


def test_get_saldo_akhir_service_raises_on_query_error(monkeypatch):
    class BrokenSession:
        def query(self, *_args, **_kwargs):
            raise RuntimeError("query gagal")

    fake_db = SimpleNamespace(session=BrokenSession(), func=DummyFunc())
    monkeypatch.setattr(saldo_service, "db", fake_db)
    monkeypatch.setattr(saldo_service, "Pemasukan", SimpleNamespace(jumlah="jumlah_pemasukan"))
    monkeypatch.setattr(saldo_service, "Pengeluaran", SimpleNamespace(jumlah="jumlah_pengeluaran"))

    with pytest.raises(RuntimeError, match="query gagal"):
        saldo_service.get_saldo_akhir(TEST_USER_ID)


# ---------- Route tests ----------
def test_get_saldo_route_returns_200(flask_app, bypass_jwt, monkeypatch):
    import src.backend.routes.saldo as saldo_route

    monkeypatch.setattr(saldo_route, "get_saldo_akhir", lambda user_id: 888000)
    client = _build_saldo_client(flask_app)

    resp = client.get("/api/saldo/")

    assert resp.status_code == 200
    assert resp.get_json()["saldo_akhir"] == "888000"


def test_get_saldo_route_returns_500_when_service_error(flask_app, bypass_jwt, monkeypatch):
    import src.backend.routes.saldo as saldo_route

    def _raise_error(user_id):
        raise RuntimeError("service gagal")

    monkeypatch.setattr(saldo_route, "get_saldo_akhir", _raise_error)
    client = _build_saldo_client(flask_app)

    resp = client.get("/api/saldo/")

    assert resp.status_code == 500
    assert "service gagal" in resp.get_json()["error"]


