from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.user import Utilisateur
from app.models.planning import Evenement
from app.schemas.planning_schema import EventCreate, EventUpdate, EventResponse
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/events", tags=["Planning - Événements"])

@router.get("", response_model=List[EventResponse])
def get_events(
    current_user: Utilisateur = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(Evenement).filter(Evenement.user_id == current_user.id).order_by(Evenement.date.asc()).all()

@router.post("", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
def create_event(
    event_in: EventCreate,
    current_user: Utilisateur = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    new_event = Evenement(
        user_id=current_user.id,
        titre=event_in.titre,
        date=event_in.date,
        occasion=event_in.occasion
    )
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event

@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(
    event_id: int,
    current_user: Utilisateur = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    e = db.query(Evenement).filter(
        Evenement.id == event_id,
        Evenement.user_id == current_user.id
    ).first()
    if not e:
        raise HTTPException(status_code=404, detail="Événement introuvable.")

    db.delete(e)
    db.commit()
    return None
