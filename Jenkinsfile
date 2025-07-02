pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'cleansync-app'
        DOCKER_TAG = "${env.BUILD_NUMBER}"
        CONTAINER_NAME = 'cleansync-container'
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out code from repository...'
                checkout scm
            }
        }
        
        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies...'
                sh '''
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install pytest pytest-cov
                '''
            }
        }
        
        stage('Code Quality Check') {
            steps {
                echo 'Running code quality checks...'
                sh '''
                    pip install flake8 pylint
                    flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
                    flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
                '''
            }
        }
        
        stage('Unit Tests') {
            steps {
                echo 'Running unit tests...'
                sh '''
                    python -m pytest CleanSync/test_autoclean.py -v --cov=CleanSync --cov-report=html
                '''
            }
            post {
                always {
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'htmlcov',
                        reportFiles: 'index.html',
                        reportName: 'Coverage Report'
                    ])
                }
            }
        }
        
        stage('Integration Tests') {
            steps {
                echo 'Running integration tests...'
                sh '''
                    python example.py
                    python clean_my_data.py sample_data.csv
                '''
            }
        }
        
        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                sh '''
                    docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .
                    docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest
                '''
            }
        }
        
        stage('Docker Security Scan') {
            steps {
                echo 'Running Docker security scan...'
                sh '''
                    docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
                        -v /tmp/.cache:/root/.cache/ aquasec/trivy image ${DOCKER_IMAGE}:${DOCKER_TAG}
                '''
            }
        }
        
        stage('Deploy to Test Environment') {
            steps {
                echo 'Deploying to test environment...'
                sh '''
                    # Stop and remove existing container
                    docker stop ${CONTAINER_NAME} || true
                    docker rm ${CONTAINER_NAME} || true
                    
                    # Run new container
                    docker run -d --name ${CONTAINER_NAME} \
                        -p 5000:5000 \
                        -v $(pwd)/uploads:/app/uploads \
                        -v $(pwd)/logs:/app/logs \
                        ${DOCKER_IMAGE}:${DOCKER_TAG}
                    
                    # Wait for application to start
                    sleep 10
                    
                    # Health check
                    curl -f http://localhost:5000/ || exit 1
                '''
            }
        }
        
        stage('Performance Test') {
            steps {
                echo 'Running performance tests...'
                sh '''
                    # Simple load test
                    for i in {1..10}; do
                        curl -s http://localhost:5000/ > /dev/null
                    done
                '''
            }
        }
    }
    
    post {
        always {
            echo 'Cleaning up...'
            sh '''
                docker stop ${CONTAINER_NAME} || true
                docker rm ${CONTAINER_NAME} || true
                docker rmi ${DOCKER_IMAGE}:${DOCKER_TAG} || true
            '''
        }
        success {
            echo 'Pipeline completed successfully!'
            emailext (
                subject: "CleanSync Build #${env.BUILD_NUMBER} - SUCCESS",
                body: "Build completed successfully. Docker image: ${DOCKER_IMAGE}:${DOCKER_TAG}",
                recipientProviders: [[$class: 'DevelopersRecipientProvider']]
            )
        }
        failure {
            echo 'Pipeline failed!'
            emailext (
                subject: "CleanSync Build #${env.BUILD_NUMBER} - FAILED",
                body: "Build failed. Check Jenkins console for details.",
                recipientProviders: [[$class: 'DevelopersRecipientProvider']]
            )
        }
    }
} 