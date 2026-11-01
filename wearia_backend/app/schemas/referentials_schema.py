from pydantic import BaseModel
from typing import Optional

class CategorieResponse(BaseModel):
    id: int
    nom: str

    class Config:
        from_attributes = True

class TypeVetementResponse(BaseModel):
    id: int
    nom: str
    categorie_id: int
    genre_cible: str
    est_couche_superieure: bool

    class Config:
        from_attributes = True

class CouleurResponse(BaseModel):
    id: int
    nom: str
    code_hex: str

    class Config:
        from_attributes = True

class StyleResponse(BaseModel):
    id: int
    libelle: str

    class Config:
        from_attributes = True
