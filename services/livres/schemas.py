from pydantic import BaseModel

class LivreCreate(BaseModel):
    titre: str
    auteur: str
    isbn: str
    quantite: int = 1

class LivreResponse(BaseModel):
    id: int
    titre: str
    auteur: str
    isbn: str
    quantite: int

    class Config:
        from_attributes = True
    