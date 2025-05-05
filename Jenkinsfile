pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                url: 'https://github.com/shahidz27/Bookstore_api_test.git'
            }
        }

        stage('Setup Python') {
            steps {
                bat 'python -m venv jenkins_venv'
                bat 'jenkins_venv\\Scripts\\pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                bat 'jenkins_venv\\Scripts\\pytest --junitxml=test-results.xml ./test'
            }
        }
    }

    post {
        always {
            junit 'test-results.xml'
        }
    }
}