from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routers.resume_routes import router as resume_router
from backend.routers.job_routes import router as job_router
from backend.routers.ai_routes import router as ai_router

app = FastAPI(
    title="ResumeIQ API",
    version="1.0.0"
)

# -----------------------------
# CORS
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Routers
# -----------------------------
app.include_router(
    resume_router,
    prefix="/resume",
    tags=["Resume"]
)

app.include_router(
    job_router,
    prefix="/job",
    tags=["Job"]
)

app.include_router(
    ai_router,
    prefix="/ai",
    tags=["AI"]
)


@app.get("/")
def root():
    return {
        "message": "ResumeIQ API is running",
        "status": "success"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }