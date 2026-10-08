from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import admin, auth, incidents, notifications, reports, worker
from app.config import FRONTEND_URL

app = FastAPI(
    title="CivicGuard AI",
    description="AI-powered infrastructure complaint and incident management platform",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL, "http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(reports.router, prefix="/api/reports", tags=["Reports"])
app.include_router(incidents.router, prefix="/api/incidents", tags=["Incidents"])
app.include_router(notifications.router, prefix="/api/notifications", tags=["Notifications"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])
app.include_router(worker.router, prefix="/api/worker", tags=["Worker"])


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "CivicGuard AI Backend"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
