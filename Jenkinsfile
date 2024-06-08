pipeline {
    agent any
    environment {
        REPOSITORY_URL = 'https://github.com/dipesg/Healthcare-Chatbot-Pipeline' // Replace with your actual repository URL
    }
    stages {
        stage('Checkout') {
            steps {
                script {
                    // Check if the repository directory already exists
                    if (!fileExists('Healthcare-Chatbot-Pipeline')) {
                        // Clone the repository if the directory doesn't exist
                        sh "git clone ${REPOSITORY_URL}"
                    } else {
                        // Pull the latest changes if the directory already exists
                        echo "Repository directory already exists. Updating..."
                        sh "cd Healthcare-Chatbot-Pipeline && git pull"
                    }
                }
            }
        }

        stage('Deploy to container') {
            steps {
                dir('Healthcare-Chatbot-Pipeline') {
                    // Run Docker Compose to build and start the container
                    sh "docker-compose up --build"
                }
            }
        }
    }
}
