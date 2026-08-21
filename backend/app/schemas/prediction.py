from pydantic import BaseModel
from typing import Optional

class PredictionResponse(BaseModel):
    species: str
    species_confidence: float
    breed: str
    breed_confidence: float
    image_url: Optional[str] = None
    kirti_code: Optional[str] = None
    
    class Config:
        from_attributes = True
