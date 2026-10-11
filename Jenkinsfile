pipeline {
    agent any

    parameters {
        choice(name: 'MARKER', choices: ['smoke', 'regression', 'all'], description: 'Which tests to run')
        string(name: 'BASE_URL', defaultValue: 'https://restful-booker.herokuapp.com', description: 'API under test')
        string(name: 'WORKERS', defaultValue: '4', description: 'Parallel pytest workers')
    }

    triggers {
        cron('H 2 * * 1-5')   // nightly run on weekdays; H spreads load across the hour
    }

    options {
        timeout(time: 30, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '20'))
        timestamps()
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Set up Python') {
            steps {
                bat 'python -m venv .venv'
                bat '.venv\\Scripts\\python -m pip install --upgrade pip'
                bat '.venv\\Scripts\\pip install -r requirements.txt'
            }
        }

        stage('Run tests') {
            steps {
                // Credentials come from Jenkins, never from the repo.
                // conftest.py reads RB_USERNAME / RB_PASSWORD from the environment.
                withCredentials([usernamePassword(credentialsId: 'restful-booker-admin',
                                                  usernameVariable: 'RB_USERNAME',
                                                  passwordVariable: 'RB_PASSWORD')]) {
                    script {
                        def markerArg = params.MARKER == 'all' ? '' : "-m ${params.MARKER}"
                        // returnStatus: test failures mark the build UNSTABLE (yellow) via junit,
                        // instead of FAILED (red), which is reserved for broken setup.
                        def status = bat(returnStatus: true, script:
                            ".venv\\Scripts\\pytest ${markerArg} -n ${params.WORKERS} " +
                            "--base-url=${params.BASE_URL} " +
                            "--junitxml=reports\\junit.xml " +
                            "--html=reports\\report.html --self-contained-html")
                        echo "pytest exit code: ${status}"
                    }
                }
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true, testResults: 'reports/junit.xml'
            archiveArtifacts artifacts: 'reports/**', allowEmptyArchive: true
        }
    }
}