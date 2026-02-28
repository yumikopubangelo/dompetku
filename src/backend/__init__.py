"""Package backend Dompetku.

Saat package ini diimpor (mis. `src.backend.services...`), tambahkan folder
`src/backend` ke `sys.path` agar import internal legacy seperti
`from models...` / `from services...` tetap ter-resolve di environment CI.
"""

from pathlib import Path
import sys

BACKEND_DIR = Path(__file__).resolve().parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))
