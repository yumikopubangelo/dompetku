"""Frontend asset tests (static contract checks)."""

from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[2]
FRONTEND_DIR = ROOT_DIR / "src" / "frontend"
ASSETS_DIR = FRONTEND_DIR / "assets"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_asset_files_exist():
    required = [
        ASSETS_DIR / "base.html",
        ASSETS_DIR / "style.css",
        ASSETS_DIR / "main.js",
    ]

    for file_path in required:
        assert file_path.exists(), f"Missing frontend asset file: {file_path}"


def test_base_template_loads_global_assets_and_components():
    content = _read(ASSETS_DIR / "base.html")

    assert "filename='style.css'" in content
    assert "filename='main.js'" in content
    assert "components/header.html" in content
    assert "components/alerts.html" in content
    assert "components/modal.html" in content
    assert "components/footer.html" in content


def test_main_js_contains_auth_and_api_helpers():
    content = _read(ASSETS_DIR / "main.js")

    expected_functions = [
        "function getApiBaseUrl()",
        "function buildApiUrl(path)",
        "function getCurrentUser()",
        "function isAuthenticated()",
        "async function apiFetch(path, options = {})",
        "async function logoutSession()",
    ]

    for fn in expected_functions:
        assert fn in content, f"Missing JS helper: {fn}"


def test_style_css_defines_tokens_and_component_classes():
    content = _read(ASSETS_DIR / "style.css")

    expected_snippets = [
        ":root {",
        "--bg-surface:",
        "--accent-primary:",
        ".app-header",
        ".tabs-nav",
        ".modal",
        ".alert",
        ".badge",
        ".btn",
    ]

    for snippet in expected_snippets:
        assert snippet in content, f"Missing CSS snippet: {snippet}"
