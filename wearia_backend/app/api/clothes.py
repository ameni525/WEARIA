import os
import uuid
import shutil
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.user import Utilisateur
from app.models.clothing import Vetement
from app.models.referentials import Categorie, TypeVetement, Couleur
from app.schemas.clothing_schema import ClothingCreate, ClothingUpdate, ClothingResponse
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/clothes", tags=["Dressing (Vêtements)"])

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
def upload_clothing_image(file: UploadFile = File(...)):
    """Enregistre une photo dans uploads/ et renvoie l'URL relative."""
    ext = os.path.splitext(file.filename)[1] or ".jpg"
    filename = f"clothing_{uuid.uuid4().hex[:10]}{ext}"
    dest_path = os.path.join(UPLOAD_DIR, filename)

    with open(dest_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"image_url": f"/uploads/{filename}"}

@router.get("", response_model=List[ClothingResponse])
def list_clothes(
    categorie_id: Optional[int] = Query(None, description="Filtre par catégorie"),
    couleur_id: Optional[int] = Query(None, description="Filtre par couleur"),
    saison: Optional[str] = Query(None, description="Filtre par saison"),
    statut: Optional[str] = Query(None, description="Filtre par statut (DISPONIBLE, SALE...)"),
    search: Optional[str] = Query(None, description="Recherche par mot-clé"),
    current_user: Utilisateur = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # BR06: L'utilisateur n'accède qu'à ses propres vêtements
    query = db.query(Vetement).filter(Vetement.user_id == current_user.id)

    if categorie_id:
        query = query.filter(Vetement.categorie_id == categorie_id)
    if couleur_id:
        query = query.filter(Vetement.couleur_id == couleur_id)
    if saison:
        query = query.filter(Vetement.saison == saison)
    if statut:
        query = query.filter(Vetement.statut == statut)
    if search:
        query = query.filter(Vetement.nom.ilike(f"%{search}%"))

    return query.order_by(Vetement.created_at.desc()).all()

@router.post("", response_model=ClothingResponse, status_code=status.HTTP_201_CREATED)
def add_clothing(
    clothing_in: ClothingCreate,
    current_user: Utilisateur = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # BR07: Photo obligatoire, type obligatoire, couleur obligatoire
    if not clothing_in.photo_url or not clothing_in.photo_url.strip():
        raise HTTPException(status_code=400, detail="Une photo est obligatoire pour enregistrer un vêtement (BR07).")

    new_item = Vetement(
        user_id=current_user.id,
        nom=clothing_in.nom,
        photo_url=clothing_in.photo_url,
        type_vetement_id=clothing_in.type_vetement_id,
        categorie_id=clothing_in.categorie_id,
        couleur_id=clothing_in.couleur_id,
        style_id=clothing_in.style_id,
        matiere=clothing_in.matiere or "Coton",
        coupe=clothing_in.coupe or "REGULIERE",
        saison=clothing_in.saison or "TOUTE_SAISON",
        est_thermique=clothing_in.est_thermique or False,
        est_impermeable=clothing_in.est_impermeable or False,
        statut=clothing_in.statut or "DISPONIBLE"
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

@router.get("/{clothing_id}", response_model=ClothingResponse)
def get_clothing_detail(
    clothing_id: int,
    current_user: Utilisateur = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    item = db.query(Vetement).filter(
        Vetement.id == clothing_id,
        Vetement.user_id == current_user.id
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Vêtement introuvable.")
    return item

@router.put("/{clothing_id}", response_model=ClothingResponse)
def update_clothing(
    clothing_id: int,
    update_data: ClothingUpdate,
    current_user: Utilisateur = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    item = db.query(Vetement).filter(
        Vetement.id == clothing_id,
        Vetement.user_id == current_user.id
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Vêtement introuvable.")

    data_dict = update_data.dict(exclude_unset=True)
    for field, val in data_dict.items():
        setattr(item, field, val)

    db.commit()
    db.refresh(item)
    return item

@router.delete("/{clothing_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_clothing(
    clothing_id: int,
    current_user: Utilisateur = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    item = db.query(Vetement).filter(
        Vetement.id == clothing_id,
        Vetement.user_id == current_user.id
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Vêtement introuvable.")

    db.delete(item)
    db.commit()
    return None
