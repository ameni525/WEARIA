import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from app.database.connection import engine, Base, SessionLocal
from app.database.seed import seed_database
import app.models

def create_postgres_database():
    try:
        print("[POSTGRES] Connexion au serveur PostgreSQL local...")
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="admin",
            host="localhost",
            port=5432
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()

        cur.execute("SELECT 1 FROM pg_database WHERE datname='wearia_db'")
        exists = cur.fetchone()
        if not exists:
            cur.execute("CREATE DATABASE wearia_db;")
            print("[POSTGRES] Base de données 'wearia_db' créée avec succès !")
        else:
            print("[POSTGRES] La base 'wearia_db' existe déjà !")

        cur.close()
        conn.close()

        # Maintenant, se connecter à wearia_db et créer les tables + insérer les données
        print("[POSTGRES] Création de toutes les tables dans 'wearia_db'...")
        Base.metadata.create_all(bind=engine)
        print("[POSTGRES] Tables créées avec succès !")

        db = SessionLocal()
        try:
            seed_database(db)
            print("[POSTGRES] Données de démonstration et référentiels insérés avec succès !")
        finally:
            db.close()

        print("\n--> TOUT EST PRÊT DANS POSTGRESQL ! Vous pouvez l'ouvrir dans pgAdmin 4.")

    except Exception as e:
        print(f"[ERREUR] Impossible de se connecter à PostgreSQL : {e}")

if __name__ == "__main__":
    create_postgres_database()
