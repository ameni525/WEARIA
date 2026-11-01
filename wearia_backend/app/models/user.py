from sqlalchemy import Column, Integer, String, Float, Boolean, Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.models.base import Base

class Utilisateur(Base):
    __tablename__ = "utilisateurs"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    mot_de_passe_hash = Column(String(255), nullable=False)
    genre = Column(String(20), default="MIXTE")  # HOMME, FEMME
    date_naissance = Column(Date, nullable=True)
    ville = Column(String(100), default="Tunis")
    hauteur_cm = Column(Integer, nullable=True)
    poids_kg = Column(Float, nullable=True)
    tour_epaules = Column(Float, nullable=True)
    tour_poitrine = Column(Float, nullable=True)
    tour_taille = Column(Float, nullable=True)
    tour_hanches = Column(Float, nullable=True)
    taille_vestimentaire = Column(String(10), nullable=True)  # S, M, L, XL
    coupe_preferee = Column(String(20), default="REGULIERE")  # AJUSTEE, REGULIERE, OVERSIZE
    consentement_rgpd = Column(Boolean, default=True)

    # Relations
    vetements = relationship("Vetement", back_populates="proprietaire", cascade="all, delete-orphan")
    routines = relationship("RoutineHebdomadaire", back_populates="utilisateur", cascade="all, delete-orphan")
    evenements = relationship("Evenement", back_populates="utilisateur", cascade="all, delete-orphan")
    tenues = relationship("Tenue", back_populates="utilisateur", cascade="all, delete-orphan")
    preferences_couleurs = relationship("PreferenceCouleur", back_populates="utilisateur", cascade="all, delete-orphan")
    preferences_styles = relationship("PreferenceStyle", back_populates="utilisateur", cascade="all, delete-orphan")

class PreferenceCouleur(Base):
    __tablename__ = "preferences_couleurs"

    id = Column(Integer, primary_key=True, index=True)
    utilisateur_id = Column(Integer, ForeignKey("utilisateurs.id"), nullable=False)
    couleur_id = Column(Integer, ForeignKey("couleurs.id"), nullable=False)
    type_preference = Column(String(20), default="AIME")  # AIME, EVITE

    utilisateur = relationship("Utilisateur", back_populates="preferences_couleurs")
    couleur = relationship("Couleur")

    __table_args__ = (UniqueConstraint("utilisateur_id", "couleur_id", "type_preference", name="uq_user_color_pref"),)

class PreferenceStyle(Base):
    __tablename__ = "preferences_styles"

    id = Column(Integer, primary_key=True, index=True)
    utilisateur_id = Column(Integer, ForeignKey("utilisateurs.id"), nullable=False)
    style_id = Column(Integer, ForeignKey("styles_vestimentaires.id"), nullable=False)
    type_preference = Column(String(20), default="AIME")  # AIME, EVITE

    utilisateur = relationship("Utilisateur", back_populates="preferences_styles")
    style = relationship("StyleVestimentaire")

    __table_args__ = (UniqueConstraint("utilisateur_id", "style_id", "type_preference", name="uq_user_style_pref"),)
