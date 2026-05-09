pipeline {
    agent any

    environment {
        PYTHON = "python"
        VENV = "venv"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/navyagurukul/TeacherWeb_Automation.git'
            }
        }

        stage('Setup Python Environment') {
            steps {
                bat '''
                %PYTHON% -m venv %VENV%
                call %VENV%\\Scripts\\activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                bat '''
                call %VENV%\\Scripts\\activate
                pytest -m regression -n auto --alluredir=allure-results
                '''
            }
        }

        stage('Generate Allure Report') {
            steps {
                bat '''
                allure generate allure-results --clean -o allure-report
                '''
            }
        }

        stage('Publish Report') {
            steps {
                publishHTML(target: [
                    reportDir: 'allure-report',
                    reportFiles: 'index.html',
                    reportName: 'Allure Report'
                ])
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'allure-results/**', allowEmptyArchive: true
        }

        success {
            echo "✅ Tests Passed!"
        }

        failure {
            echo "❌ Tests Failed!"
        }
    }
}