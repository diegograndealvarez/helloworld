import pytest
from app.api import api_application


@pytest.fixture
def client():
    # Fixture que crea un client de proves de Flask
    # Permet simular peticions HTTP sense aixecar el servidor real
    api_application.config["TESTING"] = True
    with api_application.test_client() as client:
        yield client


def test_hello_endpoint(client):
    # Comprova que l'endpoint arrel ("/") respon correctament
    # Aquest test valida que l'aplicació Flask està operativa
    response = client.get("/")
    assert response.status_code == 200
    assert b"Hello from The Calculator!" in response.data


def test_add_endpoint_ok(client):
    # Comprova el funcionament correcte de l'endpoint /calc/add
    # amb paràmetres vàlids convertibles a nombre
    response = client.get("/calc/add/2/3")
    assert response.status_code == 200
    assert response.data == b"5"


def test_add_endpoint_bad_request(client):
    # Comprova que l'endpoint /calc/add gestiona correctament
    # errors de tipus quan els paràmetres no són numèrics
    # Aquest test cobreix el bloc except del controlador
    response = client.get("/calc/add/a/3")
    assert response.status_code == 400


def test_substract_endpoint_ok(client):
    # Comprova el funcionament correcte de l'endpoint /calc/substract
    # amb valors vàlids i resposta HTTP satisfactòria
    response = client.get("/calc/substract/5/2")
    assert response.status_code == 200
    assert response.data == b"3"
