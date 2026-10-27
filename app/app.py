"""
Main Application Entry Point
Points directly to the full-featured ChurnInsight platform.
"""
from pathlib import Path
import sys

backend_dir = Path(__file__).resolve().parent / "backend"
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app import app

if __name__ == "__main__":
    print("\n===================================")
    print("CHURNINSIGHT PLATFORM")
    print("===================================")
    print("Server running on: http://127.0.0.1:5000")
    print("Admin Portal:      http://127.0.0.1:5000/login")
    print("Default Login:     admin / admin123\n")
    app.run(host="127.0.0.1", port=5000, debug=True)
