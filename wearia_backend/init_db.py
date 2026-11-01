from app.database.connection import engine, Base, SessionLocal
from app.database.seed import seed_database
import app.models # Charge tous les modèles

if __name__ == "__main__":
    print("[INIT] Création des tables dans la base de données...")
    Base.metadata.create_all(bind=engine)
    print("[INIT] Tables créées avec succès !")
    db = SessionLocal()
    try:
        seed_database(db)
        print("[INIT] Base initialisée et prête pour l'application !")
    finally:
        db.close()
