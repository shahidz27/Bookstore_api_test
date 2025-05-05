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
                    python -m venv jenkins_venv || echo "Virtualenv exists"
                    call jenkins_venv\\Scripts\\activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Start Server') {
            steps {
                script {
                    // Kill any existing processes
                    bat 'taskkill /f /im python.exe /t 2>nul || echo "No processes to kill"'

                    // Check port availability
                    bat 'netstat -ano | findstr :5000 && exit 1 || echo "Port 5000 available"'

                    // Start server with logging
                    bat '''
                        set FLASK_APP=run.py
                        start "BookstoreAPI" /B python -m flask run --host=0.0.0.0 --port=5000 > server.log 2>&1
                    '''

                    // Progressive health checks
                    bat '''
                        call jenkins_venv\\Scripts\\activate
                        python -c "
                        import requests, time
                        for _ in range(10):
                            try:
                                response = requests.get('http://localhost:5000/health', timeout=5)
                                if response.status_code == 200:
                                    print('Server is healthy!')
                                    exit(0)
                            except Exception as e:
                                print(f'Waiting for server... ({e})')
                                time.sleep(3)
                        print('Server failed to start!')
                        exit(1)
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
                script {
                    bat 'taskkill /f /im python.exe /t 2>nul || echo "Cleanup completed"'
                    bat 'type server.log'
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
        failure {
            bat 'type server.log'
            bat 'netstat -ano | findstr :5000'
        }
    }
}