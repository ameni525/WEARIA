from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.user import Utilisateur
from app.models.outfit import Tenue, Feedback
from app.models.clothing import Vetement
from app.schemas.outfit_schema import (
    OutfitRecommendationRequest,
    OutfitRecommendationResponse,
    OutfitCreate,
    OutfitResponse,
    FeedbackCreate,
    FeedbackResponse
)
from app.services.auth_service import get_current_user
from app.services.recommendation_service import generate_outfit_recommendation

router = APIRouter(tags=["Recommandations & Tenues"])

@router.post("/recommendations", response_model=OutfitRecommendationResponse)
def get_recommendation(
    req: OutfitRecommendationRequest,
    current_user: Utilisateur = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Génère une tenue intelligente :
    - Occasion déduite via BR09 (Événement > Routine hebdomadaire > QUOTIDIEN)
    - Exclusion des vêtements sales/indisponibles via BR08
    - Complétude (Haut+Bas / Robe + Chaussures) via BR01
    - Veste météo si < 14°C ou pluie via BR02
    - Harmonie des couleurs via BR03
    """
    res = generate_outfit_recommendation(
        user=current_user,
        db=db,
        occasion=req.occasion,
        temperature_celsius=req.temperature_celsius if req.temperature_celsius is not None else 19.0,
        precipitations=req.precipitations or False,
        description_meteo=req.description_meteo or "Ensoleillé"
    )
    return res

@router.get("/outfits", response_model=List[OutfitResponse])
def list_outfits(
    current_user: Utilisateur = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(Tenue).filter(Tenue.user_id == current_user.id).order_by(Tenue.date_creation.desc()).all()

@router.post("/outfits", response_model=OutfitResponse, status_code=status.HTTP_201_CREATED)
def save_outfit(
    outfit_in: OutfitCreate,
    current_user: Utilisateur = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    tenue = Tenue(
        user_id=current_user.id,
        occasion=outfit_in.occasion,
        temperature_celsius=outfit_in.temperature_celsius,
        precipitations=outfit_in.precipitations,
        description_meteo=outfit_in.description_meteo,
        explication=outfit_in.explication,
        score_compatibilite=outfit_in.score_compatibilite or 85,
        est_favorite=outfit_in.est_favorite or False,
        est_generee=True
    )

    if outfit_in.vetement_ids:
        clothes = db.query(Vetement).filter(
            Vetement.id.in_(outfit_in.vetement_ids),
            Vetement.user_id == current_user.id
        ).all()
        tenue.vetements = clothes

    db.add(tenue)
    db.commit()
    db.refresh(tenue)
    return tenue

@router.post("/outfits/{outfit_id}/feedback", response_model=FeedbackResponse)
def add_feedback(
    outfit_id: int,
    feedback_in: FeedbackCreate,
    current_user: Utilisateur = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    tenue = db.query(Tenue).filter(
        Tenue.id == outfit_id,
        Tenue.user_id == current_user.id
    ).first()
    if not tenue:
        raise HTTPException(status_code=404, detail="Tenue introuvable.")

    existing = db.query(Feedback).filter(Feedback.tenue_id == outfit_id).first()
    if existing:
        existing.appreciation = feedback_in.appreciation
        existing.motif_rejet = feedback_in.motif_rejet
        db.commit()
        db.refresh(existing)
        return existing

    fb = Feedback(
        tenue_id=outfit_id,
        user_id=current_user.id,
        appreciation=feedback_in.appreciation,
        motif_rejet=feedback_in.motif_rejet
    )
    db.add(fb)
    db.commit()
    db.refresh(fb)
    return fb
