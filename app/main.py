from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.routers import pantry
from app.routers import pantry, auth  # <-- Import the new auth router
from datetime import datetime  # <-- Import datetime

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description="Athyra Meal Planning API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(pantry.router, prefix="/api")

# Health check
@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat()
    }

# Root
@app.get("/")
async def root():
    return {
        "message": "Athyra API",
        "docs": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)