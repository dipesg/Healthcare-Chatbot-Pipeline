pipeline{
    agent any

        stage('Deploy to container'){
            steps{
                sh 'docker run -d --name chatbot -p 3000:3000 sreedhar8897/chatbot:latest'
            }
        }
   }
}