pipeline {
    agent any
    environment {
        IMAGE_NAME = 'book-exchange-portal'
        IMAGE_TAG = 'latest'
    }
    stages {
        stage('Checkout') {
            steps { checkout scm }
        }
        stage('Build Docker Image') {
            steps { sh 'docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .' }
        }
        stage('Deploy to Kubernetes') {
            steps {
                sh 'kubectl apply -f k8s/deployment.yaml'
                sh 'kubectl apply -f k8s/service.yaml'
                sh 'kubectl rollout status deployment/book-exchange --timeout=120s'
            }
        }
    }
    post {
        success { echo 'BookLoop build and Kubernetes deployment completed.' }
        failure { echo 'Pipeline failed. Review the stage logs and tool configuration.' }
    }
}
