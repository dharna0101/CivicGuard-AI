# CivicGuard AI

CivicGuard AI is an AI-powered infrastructure complaint and incident management platform for citizen reporting, incident clustering, worker coordination, and administrative oversight.

Tagline: "From Complaints to Action."

## Features

- Citizens can register, report issues with photos, and track status.
- AI clustering merges related complaints into a single real incident.
- Priority and department recommendation are calculated automatically.
- Workers handle prioritized assignments and submit repair verification.
- Admins view analytics, assign departments and workers, and approve resolutions.
- Interactive map shows incident status by severity.
- Mock AI mode works without any external API key.

## Tech stack

- Frontend: React, TypeScript, Vite, Tailwind CSS, React Router, Axios, Leaflet
- Backend: FastAPI, Pydantic, JWT
- Data: MongoDB-ready models with in-memory demo storage fallback
- AI: Modular mock AI service with deterministic recommendations

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

The app expects the backend at `http://localhost:8000`.

## Demo accounts

- Student: `student@civicguard.ai` / `student123`
- Worker: `worker@civicguard.ai` / `worker123`
- Admin: `admin@civicguard.ai` / `admin123`

## License

MIT
