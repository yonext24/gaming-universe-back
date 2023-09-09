import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.models import UserORM, SessionORM


SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:1234@localhost/ecommerce"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={}, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)


# Configuración de la base de datos de prueba
@pytest.fixture(scope="module")
def test_db():
    db = SessionLocal()
    return db


# Creación de datos de prueba antes de las pruebas
def test_setup_test_data(test_db):
    user_to_add = UserORM(
        username="testuser",
        password="testing",
        id=200,
        first_name="test",
        last_name="test",
        email="aaaaaaa",
    )

    test_db.add(user_to_add)
    test_db.commit()

    assert test_db.query(UserORM).filter_by(username="testuser").count() == 1


# Prueba de inicio de sesión después de crear un usuario
def test_login_after_user_created(client):
    form_data = {"username": "testuser", "password": "testing"}
    response = client.post(
        "/auth/login",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data=form_data,
    )
    session_cookie = response.cookies.get("session_id")

    assert response.status_code == 200
    assert session_cookie is not None

    global session_id
    session_id = session_cookie


def test_logout_after_login(client):
    assert session_id is not None
    print(session_id)

    client.cookies.set(name="session_id", value=session_id)
    response = client.delete("/auth/session")

    client.cookies.delete(name="session_id")
    assert response.status_code == 200


# Limpiar datos de prueba después de las pruebas
def test_cleanup_test_data(test_db):
    test_db.query(SessionORM).filter_by(user_id=200).delete()
    test_db.query(UserORM).filter_by(username="testuser").delete()

    test_db.commit()

    assert test_db.query(SessionORM).filter_by(user_id=200).count() == 0
    assert test_db.query(UserORM).filter_by(username="testuser").count() == 0
