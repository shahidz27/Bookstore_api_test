
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                url: 'https://github.com/shahidz27/Bookstore_api_test.git'
            }
        }

        stage('Setup') {
            steps {
                bat '''
                    python -m venv jenkins_venv
                    jenkins_venv\\Scripts\\pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                bat '''
                  set PYTHONPATH=%CD%
                  jenkins_venv\\Scripts\\pytest --junitxml=test-results.xml ./test
                '''
            }
        }
    }

    post {
        always {
            junit 'test-results.xml'
            cleanWs()
        }
    }
}