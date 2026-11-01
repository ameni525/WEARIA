from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.schemas.referentials_schema import TypeVetementResponse, CategorieResponse, CouleurResponse, StyleResponse

class ClothingCreate(BaseModel):
    nom: str = Field(..., min_length=2, example="Chemise Blanche Casual")
    photo_url: str = Field(..., example="/uploads/chemise_blanche.jpg")
    type_vetement_id: int
    categorie_id: int
    couleur_id: int
    style_id: Optional[int] = None
    matiere: Optional[str] = "Coton"
    coupe: Optional[str] = "REGULIERE"
    saison: Optional[str] = "TOUTE_SAISON"
    est_thermique: Optional[bool] = False
    est_impermeable: Optional[bool] = False
    statut: Optional[str] = "DISPONIBLE"

class ClothingUpdate(BaseModel):
    nom: Optional[str] = None
    photo_url: Optional[str] = None
    type_vetement_id: Optional[int] = None
    categorie_id: Optional[int] = None
    couleur_id: Optional[int] = None
    style_id: Optional[int] = None
    matiere: Optional[str] = None
    coupe: Optional[str] = None
    saison: Optional[str] = None
    est_thermique: Optional[bool] = None
    est_impermeable: Optional[bool] = None
    statut: Optional[str] = None

class ClothingResponse(BaseModel):
    id: int
    user_id: int
    nom: str
    photo_url: str
    type_vetement_id: int
    categorie_id: int
    couleur_id: int
    style_id: Optional[int] = None
    matiere: Optional[str] = None
    coupe: Optional[str] = None
    saison: Optional[str] = None
    est_thermique: bool
    est_impermeable: bool
    statut: str
    created_at: Optional[datetime] = None

    type_vetement: Optional[TypeVetementResponse] = None
    categorie: Optional[CategorieResponse] = None
    couleur: Optional[CouleurResponse] = None
    style: Optional[StyleResponse] = None

    class Config:
        from_attributes = True
