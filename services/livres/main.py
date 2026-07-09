from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models, schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Service Livres",
    description="Microservice de gestion des livres de la bibliothèque du DIT"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def accueil():
    return {"message": "Bienvenue sur le service Livres", "statut": "en ligne"}

# Ajouter un livre
@app.post("/livres", response_model=schemas.LivreResponse)
def ajouter_livre(livre: schemas.LivreCreate, db: Session = Depends(get_db)):
    existant = db.query(models.Livre).filter(models.Livre.isbn == livre.isbn).first()
    if existant:
        raise HTTPException(status_code=400, detail="Un livre avec cet ISBN existe déjà")
    nouveau = models.Livre(**livre.model_dump())
    db.add(nouveau)
    db.commit()
    db.refresh(nouveau)
    return nouveau

# Lister les livres
@app.get("/livres", response_model=list[schemas.LivreResponse])
def lister_livres(db: Session = Depends(get_db)):
    return db.query(models.Livre).all()

# Rechercher (par titre, auteur ou ISBN)
@app.get("/livres/recherche", response_model=list[schemas.LivreResponse])
def rechercher_livres(q: str, db: Session = Depends(get_db)):
    return db.query(models.Livre).filter(
        models.Livre.titre.ilike(f"%{q}%")
        | models.Livre.auteur.ilike(f"%{q}%")
        | models.Livre.isbn.ilike(f"%{q}%")
    ).all()

# Modifier un livre
@app.put("/livres/{livre_id}", response_model=schemas.LivreResponse)
def modifier_livre(livre_id: int, livre: schemas.LivreCreate, db: Session = Depends(get_db)):
    existant = db.query(models.Livre).filter(models.Livre.id == livre_id).first()
    if not existant:
        raise HTTPException(status_code=404, detail="Livre introuvable")
    for champ, valeur in livre.model_dump().items():
        setattr(existant, champ, valeur)
    db.commit()
    db.refresh(existant)
    return existant

# Supprimer un livre
@app.delete("/livres/{livre_id}")
def supprimer_livre(livre_id: int, db: Session = Depends(get_db)):
    existant = db.query(models.Livre).filter(models.Livre.id == livre_id).first()
    if not existant:
        raise HTTPException(status_code=404, detail="Livre introuvable")
    db.delete(existant)
    db.commit()
    return {"message": f"Livre {livre_id} supprimé"}

# Consulter un livre par son id
@app.get("/livres/{livre_id}", response_model=schemas.LivreResponse)
def consulter_livre(livre_id: int, db: Session = Depends(get_db)):
    existant = db.query(models.Livre).filter(models.Livre.id == livre_id).first()
    if not existant:
        raise HTTPException(status_code=404, detail="Livre introuvable")
    return existant
