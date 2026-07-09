from datetime import datetime, timedelta
import os
import httpx
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models, schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)


URL_SERVICE_LIVRES = os.getenv("URL_SERVICE_LIVRES", "http://localhost:8001")
URL_SERVICE_UTILISATEURS = os.getenv("URL_SERVICE_UTILISATEURS", "http://localhost:8002")
DUREE_EMPRUNT_JOURS = 14

app = FastAPI(
    title="Service Emprunts",
    description="Microservice de gestion des emprunts de la bibliothèque du DIT"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def ajouter_statut_retard(emprunt):
    emprunt.en_retard = (
        emprunt.date_retour_effective is None
        and datetime.now() > emprunt.date_retour_prevue
    )
    return emprunt

@app.get("/")
def accueil():
    return {"message": "Bienvenue sur le service Emprunts", "statut": "en ligne"}

# 1. Emprunter un livre
@app.post("/emprunts", response_model=schemas.EmpruntResponse)
def emprunter_livre(emprunt: schemas.EmpruntCreate, db: Session = Depends(get_db)):
    # Vérification auprès du service Livres
    try:
        reponse_livre = httpx.get(f"{URL_SERVICE_LIVRES}/livres/{emprunt.livre_id}")
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Service Livres injoignable")
    if reponse_livre.status_code == 404:
        raise HTTPException(status_code=404, detail="Livre introuvable")

    # Vérification auprès du service Utilisateurs
    try:
        reponse_utilisateur = httpx.get(f"{URL_SERVICE_UTILISATEURS}/utilisateurs/{emprunt.utilisateur_id}")
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Service Utilisateurs injoignable")
    if reponse_utilisateur.status_code == 404:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    maintenant = datetime.now()
    nouveau = models.Emprunt(
        livre_id=emprunt.livre_id,
        utilisateur_id=emprunt.utilisateur_id,
        date_emprunt=maintenant,
        date_retour_prevue=maintenant + timedelta(days=DUREE_EMPRUNT_JOURS),
    )
    db.add(nouveau)
    db.commit()
    db.refresh(nouveau)
    return ajouter_statut_retard(nouveau)

# 2. Retourner un livre
@app.put("/emprunts/{emprunt_id}/retour", response_model=schemas.EmpruntResponse)
def retourner_livre(emprunt_id: int, db: Session = Depends(get_db)):
    emprunt = db.query(models.Emprunt).filter(models.Emprunt.id == emprunt_id).first()
    if not emprunt:
        raise HTTPException(status_code=404, detail="Emprunt introuvable")
    if emprunt.date_retour_effective is not None:
        raise HTTPException(status_code=400, detail="Ce livre a déjà été retourné")
    emprunt.date_retour_effective = datetime.now()
    db.commit()
    db.refresh(emprunt)
    return ajouter_statut_retard(emprunt)

# 3. Historique des emprunts
@app.get("/emprunts", response_model=list[schemas.EmpruntResponse])
def historique_emprunts(db: Session = Depends(get_db)):
    emprunts = db.query(models.Emprunt).all()
    return [ajouter_statut_retard(e) for e in emprunts]

# 4. Détection des retards
@app.get("/emprunts/retards", response_model=list[schemas.EmpruntResponse])
def emprunts_en_retard(db: Session = Depends(get_db)):
    emprunts = db.query(models.Emprunt).filter(
        models.Emprunt.date_retour_effective.is_(None),
        models.Emprunt.date_retour_prevue < datetime.now(),
    ).all()
    return [ajouter_statut_retard(e) for e in emprunts]
    