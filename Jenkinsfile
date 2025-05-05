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
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt --force-reinstall || exit 1
                    python run.py
                    pip show flask
                    pip list
                '''
            }
        }

        stage('Verify Installation') {
            steps {
                bat '''
                    call jenkins_venv\\Scripts\\activate
                    python -c "import flask; print(f'Flask version: {flask.__version__}')"
                '''
            }
        }

        stage('Start Server') {
            steps {
                script {
                    // Kill previous Python processes (server cleanup)
                    bat 'taskkill /f /im python.exe /t 2>nul || echo "No python process to kill"'

                    // Start the Flask server in background
                    bat '''
                        call jenkins_venv\\Scripts\\activate
                        set FLASK_APP=run.py
                        start "BookstoreAPI" /B python -m flask run --host=0.0.0.0 --port=5000 > server.log 2>&1
                    '''

                    // Wait for server to become healthy
                    bat '''
                        call jenkins_venv\\Scripts\\activate
                        python -c "
import requests, time, sys
for i in range(10):
    try:
        res = requests.get('http://localhost:5000/health', timeout=5)
        if res.status_code == 200:
            print('✅ Health check passed')
            sys.exit(0)
    except Exception as e:
        print(f'⏳ Attempt {i+1}/10 failed: {e}')
    time.sleep(3)
print('❌ Server did not become healthy after 10 attempts')
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
                bat 'taskkill /f /im python.exe /t 2>nul || echo "Server already stopped"'
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
            bat 'netstat -ano | findstr :5000 || echo "No active service on port 5000"'
            bat 'call jenkins_venv\\Scripts\\activate && pip list'
        }
    }
}
