import sys
import os
import pytest
from fastapi.testclient import TestClient

# Agregar el directorio padre al sys.path
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from main import app


clientt = TestClient(app)


@pytest.fixture
def client():
    return clientt
