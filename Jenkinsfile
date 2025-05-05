pipeline {
    agent any

    // Automatic triggers (choose one)
    triggers {
        githubPush()  // Requires GitHub webhook setup
        // OR poll SCM periodically
        // pollSCM('H/5 * * * *')  // Every 5 minutes
    }

    stages {
        stage('Checkout & Setup') {
            steps {
                checkout scm
                bat '''
                    python -m venv jenkins_venv || true
                    call jenkins_venv\\Scripts\\activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Start Server') {
            steps {
                script {
                    // Start server and store PID
                    bat 'start /B python run.py > server.log 2>&1'
                    // Verify server is up
                    bat 'timeout /t 10 /nobreak'  // Windows wait
                    bat 'type server.log'  // Debug logs
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
                    // Windows process termination
                    bat 'taskkill /f /im python.exe /t || echo "No Python process found"'
                }
            }
        }
    }

    post {
        always {
            junit 'test-results.xml'  // Publish test results
            archiveArtifacts artifacts: 'server.log', allowEmptyArchive: true
            cleanWs()  // Clean workspace
        }
    }
}