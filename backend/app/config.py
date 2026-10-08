import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "civicguard-demo-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
MOCK_AI_MODE = os.getenv("MOCK_AI_MODE", "true").lower() == "true"
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "civicguard")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
