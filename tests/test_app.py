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


def test_cp01_registrar_tarea(client):
    r = registrar(client)
    assert r.status_code == 201
    datos = r.get_json()
    assert datos["mensaje"] == "Tarea registrada correctamente."
    assert datos["tarea"]["nombre"] == "Elaborar documentación"
    assert datos["tarea"]["estado"] == "Pendiente"


def test_cp03_consultar_tareas(client):
    registrar(client, nombre="Tarea A")
    registrar(client, nombre="Tarea B")
    tareas = client.get("/api/tareas").get_json()
    assert len(tareas) == 2
    assert {t["nombre"] for t in tareas} == {"Tarea A", "Tarea B"}


def test_registrar_sin_descripcion(client):
    r = registrar(client, descripcion="")
    assert r.status_code == 201
    assert r.get_json()["tarea"]["descripcion"] == ""


def test_pagina_principal_y_health(client):
    assert client.get("/").status_code == 200
    assert client.get("/health").get_json() == {"status": "ok"}
