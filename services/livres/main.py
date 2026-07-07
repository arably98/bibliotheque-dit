from fastapi import FastAPI

app = FastAPI(
    title="Service Livres",
    description="Microservice de gestion des livres de la bibliothèque du DIT"
)

@app.get("/")
def accueil():
    return {"message": "Bienvenue sur le service Livres", "statut": "en ligne"}