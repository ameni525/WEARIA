from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Categorie(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(50), unique=True, nullable=False)

    types = relationship("TypeVetement", back_populates="categorie", cascade="all, delete-orphan")

class TypeVetement(Base):
    __tablename__ = "types_vetements"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100), nullable=False)
    categorie_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    genre_cible = Column(String(20), default="MIXTE")  # HOMME, FEMME, MIXTE
    est_couche_superieure = Column(Boolean, default=False)  # Pull, Veste, Manteau pour BR02

    categorie = relationship("Categorie", back_populates="types")

class Couleur(Base):
    __tablename__ = "couleurs"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(50), unique=True, nullable=False)
    code_hex = Column(String(10), nullable=False)

class StyleVestimentaire(Base):
    __tablename__ = "styles_vestimentaires"

    id = Column(Integer, primary_key=True, index=True)
    libelle = Column(String(50), unique=True, nullable=False)
