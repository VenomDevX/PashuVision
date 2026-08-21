from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.scan import Scan

router = APIRouter()

@router.get("/")
def get_scans(
    skip: int = 0, 
    limit: int = 100, 
    search: str = None,
    db: Session = Depends(get_db)
):
    query = db.query(Scan)
    
    if search:
        query = query.filter(Scan.kirti_code.ilike(f"%{search}%"))
        
    scans = query.order_by(Scan.created_at.desc()).offset(skip).limit(limit).all()
    return scans
