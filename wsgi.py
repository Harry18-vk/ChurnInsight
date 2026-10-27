"""
WSGI Entry Point for Production Deployment (Render, Gunicorn, Railway)
"""
from pathlib import Path
import importlib.util
import sys

project_root = Path(__file__).resolve().parent
backend_dir = project_root / "app" / "backend"
src_dir = project_root / "src"

for d in [str(backend_dir), str(src_dir)]:
    if d not in sys.path:
        sys.path.insert(0, d)

backend_app_path = backend_dir / "app.py"
spec = importlib.util.spec_from_file_location("churninsight_backend", str(backend_app_path))
backend_module = importlib.util.module_from_spec(spec)
sys.modules["churninsight_backend"] = backend_module
spec.loader.exec_module(backend_module)

app = backend_module.app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
