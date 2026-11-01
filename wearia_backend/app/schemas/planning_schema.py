from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class RoutineCreate(BaseModel):
    jour_semaine: str = Field(..., example="LUNDI")  # LUNDI..DIMANCHE
    occasion: str = Field(default="UNIVERSITE", example="UNIVERSITE")
    est_active: Optional[bool] = True

class RoutineUpdate(BaseModel):
    occasion: Optional[str] = None
    est_active: Optional[bool] = None

class RoutineResponse(BaseModel):
    id: int
    user_id: int
    jour_semaine: str
    occasion: str
    est_active: bool

    class Config:
        from_attributes = True

class EventCreate(BaseModel):
    titre: str = Field(..., example="Soutenance de projet")
    date: date
    occasion: str = Field(default="EVENEMENT", example="EVENEMENT")

class EventUpdate(BaseModel):
    titre: Optional[str] = None
    date: Optional[date] = None
    occasion: Optional[str] = None

class EventResponse(BaseModel):
    id: int
    user_id: int
    titre: str
    date: date
    occasion: str

    class Config:
        from_attributes = True
