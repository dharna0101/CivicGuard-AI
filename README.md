# CivicGuard AI

CivicGuard AI is an AI-powered infrastructure complaint and incident management platform designed to turn citizen reports into actionable incidents.

Tagline: "From Complaints to Action."

This repository contains a full-stack application with:

- React + TypeScript + Vite frontend
- FastAPI backend with JWT auth
- MongoDB-ready domain models and mock in-memory storage
- AI analysis, clustering, priority calculation, and verification layers
- Role-based student/citizen, worker, and admin experiences
- Interactive map and dashboard analytics

## Quick start

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev -- --host 0.0.0.0
```

## Demo accounts

- Student: student@civicguard.ai / student123
- Worker: worker@civicguard.ai / worker123
- Admin: admin@civicguard.ai / admin123

### Notes

- The platform runs in mock AI mode when no external model key is configured.
- The app is intentionally designed to work without an AI API key.
