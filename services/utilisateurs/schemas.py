from typing import Literal
from pydantic import BaseModel

TypeUtilisateur = Literal["Etudiant", "Professeur", "Personnel administratif"]

class UtilisateurCreate(BaseModel):
    nom: str
    email: str
    type_utilisateur: TypeUtilisateur

class UtilisateurResponse(BaseModel):
    id: int
    nom: str
    email: str
    type_utilisateur: str

    class Config:
        from_attributes = True
