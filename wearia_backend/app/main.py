import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.database.connection import engine, Base, SessionLocal
from app.database.seed import seed_database
from app.ai.predict import get_classifier

from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.referentials import router as referentials_router
from app.api.clothes import router as clothes_router
from app.api.routines import router as routines_router
from app.api.events import router as events_router
from app.api.ai import router as ai_router
from app.api.outfits import router as outfits_router

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Démarrage : création des tables & initialisation
    print("[SERVER] Initialisation de la base de données...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()

    print("[SERVER] Initialisation du modèle IA (KNN + HOG)...")
    get_classifier()
    print("[SERVER] Wearia Backend prêt pour Sprint 1 & Sprint 2 !")
    yield
    print("[SERVER] Arrêt du serveur Wearia.")

app = FastAPI(
    title="Wearia API",
    description="Backend FastAPI du projet Wearia - Recommandation Intelligente de Tenues (L3 DSI2)",
    version="2.0.0",
    lifespan=lifespan
)

# CORS permissif pour l'application mobile Android (émulateur 10.0.2.2 ou Wi-Fi)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montage du dossier de photos /uploads
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# Enregistrement des routes
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(referentials_router)
app.include_router(clothes_router)
app.include_router(routines_router)
app.include_router(events_router)
app.include_router(ai_router)
app.include_router(outfits_router)

@app.get("/", tags=["Health"])
def root():
    return {
        "status": "online",
        "app": "Wearia Core API",
        "version": "2.0.0",
        "docs": "/docs",
        "sprint_status": "Sprint 1 & Sprint 2 Prêts"
    }
