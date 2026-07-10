# 📚 Bibliothèque Numérique du DIT

Plateforme web de gestion de bibliothèque en **architecture microservices**, développée dans le cadre de l'examen pratique DevOps (Master 1 IA, Dakar Institute of Technology).

## Architecture

L'application est composée de 5 conteneurs orchestrés par Docker Compose :

| Composant | Technologie | Port | Rôle |
|---|---|---|---|
| Frontend | HTML/CSS/JS + Nginx | 8080 | Interface web |
| Service Livres | FastAPI (Python) | 8001 | CRUD et recherche des livres |
| Service Utilisateurs | FastAPI (Python) | 8002 | Gestion des utilisateurs et types |
| Service Emprunts | FastAPI (Python) | 8003 | Emprunts, retours, détection des retards |
| Base de données | PostgreSQL 16 | 5432 | Stockage persistant |

Les services communiquent entre eux via **API REST** : le service Emprunts vérifie l'existence des livres et utilisateurs en appelant les deux autres services par HTTP (réseau interne Docker).

## Installation et lancement

### Prérequis
- Docker et Docker Compose installés
- Git

### Démarrage

```bash
# 1. Cloner le dépôt
git clone https://github.com/arably98/bibliotheque-dit.git
cd bibliotheque-dit

# 2. Lancer toute l'application
docker compose up -d --build

# 3. Vérifier que les 5 conteneurs tournent
docker ps
```

### Accès
- **Interface web** : http://localhost:8080
- **API Livres (doc interactive)** : http://localhost:8001/docs
- **API Utilisateurs** : http://localhost:8002/docs
- **API Emprunts** : http://localhost:8003/docs

## Pipeline CI/CD (Jenkins)

Le pipeline est défini dans le `Jenkinsfile` à la racine et comporte 4 étapes :

1. **Récupération du code** — clone du dépôt GitHub
2. **Construction des images Docker** — `docker compose build` des 4 images
3. **Déploiement** — `docker compose up -d` (idempotent grâce au nom de projet explicite `-p`)
4. **Vérification** — contrôle des conteneurs en cours d'exécution

### Lancer Jenkins

```bash
docker run -d --name jenkins \
  -p 8090:8080 \
  -v jenkins_data:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v /usr/bin/docker:/usr/bin/docker \
  -v /usr/libexec/docker/cli-plugins/docker-compose:/usr/local/lib/docker/cli-plugins/docker-compose \
  -u root \
  jenkins/jenkins:lts
```

Puis créer un job **Pipeline** pointant vers ce dépôt (branche `main`, script `Jenkinsfile`) et cliquer sur **Build Now**.

## Structure du projet
bibliotheque-dit/
├── docker-compose.yml      # Orchestration des 5 conteneurs
├── Jenkinsfile             # Pipeline CI/CD
├── frontend/               # Interface web (nginx)
│   ├── Dockerfile
│   ├── index.html
│   ├── style.css
│   └── app.js
└── services/
├── livres/             # Microservice Livres
│   ├── Dockerfile
│   ├── main.py         # Endpoints FastAPI
│   ├── models.py       # Table SQLAlchemy
│   ├── schemas.py      # Validation Pydantic
│   ├── database.py     # Connexion PostgreSQL
│   └── requirements.txt
├── utilisateurs/       # Microservice Utilisateurs (même structure)
└── emprunts/           # Microservice Emprunts (même structure + appels HTTP inter-services)
