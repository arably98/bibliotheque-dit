from sqlalchemy import Column, Integer, DateTime
from database import Base

class Emprunt(Base):
    __tablename__ = "emprunts"

    id = Column(Integer, primary_key=True, index=True)
    livre_id = Column(Integer, nullable=False, index=True)
    utilisateur_id = Column(Integer, nullable=False, index=True)
    date_emprunt = Column(DateTime, nullable=False)
    date_retour_prevue = Column(DateTime, nullable=False)
    date_retour_effective = Column(DateTime, nullable=True)
    