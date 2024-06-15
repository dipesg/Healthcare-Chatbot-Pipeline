pipeline {
    agent any
    environment {
        REPOSITORY_URL = 'https://github.com/dipesg/Healthcare-Chatbot-Pipeline' 
    stages {
        stage('Checkout') {
            steps {
                script {
                    if (!fileExists('Healthcare-Chatbot-Pipeline')) {
                        sh "git clone ${REPOSITORY_URL}"
                    } else {
                        dir('Healthcare-Chatbot-Pipeline') {
                            sh "git pull"
                        }
                    }
                }
            }
        }

        stage('Deploy to container') {
            steps {
                dir('Healthcare-Chatbot-Pipeline') {
                    sh "sudo docker-compose up --build --detach"
                }
            }
        }
    }
}
