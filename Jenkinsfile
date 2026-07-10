pipeline {
    agent any

    stages {
        stage('Recuperation du code') {
            steps {
                echo 'Code recupere depuis GitHub'
                sh 'ls -la'
            }
        }

        stage('Construction des images Docker') {
            steps {
                echo 'Build des images de tous les services'
                sh 'docker compose -p bibliotheque-dit build'
            }
        }

        stage('Deploiement') {
            steps {
                echo 'Deploiement avec Docker Compose'
                sh 'docker compose -p bibliotheque-dit up -d'
            }
        }

        stage('Verification') {
            steps {
                echo 'Controle des conteneurs en cours'
                sh 'docker ps'
            }
        }
    }

    post {
        success {
            echo 'Pipeline termine avec succes - application deployee !'
        }
        failure {
            echo 'Echec du pipeline - consulter les logs ci-dessus'
        }
    }
}
