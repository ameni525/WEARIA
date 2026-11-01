from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Vetement(Base):
    __tablename__ = "vetements"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("utilisateurs.id"), nullable=False)
    nom = Column(String(150), nullable=False)
    photo_url = Column(String(300), nullable=False)  # BR07: photo obligatoire
    type_vetement_id = Column(Integer, ForeignKey("types_vetements.id"), nullable=False)  # BR07: type obligatoire
    categorie_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    couleur_id = Column(Integer, ForeignKey("couleurs.id"), nullable=False)  # BR07: couleur obligatoire
    style_id = Column(Integer, ForeignKey("styles_vestimentaires.id"), nullable=True)

    matiere = Column(String(100), default="Coton")  # saisie manuelle
    coupe = Column(String(20), default="REGULIERE")  # AJUSTEE, REGULIERE, OVERSIZE
    saison = Column(String(20), default="TOUTE_SAISON")  # PRINTEMPS, ETE, AUTOMNE, HIVER, TOUTE_SAISON
    est_thermique = Column(Boolean, default=False)
    est_impermeable = Column(Boolean, default=False)
    statut = Column(String(20), default="DISPONIBLE")  # DISPONIBLE, SALE, EN_LAVAGE, INDISPONIBLE

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relations
    proprietaire = relationship("Utilisateur", back_populates="vetements")
    type_vetement = relationship("TypeVetement")
    categorie = relationship("Categorie")
    couleur = relationship("Couleur")
    style = relationship("StyleVestimentaire")
