from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.user import Utilisateur
from app.models.planning import RoutineHebdomadaire
from app.schemas.planning_schema import RoutineCreate, RoutineUpdate, RoutineResponse
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/routines", tags=["Planning - Routine Hebdomadaire"])

@router.get("", response_model=List[RoutineResponse])
def get_routines(
    current_user: Utilisateur = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(RoutineHebdomadaire).filter(
        RoutineHebdomadaire.user_id == current_user.id
    ).all()

@router.post("", response_model=RoutineResponse, status_code=status.HTTP_201_CREATED)
def create_or_update_routine(
    routine_in: RoutineCreate,
    current_user: Utilisateur = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Unicité (utilisateur, jourSemaine)
    existing = db.query(RoutineHebdomadaire).filter(
        RoutineHebdomadaire.user_id == current_user.id,
        RoutineHebdomadaire.jour_semaine == routine_in.jour_semaine.upper()
    ).first()

    if existing:
        existing.occasion = routine_in.occasion
        existing.est_active = routine_in.est_active if routine_in.est_active is not None else existing.est_active
        db.commit()
        db.refresh(existing)
        return existing

    new_routine = RoutineHebdomadaire(
        user_id=current_user.id,
        jour_semaine=routine_in.jour_semaine.upper(),
        occasion=routine_in.occasion,
        est_active=routine_in.est_active if routine_in.est_active is not None else True
    )
    db.add(new_routine)
    db.commit()
    db.refresh(new_routine)
    return new_routine

@router.delete("/{routine_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_routine(
    routine_id: int,
    current_user: Utilisateur = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    r = db.query(RoutineHebdomadaire).filter(
        RoutineHebdomadaire.id == routine_id,
        RoutineHebdomadaire.user_id == current_user.id
    ).first()
    if not r:
        raise HTTPException(status_code=404, detail="Routine introuvable.")

    db.delete(r)
    db.commit()
    return None
