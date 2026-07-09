pipeline {
    agent any

    stages {
        stage('Récupération du code') {
            steps {
                echo 'Code récupéré depuis GitHub'
                sh 'ls -la'
            }
        }

        stage('Construction des images Docker') {
            steps {
                echo 'Build des images de tous les services'
                sh 'docker compose build'
            }
        }

        stage('Déploiement') {
            steps {
                echo 'Déploiement avec Docker Compose'
                sh 'docker compose up -d'
            }
        }

        stage('Vérification') {
            steps {
                echo 'Contrôle des conteneurs en cours'
                sh 'docker ps'
            }
        }
    }

    post {
        success {
            echo 'Pipeline terminé avec succès — application déployée !'
        }
        failure {
            echo 'Échec du pipeline — consulter les logs ci-dessus'
        }
    }
}
