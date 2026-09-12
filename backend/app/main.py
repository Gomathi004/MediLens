from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.history import router as history_router
from app.api.routes.scan import router as scan_router


# ==================================================
# MediLens FastAPI Application
# ==================================================

app = FastAPI(
    title="MediLens API",
    description=(
        "Backend API for the MediLens "
        "medicine label simplifier"
    ),
    version="1.0.0",
)


# ==================================================
# CORS Configuration
# ==================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================================================
# API Routers
# ==================================================

app.include_router(scan_router)
app.include_router(history_router)


# ==================================================
# Root Endpoint
# ==================================================

@app.get("/")
def root():
    return {
        "message": "Welcome to MediLens API",
        "status": "running",
        "version": "1.0.0",
    }


# ==================================================
# Health Check
# ==================================================

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "MediLens API",
    }