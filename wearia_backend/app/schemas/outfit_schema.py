from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, date
from app.schemas.clothing_schema import ClothingResponse

class OutfitItem(BaseModel):
    id: int
    name: str
    category: str
    color: str
    photo_url: str

class OutfitRecommendationRequest(BaseModel):
    occasion: Optional[str] = None  # Si absent, déduit selon BR09 (Événement ou Routine ou QUOTIDIEN)
    temperature_celsius: Optional[float] = 19.0
    precipitations: Optional[bool] = False
    description_meteo: Optional[str] = "Ensoleillé"

class OutfitRecommendationResponse(BaseModel):
    outfit_id: Optional[int] = None
    occasion: str
    temperature: float
    weather: str
    items: List[OutfitItem]
    score: int
    explanation: str

class OutfitCreate(BaseModel):
    occasion: str
    temperature_celsius: Optional[float] = None
    precipitations: Optional[bool] = False
    description_meteo: Optional[str] = None
    explication: Optional[str] = None
    score_compatibilite: Optional[int] = 85
    vetement_ids: List[int]
    est_favorite: Optional[bool] = False

class OutfitResponse(BaseModel):
    id: int
    user_id: int
    date_creation: datetime
    date_prevue: Optional[date] = None
    date_portee: Optional[datetime] = None
    occasion: str
    temperature_celsius: Optional[float] = None
    precipitations: bool
    description_meteo: Optional[str] = None
    explication: Optional[str] = None
    score_compatibilite: int
    est_generee: bool
    est_favorite: bool
    vetements: List[ClothingResponse] = []

    class Config:
        from_attributes = True

class FeedbackCreate(BaseModel):
    appreciation: str  # AIME, MOYEN, PAS_POUR_MOI
    motif_rejet: Optional[str] = None

class FeedbackResponse(BaseModel):
    id: int
    tenue_id: int
    user_id: int
    appreciation: str
    motif_rejet: Optional[str] = None
    date_feedback: datetime

    class Config:
        from_attributes = True
