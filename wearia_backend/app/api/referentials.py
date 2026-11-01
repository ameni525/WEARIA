from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.referentials import Categorie, TypeVetement, Couleur, StyleVestimentaire
from app.schemas.referentials_schema import (
    CategorieResponse,
    TypeVetementResponse,
    CouleurResponse,
    StyleResponse
)

router = APIRouter(prefix="/referentials", tags=["Référentiels"])

@router.get("/categories", response_model=List[CategorieResponse])
def get_categories(db: Session = Depends(get_db)):
    return db.query(Categorie).all()

@router.get("/types", response_model=List[TypeVetementResponse])
def get_types(categorie_id: int = None, db: Session = Depends(get_db)):
    query = db.query(TypeVetement)
    if categorie_id:
        query = query.filter(TypeVetement.categorie_id == categorie_id)
    return query.all()

@router.get("/colors", response_model=List[CouleurResponse])
def get_colors(db: Session = Depends(get_db)):
    return db.query(Couleur).all()

@router.get("/styles", response_model=List[StyleResponse])
def get_styles(db: Session = Depends(get_db)):
    return db.query(StyleVestimentaire).all()
