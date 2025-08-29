pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                git 'https://github.com/shakilmunavary/java-maven-calculator-web-app.git'
            }
        }

        stage('JUnit Test') {
            steps {
                sh 'mvn clean test'
            }
        }

        stage('Integration Test') {
            steps {
                sh 'mvn integration-test'
            }
        }

        /*
        stage('Performance Test') {
            steps {
                sh 'mvn cargo:start verify cargo:stop'
            }
        }
        */

        stage('Performance Test') {
            steps {
                sh 'mvn verify'
            }
        }

        stage('Deploy') {
            steps {
                timeout(time: 10, unit: 'MINUTES') {
                    input message: 'Deploy this web app to production?'
                }
                echo 'Deploying to production...'
            }
        }
    }
}
