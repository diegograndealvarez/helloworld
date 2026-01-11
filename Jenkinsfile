pipeline {
    agent any

    stages {

        stage('Get Code') {
            // Obtenció del codi font des del repositori
            steps {
                checkout scm
            }
        }

        stage('Unit') {
            // Execució dels tests unitaris (només una vegada en tot el pipeline)
            steps {
                sh '''
                    pip3 install -r requirements.txt
                    pytest --junitxml=reports/unit-tests.xml
                '''
            }
            post {
                always {
                    junit 'reports/unit-tests.xml'
                }
            }
        }

        stage('Rest') {
            // Execució dels tests d'integració REST
            steps {
                sh 'pytest test/rest'
            }
        }

        stage('Static') {
            // Anàlisi estàtic del codi amb flake8
            steps {
                sh '''
                    flake8 app > flake8-report.txt || true
                '''
                recordIssues(
                    tools: [flake8(pattern: 'flake8-report.txt')],
                    qualityGates: [
                        [threshold: 8, type: 'TOTAL', unstable: true],
                        [threshold: 10, type: 'TOTAL', failure: true]
                    ]
                )
            }
        }

        stage('Security Test') {
            // Anàlisi de seguretat del codi amb bandit
            steps {
                sh '''
                    bandit -r app -f txt -o bandit-report.txt || true
                '''
                recordIssues(
                    tools: [bandit(pattern: 'bandit-report.txt')],
                    qualityGates: [
                        [threshold: 2, type: 'TOTAL', unstable: true],
                        [threshold: 4, type: 'TOTAL', failure: true]
                    ]
                )
            }
        }

        stage('Coverage') {
            // Càlcul de la cobertura reutilitzant els tests unitaris
            steps {
                sh '''
                    coverage run -m pytest
                    coverage xml -o coverage.xml
                    coverage report
                '''
                publishCoverage adapters: [
                    coberturaAdapter('coverage.xml')
                ]
            }
        }

        stage('Performance') {
            // Execució de proves de càrrega amb JMeter
            steps {
                sh '''
                    jmeter -n -t performance/test-plan.jmx -l performance/results.jtl
                '''
                perfReport 'performance/results.jtl'
            }
        }
    }
}

