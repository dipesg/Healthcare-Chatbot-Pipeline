// pipeline {
//     agent any
//     environment {
//         REPOSITORY_URL = 'https://github.com/dipesg/Healthcare-Chatbot-Pipeline'
//         TARGET_EC2_USER = 'ubuntu'
//         TARGET_EC2_IP = 'ec2-13-51-106-7.eu-north-1.compute.amazonaws.com'
//         SSH_KEY_PATH = '/home/ubuntu/chatbot-jenkins-key.pem'  // Adjust the path as needed
//     }
//     stages {
//         stage('Deploy to EC2') {
//             steps {
//                 script {
//                     sshagent(['your-ssh-credential-id']) {
//                         // Deploy the application
//                         bat """
//                             ssh -o StrictHostKeyChecking=no -i ${SSH_KEY_PATH} ${TARGET_EC2_USER}@${TARGET_EC2_IP} "
//                             if [ ! -d Healthcare-Chatbot-Pipeline ]; then
//                                 git clone ${REPOSITORY_URL}
//                             else
//                                 cd Healthcare-Chatbot-Pipeline && git pull
//                             fi
//                             cd Healthcare-Chatbot-Pipeline
//                             sudo docker-compose down
//                             sudo docker-compose up --build -d
//                             "
//                         """
//                     }
//                 }
//             }
//         }
//     }
// }

// pipeline {
//     agent any

//     environment {
//         // Define environment variables
//         REPO_URL = 'https://github.com/dipesg/Healthcare-Chatbot-Pipeline.git'
//         BRANCH = 'main' 
//     }

//     stages {
//         stage('Clone Repository') {
//             steps {
//                 // Clone the GitHub repository
//                 git clone ${REPO_URL}
//             }
//         }
        
//         stage('Run Docker Compose') {
//             steps {
//                 script {
//                     // Run Docker Compose with sudo
//                     sh 'sudo docker-compose up --build'
//                 }
//             }
//         }
//     }

//     post {
//         always {
//             // Cleanup or post actions can be added here
//             echo 'Pipeline finished.'
//         }
//     }
// }

pipeline {
    agent any

    environment {
        // Define environment variables
        REPO_URL = 'https://github.com/dipesg/Healthcare-Chatbot-Pipeline.git'
        BRANCH = 'main' // Change to your desired branch if necessary
    }

    stages {
        stage('Clone Repository') {
            steps {
                // Clone the GitHub repository
                git branch: "${BRANCH}", url: "${REPO_URL}"
            }
        }
        
        stage('Run Docker Compose') {
            steps {
                script {
                    // Run Docker Compose with sudo
                    sh 'docker-compose up --build'
                }
            }
        }
    }

    post {
        always {
            // Cleanup or post actions can be added here
            echo 'Pipeline finished.'
        }
    }
}


