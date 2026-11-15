pipeline {
    agent any

    environment {
        PYTHONUNBUFFERED = '1'
        PYTHONDONTWRITEBYTECODE = '1'
        MODEL_PROVIDER = 'google'
        HOST = '127.0.0.1'
        PORT = '8000'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
                checkout scm
            }
        }

        stage('Environment & Dependencies') {
            steps {
                echo 'Setting up Python virtual environment and installing dependencies...'
                sh '''
                    python3 -m venv .venv || virtualenv .venv
                    . .venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Code Compilation & Lint') {
            steps {
                echo 'Running Python syntax and import compilation check...'
                sh '''
                    . .venv/bin/activate
                    python -m py_compile app/config.py app/schemas.py app/main.py streamlit_app.py
                    python -m py_compile app/agents/medical_team.py app/agents/tools.py app/data/sample_documents.py
                '''
            }
        }

        stage('Run Automated Tests') {
            steps {
                echo 'Executing Pytest test suite for medical agents and endpoints...'
                sh '''
                    . .venv/bin/activate
                    pytest -v --junitxml=test-results.xml tests/
                '''
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'test-results.xml'
                }
            }
        }

        stage('Build Docker Containers') {
            steps {
                echo 'Building production Docker images via Docker Compose...'
                sh '''
                    docker compose build
                '''
            }
        }

        stage('Container Smoke Test') {
            steps {
                echo 'Verifying container startup and health check endpoint...'
                sh '''
                    docker compose up -d
                    sleep 10
                    curl -f http://localhost:8000/health || exit 1
                    docker compose down
                '''
            }
        }
    }

    post {
        success {
            echo '=== MediResearch AI Jenkins Build Succeeded! ==='
        }
        failure {
            echo '=== MediResearch AI Jenkins Build Failed! ==='
        }
        always {
            cleanWs deleteDirs: true, notFailBuild: true
        }
    }
}
