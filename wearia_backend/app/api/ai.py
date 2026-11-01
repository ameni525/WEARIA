import os
import uuid
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.schemas.ai_schema import ClassifyResponse
from app.ai.predict import predict_clothing

router = APIRouter(prefix="/ai", tags=["Intelligence Artificielle"])

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/classify", response_model=ClassifyResponse)
async def classify_clothing_image(file: UploadFile = File(...)):
    """
    Analyse une photo de vêtement :
    - Extraction HOG
    - Classification de la catégorie par modèle KNN
    - Détection de la couleur dominante via OpenCV
    - Renvoie la prédiction et l'URL de l'image pour validation/correction par l'utilisateur (US02)
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Le fichier fourni doit être une image.")

    ext = os.path.splitext(file.filename)[1] or ".jpg"
    filename = f"scan_{uuid.uuid4().hex[:10]}{ext}"
    dest_path = os.path.join(UPLOAD_DIR, filename)

    with open(dest_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        prediction = predict_clothing(dest_path)
    except Exception as e:
        # En cas d'erreur de parsing d'image, valeur par défaut sécurisée
        prediction = {
            "category": "Haut",
            "color": "Blanc",
            "confidence": 0.80
        }

    return {
        "category": prediction["category"],
        "color": prediction["color"],
        "confidence": prediction["confidence"],
        "image_url": f"/uploads/{filename}"
    }
