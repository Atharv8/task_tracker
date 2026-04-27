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
                sh "docker build -t ${IMAGE_NAME}:latest ."
            }
        }

        stage('Start Test Environment') {
            steps {
                // Run the container in the background to test against it
                sh "docker run -d --name ${CONTAINER_NAME} -p 5000:5000 ${IMAGE_NAME}:latest"
                // Give Flask a second to start
                sleep 5
            }
        }

        stage('Run Selenium Tests') {
            steps {
                // Install dependencies for testing
                sh "pip3 install -r requirements.txt"
                // Run the test script
                sh "python3 test_app.py"
            }
            post {
                always {
                    // Tear down the test container whether tests pass or fail
                    sh "docker stop ${CONTAINER_NAME} || true"
                    sh "docker rm ${CONTAINER_NAME} || true"
                }
            }
        }

        stage('Push Image to Minikube') {
            steps {
                // Loads the locally built Docker image directly into Minikube's registry
                sh "minikube image load ${IMAGE_NAME}:latest"
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                // Apply the storage and deployment manifests
                sh "kubectl apply -f k8s/database-storage.yaml"
                sh "kubectl apply -f k8s/deployment.yaml"
                
                // Rollout restart ensures K8s pulls the newly loaded image
                sh "kubectl rollout restart deployment task-tracker-deploy"
            }
        }
    }
}
