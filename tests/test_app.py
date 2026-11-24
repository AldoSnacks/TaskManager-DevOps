"""Pruebas unitarias de TaskManager (CP01 a CP07)."""
import pytest

from app import create_app


@pytest.fixture
def client(tmp_path):
    app = create_app(str(tmp_path / "test.db"))
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def registrar(client, **datos):
    base = {"nombre": "Elaborar documentación", "descripcion": "Manual de usuario", "prioridad": "Alta"}
    base.update(datos)
    return client.post("/api/tareas", json=base)


def test_pagina_principal_y_health(client):
    assert client.get("/").status_code == 200
    assert client.get("/health").get_json() == {"status": "ok"}
