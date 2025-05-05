pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                url: 'https://github.com/shahidz27/Bookstore_api_test.git'
            }
        }

        stage('Setup') {
            steps {
                bat '''
                    python -m venv jenkins_venv
                    jenkins_venv\\Scripts\\pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                bat '''
                    set PYTHONPATH=%CD%
                    start /B jenkins_venv\\Scripts\\python run.py
                    timeout /T 5
                    jenkins_venv\\Scripts\\pytest --junitxml=test-results.xml ./test
                    taskkill /F /IM python.exe >nul 2>&1
                '''
            }
        }
    }

    post {
        always {
            junit 'test-results.xml'
            cleanWs()
        }
    }
}
