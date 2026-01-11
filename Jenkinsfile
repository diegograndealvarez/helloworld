pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Tests unitaris') {
            steps {
                sh '''
                  export PYTHONPATH=$WORKSPACE
                  pytest test/unit
                '''
            }
        }

        stage('Tests REST') {
            steps {
                sh '''
                  export PYTHONPATH=$WORKSPACE
                  export FLASK_APP=app/api.py

                  # Descarregar Wiremock
                  wget -q https://repo1.maven.org/maven2/com/github/tomakehurst/wiremock-jre8-standalone/2.35.0/wiremock-jre8-standalone-2.35.0.jar

                  # Crear mapping de Wiremock
                  mkdir -p mappings
                  cat << 'EOF' > mappings/sqrt64.json
{
  "request": {
    "method": "GET",
    "url": "/calc/sqrt/64"
  },
  "response": {
    "status": 200,
    "body": "8"
  }
}
EOF

                  # Arrencar els serveis necessaris
                  java -jar wiremock-jre8-standalone-2.35.0.jar --port 9090 --root-dir . &
                  flask run &

                  # Esperar que els serveis estiguin disponibles
                  sleep 5

                  # Executar els tests REST
                  pytest test/rest
                '''
            }
        }

    }
}

