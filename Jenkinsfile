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


stage('Security Test') {
    steps {
        sh '''
            export PYTHONPATH=$WORKSPACE
            mkdir -p reports/security
            python3 -m bandit -r app -f json -o reports/security/bandit-report.json || true
        '''
        recordIssues(
            tools: [bandit(pattern: 'reports/security/bandit-report.json')]
        )

    }
}


stage('Coverage') {
    steps {
        sh '''
            export PYTHONPATH=$WORKSPACE
            python3 -m coverage run --branch --source=app -m pytest test/unit
            python3 -m coverage xml -o coverage.xml
        '''

        script {
            recordCoverage(
                tools: [[parser: 'COBERTURA', pattern: 'coverage.xml']]
            )
        }

        archiveArtifacts artifacts: 'coverage.xml', fingerprint: true
    }
}











stage('Performance') {
  steps {
    sh '''
      set -e
      export PYTHONPATH=$WORKSPACE
      mkdir -p reports/performance

      # Levantar Flask en background
      export FLASK_APP=app/api.py
      nohup flask run --host=127.0.0.1 --port=5000 > reports/performance/flask.log 2>&1 &
      FLASK_PID=$!

      # Esperar a que el puerto responda (hasta ~10s)
      for i in $(seq 1 20); do
        if curl -s http://127.0.0.1:5000/calc/add/1/2 >/dev/null; then
          echo "Flask OK"
          break
        fi
        sleep 0.5
      done

      # Ejecutar JMeter (tu .jmx)
      jmeter -n -t test/jmeter/flask.jmx -l reports/performance/results.jtl

      # Parar Flask
      kill $FLASK_PID || true
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
