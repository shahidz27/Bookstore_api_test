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
                    python -m venv jenkins_venv || echo "Virtualenv exists"
                    call jenkins_venv\\Scripts\\activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Start Server') {
            steps {
                script {
                    // Kill any existing Python processes
                    bat 'taskkill /f /im python.exe /t || echo "No processes to kill"'

                    // Start server with explicit host and port
                    bat '''
                        start /B python run.py --host 0.0.0.0 --port 5000 > server.log 2>&1
                        ping 127.0.0.1 -n 15 > nul
                    '''

                    // Debugging checks
                    bat 'type server.log'
                    bat 'netstat -ano | findstr 5000'
                    bat 'tasklist /fi "IMAGENAME eq python.exe"'
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
                bat 'taskkill /f /im python.exe /t || echo "Cleanup complete"'
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