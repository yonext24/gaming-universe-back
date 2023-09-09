# ***************************************************************************************
#
#   Este archivo contiente tests unitarios a los endpoints de /auth de la api.
#   No contiene tests de integración con la base de datos, esos tests estan en
#                           /test_integration
#
# ***************************************************************************************
#
#   This file contains unitary tests for the /auth api endpoints. Tt doesn't contain
#   integration tests with the database, those tests are in /test_integration
#
# ***************************************************************************************


def test_read_incorrect_user(client):
    response = client.get("/auth/user")
    assert response.status_code == 401


def test_read_user_with_incorrect_cookie(client):
    client.cookies.set(name="session_id", value="fake")

    response = client.get("/auth/user")

    client.cookies.delete(name="session_id")
    assert response.status_code == 401


def test_incorrect_login(client):
    data = {"username": "fake", "password": "fake"}
    response = client.post("/auth/login", data=data)
    assert response.status_code == 409


def test_session_with_no_cookie(client):
    response = client.get("auth/session")
    assert response.status_code == 401


def test_session_with_expirated_cookie(client):
    cookie = {"session_id": "fake", "maxAge": "fake"}
