pipeline {
    agent any

    triggers {
        githubPush()
        // pollSCM('H/5 * * * *')  // Uncomment if you want periodic polling
    }

    stages {
        stage('Checkout & Setup') {
            steps {
                checkout scm
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
                    // Start server in background
                    bat 'start /B python run.py > server.log 2>&1'
                    // Wait for server to start (Windows alternative to sleep)
                    bat 'ping 127.0.0.1 -n 10 > nul'  // 10 second delay
                    // Verify server is running
                    bat 'type server.log'
                    bat 'tasklist | findstr python.exe || echo "Python process not found"'
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
                    bat 'taskkill /f /im python.exe /t || echo "No Python process to kill"'
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