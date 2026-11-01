from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class UserRegister(BaseModel):
    nom: str = Field(..., min_length=2, example="Ameni Homri")
    email: str = Field(..., min_length=5, example="ameni@wearia.tn")
    mot_de_passe: str = Field(..., min_length=8, description="Au moins 8 caractères selon BR05", example="secret1234")
    genre: Optional[str] = "FEMME"
    ville: Optional[str] = "Tunis"

class UserLogin(BaseModel):
    email: str = Field(..., min_length=5, example="ameni@wearia.tn")
    mot_de_passe: str = Field(..., example="secret1234")

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    nom: str
    email: str

class UserProfileUpdate(BaseModel):
    nom: Optional[str] = None
    genre: Optional[str] = None
    date_naissance: Optional[date] = None
    ville: Optional[str] = None
    hauteur_cm: Optional[int] = None
    poids_kg: Optional[float] = None
    taille_vestimentaire: Optional[str] = None
    coupe_preferee: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    nom: str
    email: str
    genre: Optional[str] = None
    ville: Optional[str] = None
    hauteur_cm: Optional[int] = None
    poids_kg: Optional[float] = None
    taille_vestimentaire: Optional[str] = None
    coupe_preferee: Optional[str] = None

    class Config:
        from_attributes = True
