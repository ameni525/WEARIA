import os
from sqlalchemy.orm import Session
from app.models.referentials import Categorie, TypeVetement, Couleur, StyleVestimentaire
from app.models.user import Utilisateur
from app.models.clothing import Vetement
from app.models.planning import RoutineHebdomadaire
from app.services.auth_service import hash_password

def seed_database(db: Session):
    # 1. Catégories
    categories_data = ["Haut", "Bas", "Chaussures", "Veste", "Robe", "Accessoire"]
    cat_map = {}
    for cat_name in categories_data:
        c = db.query(Categorie).filter(Categorie.nom == cat_name).first()
        if not c:
            c = Categorie(nom=cat_name)
            db.add(c)
            db.commit()
            db.refresh(c)
        cat_map[cat_name] = c

    # 2. Types de vêtements
    types_data = [
        ("Chemise", "Haut", "MIXTE", False),
        ("T-shirt", "Haut", "MIXTE", False),
        ("Pull", "Haut", "MIXTE", True),
        ("Pantalon", "Bas", "MIXTE", False),
        ("Jean", "Bas", "MIXTE", False),
        ("Jupe", "Bas", "FEMME", False),
        ("Robe", "Robe", "FEMME", False),
        ("Baskets", "Chaussures", "MIXTE", False),
        ("Chaussures classiques", "Chaussures", "MIXTE", False),
        ("Veste", "Veste", "MIXTE", True),
        ("Manteau", "Veste", "MIXTE", True),
    ]
    type_map = {}
    for nom, cat_name, genre, couche in types_data:
        t = db.query(TypeVetement).filter(TypeVetement.nom == nom).first()
        if not t:
            t = TypeVetement(
                nom=nom,
                categorie_id=cat_map[cat_name].id,
                genre_cible=genre,
                est_couche_superieure=couche
            )
            db.add(t)
            db.commit()
            db.refresh(t)
        type_map[nom] = t

    # 3. Couleurs
    couleurs_data = [
        ("Blanc", "#FFFFFF"),
        ("Noir", "#1A1A1A"),
        ("Bleu", "#1E88E5"),
        ("Bleu Marine", "#0D1B2A"),
        ("Gris", "#9E9E9E"),
        ("Beige", "#E0D6C3"),
        ("Rouge", "#E53935"),
        ("Marron", "#6D4C41"),
        ("Vert", "#43A047"),
        ("Kaki", "#78866B")
    ]
    color_map = {}
    for nom, code in couleurs_data:
        cl = db.query(Couleur).filter(Couleur.nom == nom).first()
        if not cl:
            cl = Couleur(nom=nom, code_hex=code)
            db.add(cl)
            db.commit()
            db.refresh(cl)
        color_map[nom] = cl

    # 4. Styles vestimentaires
    styles_data = ["Decontracte", "Formel", "Elegant", "Sport", "Streetwear"]
    style_map = {}
    for s_nom in styles_data:
        st = db.query(StyleVestimentaire).filter(StyleVestimentaire.libelle == s_nom).first()
        if not st:
            st = StyleVestimentaire(libelle=s_nom)
            db.add(st)
            db.commit()
            db.refresh(st)
        style_map[s_nom] = st

    # 5. Utilisateur de démonstration
    demo_email = "ameni@wearia.tn"
    user = db.query(Utilisateur).filter(Utilisateur.email == demo_email).first()
    if not user:
        user = Utilisateur(
            nom="Ameni Homri",
            email=demo_email,
            mot_de_passe_hash=hash_password("password123"),
            genre="FEMME",
            ville="Tunis",
            hauteur_cm=165,
            poids_kg=58.0,
            taille_vestimentaire="M",
            coupe_preferee="REGULIERE",
            consentement_rgpd=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        # Routine hebdomadaire (Lundi, Mercredi, Vendredi -> UNIVERSITE)
        for jour in ["LUNDI", "MERCREDI", "VENDREDI"]:
            db.add(RoutineHebdomadaire(
                user_id=user.id,
                jour_semaine=jour,
                occasion="UNIVERSITE",
                est_active=True
            ))
        db.commit()

    # Vider les anciens vêtements de démo et en insérer 8 complets avec photos
    existing_count = db.query(Vetement).filter(Vetement.user_id == user.id).count()
    if existing_count < 8:
        db.query(Vetement).filter(Vetement.user_id == user.id).delete()
        db.commit()

        demo_items = [
            ("Chemise Oxford Blanche", "/uploads/demo_chemise.jpg", "Chemise", "Haut", "Blanc", "Decontracte", False, False),
            ("Jean Denim Bleu", "/uploads/demo_jean.jpg", "Jean", "Bas", "Bleu", "Decontracte", False, False),
            ("Pantalon Chino Noir", "/uploads/demo_pantalon.jpg", "Pantalon", "Bas", "Noir", "Formel", False, False),
            ("Baskets Blanches", "/uploads/demo_baskets.jpg", "Baskets", "Chaussures", "Blanc", "Sport", False, False),
            ("Veste Coupe-Vent Noire", "/uploads/demo_veste.jpg", "Veste", "Veste", "Noir", "Decontracte", True, True),
            ("Pull Maille Beige", "/uploads/demo_pull.jpg", "Pull", "Haut", "Beige", "Decontracte", True, False),
            ("T-shirt Basique Noir", "/uploads/demo_tshirt.jpg", "T-shirt", "Haut", "Noir", "Streetwear", False, False),
            ("Chaussures en Cuir Marron", "/uploads/demo_chaussures.jpg", "Chaussures classiques", "Chaussures", "Marron", "Formel", False, False),
        ]

        for nom, photo, type_nom, cat_nom, col_nom, sty_nom, therm, imperm in demo_items:
            vet = Vetement(
                user_id=user.id,
                nom=nom,
                photo_url=photo,
                type_vetement_id=type_map[type_nom].id,
                categorie_id=cat_map[cat_nom].id,
                couleur_id=color_map[col_nom].id,
                style_id=style_map[sty_nom].id,
                matiere="Coton",
                coupe="REGULIERE",
                saison="TOUTE_SAISON",
                est_thermique=therm,
                est_impermeable=imperm,
                statut="DISPONIBLE"
            )
            db.add(vet)
        db.commit()
        print("[DATABASE] 8 vêtements enrichis avec photos insérés pour Ameni !")

    print("[DATABASE] Référentiels synchronisés avec succès !")
