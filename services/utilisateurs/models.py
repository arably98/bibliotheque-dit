from sqlalchemy import Column, Integer, String
from database import Base

class Utilisateur(Base):
    __tablename__ = "utilisateurs"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    type_utilisateur = Column(String, nullable=False)
