pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup') {
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
                    // Start server in background and log output
                    bat 'start /B python run.py > server.log 2>&1'
                    // Wait 10 seconds for server to start (Windows)
                    bat 'ping 127.0.0.1 -n 10 > nul'
                    // Verify server is running
                    bat 'tasklist | findstr python.exe || exit 1'
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
                script {
                    // Kill all Python processes
                    bat 'taskkill /f /im python.exe /t || echo "No Python processes to kill"'
                }
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