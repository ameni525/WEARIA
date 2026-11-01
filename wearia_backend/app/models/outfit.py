from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, Date, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.models.base import Base

tenue_vetements = Table(
    "tenue_vetements",
    Base.metadata,
    Column("tenue_id", Integer, ForeignKey("tenues.id", ondelete="CASCADE"), primary_key=True),
    Column("vetement_id", Integer, ForeignKey("vetements.id", ondelete="CASCADE"), primary_key=True)
)

class Tenue(Base):
    __tablename__ = "tenues"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("utilisateurs.id"), nullable=False)
    date_creation = Column(DateTime, default=datetime.utcnow)
    date_prevue = Column(Date, nullable=True)
    date_portee = Column(DateTime, nullable=True)
    occasion = Column(String(30), default="QUOTIDIEN")
    temperature_celsius = Column(Float, nullable=True)
    precipitations = Column(Boolean, default=False)
    description_meteo = Column(String(100), default="Ensoleillé")
    explication = Column(String(500), nullable=True)
    score_compatibilite = Column(Integer, default=85)  # Sur 100
    est_generee = Column(Boolean, default=True)
    est_favorite = Column(Boolean, default=False)

    utilisateur = relationship("Utilisateur", back_populates="tenues")
    vetements = relationship("Vetement", secondary=tenue_vetements)
    feedback = relationship("Feedback", back_populates="tenue", uselist=False, cascade="all, delete-orphan")

class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    tenue_id = Column(Integer, ForeignKey("tenues.id"), nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey("utilisateurs.id"), nullable=False)
    appreciation = Column(String(20), nullable=False)  # AIME, MOYEN, PAS_POUR_MOI
    motif_rejet = Column(String(200), nullable=True)
    date_feedback = Column(DateTime, default=datetime.utcnow)

    tenue = relationship("Tenue", back_populates="feedback")
