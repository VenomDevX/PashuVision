# System Architecture

PashuVision uses a modern 3-tier architecture:

1. **Frontend (Next.js 14)**
   - App Router based React framework.
   - Tailwind CSS for styling.
   - Component-driven architecture (`ImageUploader`, `PredictionCard`).

2. **Backend (FastAPI)**
   - High-performance Python backend.
   - SQLAlchemy for local SQLite storage (extensible to PostgreSQL).
   - PyTorch integration for inference inside `services/classifier.py`.

3. **AI Pipeline (PyTorch/YOLOv8)**
   - Two-stage classification: Species routing (Cattle vs Buffalo) followed by Breed classification.
   - Dataset augmented and balanced to 350 images per breed using `albumentations`.
