import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Use Supabase PostgreSQL if DATABASE_URL is set, otherwise fall back to SQLite
DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    # Supabase / PostgreSQL
    engine = create_engine(DATABASE_URL)
else:
    # Local SQLite fallback
    engine = create_engine(
        "sqlite:///./pashuvision.db",
        connect_args={"check_same_thread": False}
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
