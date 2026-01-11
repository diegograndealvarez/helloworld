pipeline {
    agent any

    stages {

        stage('Get Code') {
            steps {
                checkout scm
            }
        }

        stage('Unit') {
            steps {
                sh '''
                    export PYTHONPATH=$WORKSPACE
                    pip3 install pytest flask flake8 bandit coverage
                    mkdir -p reports/unit
                    pytest test/unit --junitxml=reports/unit/unit-tests.xml
                '''
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'reports/unit/unit-tests.xml'
                }
            }
        }

        stage('Rest') {
            steps {
                sh '''
                    export PYTHONPATH=$WORKSPACE
                    pytest test/rest || true
                '''
            }
        }

        stage('Static') {
            steps {
                sh '''
                    export PYTHONPATH=$WORKSPACE
                    mkdir -p reports/static
                    python3 -m flake8 app > reports/static/flake8-report.txt || true
                '''
                recordIssues(
                    tools: [flake8(pattern: 'reports/static/flake8-report.txt')],
                    qualityGates: [
                        [threshold: 8, type: 'TOTAL', unstable: true],
                        [threshold: 10, type: 'TOTAL', unstable: false]
                    ]
                )
            }
        }

        stage('Security Test') {
            steps {
                sh '''
                    export PYTHONPATH=$WORKSPACE
                    mkdir -p reports/security
                    python3 -m bandit -r app -f txt -o reports/security/bandit-report.txt || true
                '''
            }
        }

        stage('Coverage') {
            steps {
                sh '''
                    export PYTHONPATH=$WORKSPACE
                    mkdir -p reports/unit
                    python3 -m coverage run -m pytest test/unit
                    python3 -m coverage xml -o reports/unit/coverage.xml
                    python3 -m coverage report
                '''
                archiveArtifacts artifacts: 'reports/unit/coverage.xml', fingerprint: true
            }
        }

stage('Performance') {
    // Proves de rendiment amb Apache JMeter
    steps {
        sh '''
            mkdir -p reports/performance
            if command -v jmeter >/dev/null 2>&1; then
                jmeter -n -t performance/test-plan.jmx -l reports/performance/results.jtl
            else
                echo "JMeter no disponible al Jenkins docent, prova de rendiment omesa"
            fi
        '''
    }
    post {
        always {
            perfReport sourceDataFiles: 'reports/performance/results.jtl'
        }
    }
}



    }
}
