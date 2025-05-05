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
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt --force-reinstall
                    pip list  # Debug: Show installed packages
                '''
            }
        }

        stage('Verify Installation') {
            steps {
                bat '''
                    call jenkins_venv\\Scripts\\activate
                    python -c "import flask; print(f'Flask version: {flask.__version__}')" || exit 1
                '''
            }
        }

        stage('Start Server') {
            steps {
                script {
                    // Clean up any existing processes
                    bat 'taskkill /f /im python.exe /t 2>nul || echo "No processes to kill"'

                    // Start server within the virtualenv
                    bat '''
                        call jenkins_venv\\Scripts\\activate
                        set FLASK_APP=run.py
                        start "BookstoreAPI" /B python -m flask run --host=0.0.0.0 --port=5000 > server.log 2>&1
                    '''

                    // Progressive health checks with virtualenv activation
                    bat '''
                        call jenkins_venv\\Scripts\\activate
                        python -c "
                        import requests, time
                        for i in range(10):
                            try:
                                response = requests.get('http://localhost:5000/health', timeout=5)
                                if response.status_code == 200:
                                    print('Server health check passed!')
                                    exit(0)
                            except Exception as e:
                                print(f'Attempt {i+1}/10: Server not ready yet ({str(e)})')
                                time.sleep(3)
                        print('Health check failed after 10 attempts')
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
        failure {
            bat 'type server.log'
            bat 'netstat -ano | findstr :5000 || echo "No process on port 5000"'
            bat 'pip list || echo "Pip list failed"'
        }
    }
}