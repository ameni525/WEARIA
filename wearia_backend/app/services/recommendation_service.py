from datetime import date, datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.user import Utilisateur
from app.models.clothing import Vetement
from app.models.planning import RoutineHebdomadaire, Evenement
from app.models.referentials import Categorie, TypeVetement, Couleur

JOURS_SEMAINE_FR = {
    0: "LUNDI",
    1: "MARDI",
    2: "MERCREDI",
    3: "JEUDI",
    4: "VENDREDI",
    5: "SAMEDI",
    6: "DIMANCHE",
}

def determine_daily_occasion(user: Utilisateur, db: Session, target_date: Optional[date] = None) -> str:
    d = target_date or date.today()

    # 1. Événement ponctuel
    event = db.query(Evenement).filter(
        Evenement.user_id == user.id,
        Evenement.date == d
    ).first()
    if event and event.occasion:
        return event.occasion

    # 2. Routine hebdomadaire du jour
    jour_nom = JOURS_SEMAINE_FR.get(d.weekday(), "LUNDI")
    routine = db.query(RoutineHebdomadaire).filter(
        RoutineHebdomadaire.user_id == user.id,
        RoutineHebdomadaire.jour_semaine == jour_nom,
        RoutineHebdomadaire.est_active == True
    ).first()
    if routine and routine.occasion:
        return routine.occasion

    # 3. Par défaut
    return "QUOTIDIEN"

def generate_outfit_recommendation(
    user: Utilisateur,
    db: Session,
    occasion: Optional[str] = None,
    temperature_celsius: float = 19.0,
    precipitations: bool = False,
    description_meteo: str = "Ensoleillé"
) -> dict:
    occ = occasion or determine_daily_occasion(user, db)

    # Récupérer les vêtements DISPONIBLES de l'utilisateur
    available_clothes = db.query(Vetement).filter(
        Vetement.user_id == user.id,
        Vetement.statut == "DISPONIBLE"
    ).all()

    if not available_clothes:
        return {
            "occasion": occ,
            "temperature": temperature_celsius,
            "weather": description_meteo,
            "items": [],
            "score": 0,
            "explanation": "Aucun vêtement propre disponible dans votre dressing. Ajoutez de nouveaux articles ou marquez vos vêtements comme propres."
        }

    # Classifier par catégories
    hauts = [v for v in available_clothes if v.categorie and v.categorie.nom in ["Haut"]]
    bas = [v for v in available_clothes if v.categorie and v.categorie.nom in ["Bas"]]
    chaussures = [v for v in available_clothes if v.categorie and v.categorie.nom in ["Chaussures"]]
    vestes = [v for v in available_clothes if (v.categorie and v.categorie.nom in ["Veste"]) or (v.type_vetement and v.type_vetement.est_couche_superieure)]
    robes = [v for v in available_clothes if v.categorie and v.categorie.nom in ["Robe"]]

    selected_items: List[Vetement] = []
    reasons: List[str] = []
    score = 100

    # Complétude : (Haut + Bas OU Robe) + Chaussures
    if robes and (not hauts or not bas):
        selected_items.append(robes[0])
        reasons.append(f"Robe élégante ({robes[0].nom})")
    elif hauts and bas:
        selected_items.append(hauts[0])
        selected_items.append(bas[0])
        reasons.append(f"Ensemble {hauts[0].nom} et {bas[0].nom}")
    elif hauts:
        selected_items.append(hauts[0])
        score -= 20
        reasons.append("Haut sélectionné (pensez à ajouter un bas)")
    elif bas:
        selected_items.append(bas[0])
        score -= 20
        reasons.append("Bas sélectionné (pensez à ajouter un haut)")

    if chaussures:
        selected_items.append(chaussures[0])
        reasons.append(f"Chaussures assorties ({chaussures[0].nom})")
    else:
        score -= 15

    # Météo : température < 14°C ou pluie -> veste/couche supérieure
    besoin_couche = (temperature_celsius < 14.0) or precipitations
    if besoin_couche:
        if vestes:
            selected_items.append(vestes[0])
            reasons.append(f"Couche chaude ({vestes[0].nom}) adaptée à la météo ({temperature_celsius}°C)")
        else:
            score -= 10
            reasons.append("Prévoir une veste car il fait frais")

    # Harmonie colorimétrique
    couleurs = set(v.couleur.nom for v in selected_items if v.couleur)
    if len(couleurs) <= 3:
        reasons.append("Palette harmonieuse de couleurs")
    else:
        score -= 10

    explanation = f"Tenue recommandée pour votre journée {occ.lower()} ({temperature_celsius}°C, {description_meteo.lower()}). " + " • ".join(reasons) + "."

    items_res = []
    for item in selected_items:
        items_res.append({
            "id": item.id,
            "name": item.nom,
            "category": item.categorie.nom if item.categorie else "Autre",
            "color": item.couleur.nom if item.couleur else "Inconnue",
            "photo_url": item.photo_url
        })

    return {
        "occasion": occ,
        "temperature": temperature_celsius,
        "weather": description_meteo,
        "items": items_res,
        "score": max(min(score, 100), 40),
        "explanation": explanation
    }
