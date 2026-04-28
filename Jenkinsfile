pipeline {
    agent any

    environment {
        IMAGE_NAME = "task-tracker"
        CONTAINER_NAME = "task-tracker-test"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

       stage('Build Docker Image') {
            steps {
                echo 'Building the Docker Image...'
                // Use the Jenkins BUILD_ID to create a unique tag
                sh "docker build -t task-tracker:${env.BUILD_ID} ."
            }
        }

        stage('Start Test Environment') {
            steps {
                echo 'Starting temporary container for testing...'
                // Start the container using the unique tag
                sh "docker run -d --name ${CONTAINER_NAME} -p 5000:5000 task-tracker:${env.BUILD_ID}"
                sleep 5
            }
        }

        stage('Run Selenium Tests') {
            // (Keep your existing venv and test steps here)
            steps {
                sh '''
                    python3 -m venv test_env
                    test_env/bin/pip install -r requirements.txt
                    test_env/bin/python test_app.py
                '''
            }
            post {
                always {
                    sh "docker stop ${CONTAINER_NAME} || true"
                    sh "docker rm ${CONTAINER_NAME} || true"
                }
            }
        }

        stage('Push Image to Minikube') {
            steps {
                echo 'Loading image into Minikube...'
                // Push the uniquely tagged image
                sh "minikube image load task-tracker:${env.BUILD_ID}"
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo 'Applying Kubernetes Manifests...'
                
                // NEW LINE: This finds 'task-tracker:latest' in your deployment.yaml 
                // and replaces it with 'task-tracker:5' (or whatever the build ID is)
                sh "sed -i 's/image: task-tracker:latest/image: task-tracker:${env.BUILD_ID}/g' k8s/deployment.yaml"
                
                sh 'kubectl apply -f k8s/deployment.yaml'
                sh 'kubectl apply -f k8s/service.yaml'
                // Removed the rollout restart line, as changing the image tag automatically triggers a rollout!
            }
        }
    }
}
