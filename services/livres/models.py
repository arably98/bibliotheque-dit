from sqlalchemy import Column, Integer, String
from database import Base

class Livre(Base):
    __tablename__ = "livres"

    id = Column(Integer, primary_key=True, index=True)
    titre = Column(String, nullable=False)
    auteur = Column(String, nullable=False)
    isbn = Column(String, unique=True, index=True)
    quantite = Column(Integer, default=1)