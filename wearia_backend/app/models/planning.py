from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.models.base import Base

class RoutineHebdomadaire(Base):
    __tablename__ = "routines_hebdomadaires"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("utilisateurs.id"), nullable=False)
    jour_semaine = Column(String(20), nullable=False)  # LUNDI, MARDI, MERCREDI, etc.
    occasion = Column(String(30), default="UNIVERSITE")  # UNIVERSITE, TRAVAIL, SORTIE, SPORT, QUOTIDIEN
    est_active = Column(Boolean, default=True)

    utilisateur = relationship("Utilisateur", back_populates="routines")

    # Contrainte: une seule routine par jour et utilisateur
    __table_args__ = (UniqueConstraint("user_id", "jour_semaine", name="uq_user_day_routine"),)

class Evenement(Base):
    __tablename__ = "evenements"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("utilisateurs.id"), nullable=False)
    titre = Column(String(150), nullable=False)
    date = Column(Date, nullable=False)
    occasion = Column(String(30), default="EVENEMENT")

    utilisateur = relationship("Utilisateur", back_populates="evenements")
