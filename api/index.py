"""
Vercel serverless giriş noktası.
backend/main.py içindeki FastAPI uygulamasını /api altında mount eder,
böylece backend kodu tek bir yerde kalır (bu dosya sadece bir köprüdür).
"""

import pathlib
import sys

BACKEND_DIR = pathlib.Path(__file__).resolve().parent.parent / "backend"
sys.path.insert(0, str(BACKEND_DIR))

from fastapi import FastAPI

from main import app as backend_app  # noqa: E402

app = FastAPI()
app.mount("/api", backend_app)
