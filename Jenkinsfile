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
    }
}














stage('Coverage') {
    // Mesura de la cobertura només sobre tests unitaris
    steps {
        sh '''
            export PYTHONPATH=$WORKSPACE
            python3 -m coverage run -m pytest test/unit
            python3 -m coverage report --fail-under=80
        '''
    }
}




stage('Coverage') {
    // Mesura de la cobertura només sobre tests unitaris
    steps {
        sh '''
            export PYTHONPATH=$WORKSPACE
            python3 -m coverage run -m pytest test/unit
            python3 -m coverage xml -o coverage.xml
            python3 -m coverage report
        '''
    }
    post {
        always {
            publishCoverage adapters: [
                coberturaAdapter('coverage.xml')
            ]
        }
    }
}







stage('Performance') {
  steps {
    sh '''
      if command -v jmeter >/dev/null 2>&1; then
        jmeter -n -t performance/test-plan.jmx -l performance/results.jtl
      else
        echo "JMeter no disponible al Jenkins docent, prova de rendiment omesa"
      fi
    '''
  }
}










}

}
