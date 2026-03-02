"""Frontend component tests (static contract checks)."""

from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[2]
COMPONENTS_DIR = ROOT_DIR / "src" / "frontend" / "components"


def _read(name: str) -> str:
    return (COMPONENTS_DIR / name).read_text(encoding="utf-8")


def test_component_files_exist():
    required = ["header.html", "footer.html", "modal.html", "alerts.html"]

    for name in required:
        component_path = COMPONENTS_DIR / name
        assert component_path.exists(), f"Missing component file: {component_path}"


def test_header_contains_nav_and_runtime_hooks():
    content = _read("header.html")

    assert "id=\"authUserLabel\"" in content
    assert "id=\"saldoHeader\"" in content
    assert "logoutSession()" in content
    assert "function renderCurrentUser()" in content
    assert "async function updateSaldo()" in content

    for route in ["/dashboard", "/pemasukan", "/pengeluaran", "/kategori", "/rekap"]:
        assert f"href=\"{route}\"" in content


def test_modal_contains_required_form_and_handlers():
    content = _read("modal.html")

    assert "id=\"modal\"" in content
    assert "id=\"modalForm\"" in content
    assert "id=\"formFields\"" in content
    assert "function openModal(type, id = null)" in content
    assert "function closeModal()" in content
    assert "async function saveData()" in content
    assert "async function loadKategoriOptions(tipe)" in content


def test_alerts_component_exposes_alert_container_and_function():
    content = _read("alerts.html")

    assert "id=\"alert\"" in content
    assert "function showAlert(message, type = 'success')" in content


def test_footer_contains_dompetku_branding():
    content = _read("footer.html")

    assert "Dompetku" in content
    assert "Aplikasi Keuangan Pribadi" in content
