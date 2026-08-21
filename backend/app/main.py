# pyrefly: ignore [missing-import]
from fastapi import FastAPI
# pyrefly: ignore [missing-import]
from fastapi.middleware.cors import CORSMiddleware
from app.download_models import download_models

# Download AI models from Google Drive on first startup
download_models()

from app.api import predict, scans, health
from app.database import engine, Base
from app.models.scan import Scan
from app.models.user import User
from fastapi.staticfiles import StaticFiles
import os

# Create static directory if it doesn't exist
os.makedirs("static/uploads", exist_ok=True)

from sqlalchemy import text

# Create database tables
Base.metadata.create_all(bind=engine)

def run_auto_migrations():
    """Safely apply table schema updates directly."""
    print("Checking database schema updates...")
    with engine.begin() as conn:
        try:
            conn.execute(text("ALTER TABLE scans ADD COLUMN image_hash VARCHAR;"))
            conn.execute(text("CREATE INDEX ix_scans_image_hash ON scans (image_hash);"))
            print("Added image_hash column.")
        except Exception:
            pass
            
        try:
            conn.execute(text("ALTER TABLE scans ADD COLUMN kirti_code VARCHAR;"))
            conn.execute(text("CREATE INDEX ix_scans_kirti_code ON scans (kirti_code);"))
            print("Added kirti_code column.")
        except Exception:
            pass

run_auto_migrations()

app = FastAPI(
    title="PashuVision API",
    description="Backend API for Livestock Breed Identification",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, tags=["Health"])
app.include_router(predict.router, prefix="/api/v1/predict", tags=["Prediction"])
app.include_router(scans.router, prefix="/api/v1/scans", tags=["Scans"])

# Serve static files for uploaded images
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return {"message": "Welcome to PashuVision API"}
