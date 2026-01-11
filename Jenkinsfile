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
    // Execució dels tests unitaris (sense proves REST)
    steps {
        sh '''
            export PYTHONPATH=$WORKSPACE
            pip3 install pytest flask flake8 bandit coverage
            mkdir -p reports
            pytest test/unit --junitxml=reports/unit-tests.xml
        '''
    }
    post {
        always {
            junit allowEmptyResults: true, testResults: 'reports/unit-tests.xml'
        }
    }
}



stage('Rest') {
    // Execució de les proves d'integració REST
    steps {
        sh '''
            export PYTHONPATH=$WORKSPACE
            pytest test/rest || true
        '''
    }
}


stage('Static') {
    // Anàlisi estàtic del codi amb flake8
    steps {
        sh '''
            export PYTHONPATH=$WORKSPACE
            python3 -m flake8 app > flake8-report.txt || true
        '''
        recordIssues(
            tools: [flake8(pattern: 'flake8-report.txt')],
            qualityGates: [
                [threshold: 8, type: 'TOTAL', unstable: true],
                [threshold: 10, type: 'TOTAL', unstable: false]
            ]
        )
    }
}


stage('Security Test') {
    // Anàlisi de seguretat del codi amb Bandit
    steps {
        sh '''
            export PYTHONPATH=$WORKSPACE
            python3 -m bandit -r app -f txt -o bandit-report.txt || true
        '''
        scanForIssues(
            tool: bandit(pattern: 'bandit-report.txt'),
            qualityGates: [
                [threshold: 2, type: 'TOTAL', unstable: true],
                [threshold: 4, type: 'TOTAL', unstable: true]
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

