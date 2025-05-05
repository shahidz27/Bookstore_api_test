pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python') {
            steps {
                bat '''
                    python -m venv jenkins_venv || echo "Virtualenv already exists"
                    call jenkins_venv\\Scripts\\activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pip list
                '''
            }
        }

        stage('Verify Server Connection') {
            steps {
                script {
                    // First check if server is running
                    def serverUp = bat(
                        script: '@call jenkins_venv\\Scripts\\activate && python -c "import requests; requests.get(\'http://localhost:5000/health\', timeout=5).raise_for_status()"',
                        returnStatus: true
                    ) == 0

                    if (!serverUp) {
                        error("""
                        Server not detected at http://localhost:5000
                        Please manually start the server first with:
                        python run.py
                        The server must be running before tests can execute.
                        """)
                    }
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
    }

    post {
        always {
            junit 'test-results.xml'
            archiveArtifacts artifacts: 'test-results.xml', allowEmptyArchive: true
        }
        failure {
            echo """
            TEST FAILURE ANALYSIS:
            1. Verify your Flask server is running: python run.py
            2. Check endpoint manually: curl http://localhost:5000/health
            3. Confirm BASE_URL in tests matches your running server
            """
            bat 'netstat -ano | findstr :5000 || echo "No process found on port 5000"'
        }
    }
}