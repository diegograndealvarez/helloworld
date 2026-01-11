# Pràctica CP1 – Integració Contínua amb Jenkins

## 1. Objectiu de la pràctica

L’objectiu d’aquesta pràctica és introduir l’ús de **Jenkins** com a eina d’**Integració Contínua**, automatitzant l’execució de **tests unitaris** i **tests REST** sobre una aplicació Python mitjançant un **pipeline declaratiu** definit en un fitxer `Jenkinsfile`.

---

## 2. Entorn de treball

L’entorn utilitzat per a la realització de la pràctica és el següent:

- Sistema operatiu: Ubuntu 22.04 (Vagrant)
- Jenkins: Jenkins LTS
- Llenguatge: Python 3.10
- Framework de proves: pytest
- API REST: Flask
- Mock de serveis REST: Wiremock
- Control de versions: Git i GitHub

Jenkins s’executa de manera local dins d’una màquina virtual gestionada amb **Vagrant**.

---

## 3. Repositori del projecte

El codi font de l’aplicació es gestiona mitjançant un repositori Git allotjat a GitHub.  
El repositori conté:

- Codi de l’aplicació (`app/`)
- Tests unitaris (`test/unit`)
- Tests REST (`test/rest`)
- Fitxer `Jenkinsfile` amb la definició del pipeline

---

## 4. Pipeline de Jenkins

El pipeline està definit mitjançant un **pipeline declaratiu** en el fitxer `Jenkinsfile` i consta de **tres etapes principals**.

---

### 4.1 Checkout del codi

En aquesta etapa Jenkins clona automàticament el repositori des de GitHub per disposar del codi actualitzat en cada execució.

```groovy
stage('Checkout') {
    steps {
        checkout scm
    }
}
```

---

### 4.2 Execució de tests unitaris

En aquesta etapa s’executen els **tests unitaris** mitjançant `pytest`, validant la lògica interna de l’aplicació.

```groovy
stage('Tests unitaris') {
    steps {
        sh '''
          export PYTHONPATH=$WORKSPACE
          pytest test/unit
        '''
    }
}
```

Els tests unitaris s’executen correctament i el pipeline continua únicament si totes les proves passen.

---

### 4.3 Execució de tests REST

En aquesta etapa es validen els **endpoints REST** de l’aplicació.

Per a això es realitzen les accions següents:

1. Descàrrega dinàmica de Wiremock.
2. Creació del mapping necessari per simular l’endpoint `/calc/sqrt/64`.
3. Arrencada de l’API Flask.
4. Arrencada de Wiremock.
5. Execució dels tests REST mitjançant `pytest`.

```groovy
stage('Tests REST') {
    steps {
        sh '''
          export PYTHONPATH=$WORKSPACE
          export FLASK_APP=app/api.py

          wget -q https://repo1.maven.org/maven2/com/github/tomakehurst/wiremock-jre8-standalone/2.35.0/wiremock-jre8-standalone-2.35.0.jar

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

          java -jar wiremock-jre8-standalone-2.35.0.jar --port 9090 --root-dir . &
          flask run &

          sleep 5
          pytest test/rest
        '''
    }
}
```

Els tests REST validen tant l’endpoint real de l’API com l’endpoint simulat mitjançant Wiremock.

---

## 5. Resultats obtinguts

Els resultats de l’execució del pipeline són els següents:

- Tests unitaris executats correctament.
- Tests REST executats correctament.
- Pipeline finalitzat amb estat **SUCCESS**.

Cada execució del pipeline es realitza en un entorn net i reproductible.

---

## 6. Conclusions

Mitjançant aquesta pràctica s’ha aconseguit:

- Automatitzar l’execució de proves mitjançant Jenkins.
- Integrar tests unitaris i tests REST en un pipeline d’Integració Contínua.
- Utilitzar Wiremock per simular serveis REST externs.
- Garantir la reproductibilitat de l’entorn de proves en cada execució.

La Integració Contínua permet detectar errors de manera primerenca i millorar la qualitat del programari desenvolupat.

---

## 7. Evidències

S’adjunten com a evidències:

- Captura del dashboard de Jenkins.
- Captura del job CP1-Pipeline.
- Captura del build finalitzat en **SUCCESS**.
- Fitxer `Jenkinsfile`.
