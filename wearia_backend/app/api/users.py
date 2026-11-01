from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.user import Utilisateur
from app.schemas.user_schema import UserResponse, UserProfileUpdate
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/users", tags=["Utilisateurs"])

@router.get("/me", response_model=UserResponse)
def get_profile(current_user: Utilisateur = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=UserResponse)
def update_profile(
    update_data: UserProfileUpdate,
    current_user: Utilisateur = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    update_dict = update_data.dict(exclude_unset=True)
    for field, val in update_dict.items():
        setattr(current_user, field, val)

    db.commit()
    db.refresh(current_user)
    return current_user

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_account(
    current_user: Utilisateur = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db.delete(current_user)
    db.commit()
    return None
