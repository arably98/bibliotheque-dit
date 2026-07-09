from datetime import datetime
from pydantic import BaseModel

class EmpruntCreate(BaseModel):
    livre_id: int
    utilisateur_id: int

class EmpruntResponse(BaseModel):
    id: int
    livre_id: int
    utilisateur_id: int
    date_emprunt: datetime
    date_retour_prevue: datetime
    date_retour_effective: datetime | None
    en_retard: bool = False

    class Config:
        from_attributes = True