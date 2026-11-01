from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.user import Utilisateur
from app.models.planning import RoutineHebdomadaire
from app.schemas.user_schema import UserRegister, UserLogin, TokenResponse, UserResponse
from app.services.auth_service import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentification"])

@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    # BR05: E-mail unique et mot de passe >= 8 caractères
    existing_user = db.query(Utilisateur).filter(Utilisateur.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Un compte avec cette adresse e-mail existe déjà (BR05)."
        )

    hashed_pw = hash_password(user_data.mot_de_passe)
    new_user = Utilisateur(
        nom=user_data.nom,
        email=user_data.email,
        mot_de_passe_hash=hashed_pw,
        genre=user_data.genre or "MIXTE",
        ville=user_data.ville or "Tunis",
        consentement_rgpd=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Création par défaut d'une routine hebdomadaire pour tester immédiatement BR09
    default_routine = RoutineHebdomadaire(
        user_id=new_user.id,
        jour_semaine="LUNDI",
        occasion="UNIVERSITE",
        est_active=True
    )
    db.add(default_routine)
    db.commit()

    token = create_access_token({"sub": str(new_user.id), "email": new_user.email})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": new_user.id,
        "nom": new_user.nom,
        "email": new_user.email
    }

@router.post("/login", response_model=TokenResponse)
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(Utilisateur).filter(Utilisateur.email == login_data.email).first()
    if not user or not verify_password(login_data.mot_de_passe, user.mot_de_passe_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants incorrects (e-mail ou mot de passe invalide)."
        )

    token = create_access_token({"sub": str(user.id), "email": user.email})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": user.id,
        "nom": user.nom,
        "email": user.email
    }
