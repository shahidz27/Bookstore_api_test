pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Environment') {
            steps {
                bat '''
                    python -m venv jenkins_venv || exit /b 1
                    call jenkins_venv\\Scripts\\activate
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt --force-reinstall
                '''
            }
        }

        stage('Start Server') {
            steps {
                script {
                    bat 'taskkill /f /im python.exe /t 2>nul || exit /b 0'

                    bat '''
                        call jenkins_venv\\Scripts\\activate
                        start /B python run.py
                    '''

                    bat '''
                        call jenkins_venv\\Scripts\\activate
                        python -c "
import requests, time, sys
for _ in range(10):
    try:
        if requests.get('http://localhost:5000/health').status_code == 200:
            sys.exit(0)
    except: pass
    time.sleep(2)
sys.exit(1)
                        "
                    '''
                }
            }
        }

        stage('Run Tests') {
            steps {
                bat '''
                    call jenkins_venv\\Scripts\\activate
                    pytest --junitxml=test-results.xml ./test
                '''
            }
        }

        stage('Stop Server') {
            steps {
                bat 'taskkill /f /im python.exe /t 2>nul || exit /b 0'
            }
        }
    }

    post {
        always {
            junit 'test-results.xml'
            archiveArtifacts artifacts: 'server.log', allowEmptyArchive: true
            cleanWs()
        }
    }
}
