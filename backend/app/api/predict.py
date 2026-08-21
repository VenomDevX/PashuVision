import os
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.prediction import PredictionResponse
from app.services.classifier import predict_image
from app.services.image_service import save_upload_file
from app.models.scan import Scan

router = APIRouter()

@router.post("/", response_model=PredictionResponse)
async def create_prediction(
    image: UploadFile = File(...),
    species_hint: str = Form("auto"),
    db: Session = Depends(get_db)
):
    if not image.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")
        
    try:
        # Save image via service
        file_location = save_upload_file(image, image.filename)
        
        # Run prediction
        result = predict_image(str(file_location), species_hint)
        
        # Save to database
        db_scan = Scan(
            image_url=f"/static/uploads/{image.filename}",
            species=result["species"],
            species_confidence=result["species_confidence"],
            breed=result["breed"],
            breed_confidence=result["breed_confidence"]
        )
        db.add(db_scan)
        db.commit()
        db.refresh(db_scan)
        
        # Return response
        response = PredictionResponse(**result, image_url=db_scan.image_url)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
