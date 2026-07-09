from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models, schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Service Utilisateurs",
    description="Microservice de gestion des utilisateurs de la bibliothèque du DIT"
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
    return {"message": "Bienvenue sur le service Utilisateurs", "statut": "en ligne"}

@app.post("/utilisateurs", response_model=schemas.UtilisateurResponse)
def creer_utilisateur(utilisateur: schemas.UtilisateurCreate, db: Session = Depends(get_db)):
    existant = db.query(models.Utilisateur).filter(models.Utilisateur.email == utilisateur.email).first()
    if existant:
        raise HTTPException(status_code=400, detail="Un utilisateur avec cet email existe déjà")
    nouveau = models.Utilisateur(**utilisateur.model_dump())
    db.add(nouveau)
    db.commit()
    db.refresh(nouveau)
    return nouveau

@app.get("/utilisateurs", response_model=list[schemas.UtilisateurResponse])
def lister_utilisateurs(db: Session = Depends(get_db)):
    return db.query(models.Utilisateur).all()

@app.get("/utilisateurs/{utilisateur_id}", response_model=schemas.UtilisateurResponse)
def profil_utilisateur(utilisateur_id: int, db: Session = Depends(get_db)):
    existant = db.query(models.Utilisateur).filter(models.Utilisateur.id == utilisateur_id).first()
    if not existant:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    return existant
