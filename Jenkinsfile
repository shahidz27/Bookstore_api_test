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
                    python -m venv jenkins_venv || echo "Virtualenv already exists"
                    call jenkins_venv\\Scripts\\activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Start Server') {
            steps {
                script {
                    // Clean up any existing processes
                    bat 'taskkill /f /im python.exe /t 2>nul || echo "No existing processes to kill"'

                    // Start server with explicit host and port
                    bat '''
                        set FLASK_APP=run.py
                        start "BookstoreAPI" /B python -m flask run --host=0.0.0.0 --port=5000 > server.log 2>&1
                    '''

                    // Wait for server to start (20 seconds)
                    bat 'ping -n 20 127.0.0.1 > nul'

                    // Verify server is running
                    bat '''
                        call jenkins_venv\\Scripts\\activate
                        python -c "import requests; requests.get('http://localhost:5000/health').raise_for_status()" || exit 1
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
                bat 'taskkill /f /im python.exe /t 2>nul || echo "Cleanup completed"'
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