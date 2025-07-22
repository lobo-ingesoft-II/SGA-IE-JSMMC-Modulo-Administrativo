import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
import respx
from httpx import AsyncClient, Response, ASGITransport
from app.main import app
from app.routers.portal_admin import AUTH_API_URL

respx.assert_all_mocked = False
transport = ASGITransport(app=app)

profesores_mock = [
    {
        "id_usuario": 1,
        "id_profesor": 101,
        "nombres": "Carlos",
        "apellidos": "Ramírez",
        "email": "carlos.ramirez@colegio.edu.co"
    }
]

acudientes_mock = [
    {
        "id_usuario": 2,
        "id_acudiente": 201,
        "nombres": "Marta",
        "apellidos": "López",
        "email": "marta.lopez@colegio.edu.co"
    }
]

administradores_mock = [
    {
        "id_usuario": 3,
        "id_administrador": 301,
        "nombres": "Luis",
        "apellidos": "Gómez",
        "email": "luis.gomez@colegio.edu.co"
    }
]


# -------------------- PROFESORES ------------------------

@pytest.mark.asyncio
@respx.mock
async def test_obtener_profesores_exitoso():
    url = f"{AUTH_API_URL}/profesores"
    respx.get(url, params={"limit": 100}).mock(
        return_value=Response(200, json=profesores_mock)
    )

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/portal_admin/profesores", params={"limit": 100})

    assert response.status_code == 200
    assert response.json() == profesores_mock

@pytest.mark.asyncio
@respx.mock
async def test_obtener_profesores_error():
    url = f"{AUTH_API_URL}/profesores"
    respx.get(url, params={"limit": 100}).mock(
        return_value=Response(500, json={"detail": "Error interno del servidor"})
    )

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/portal_admin/profesores", params={"limit": 100})

    assert response.status_code == 500
    assert response.json()["detail"] == "Error interno del servidor"


# -------------------- ACUDIENTES ------------------------

@pytest.mark.asyncio
@respx.mock
async def test_obtener_acudientes_exitoso():
    url = f"{AUTH_API_URL}/acudientes"
    respx.get(url, params={"limit": 100}).mock(
        return_value=Response(200, json=acudientes_mock)
    )

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/portal_admin/acudientes", params={"limit": 100})

    assert response.status_code == 200
    assert response.json() == acudientes_mock

@pytest.mark.asyncio
@respx.mock
async def test_obtener_acudientes_error():
    url = f"{AUTH_API_URL}/acudientes"
    respx.get(url, params={"limit": 100}).mock(
        return_value=Response(404, json={"detail": "No se encontraron acudientes"})
    )

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/portal_admin/acudientes", params={"limit": 100})

    assert response.status_code == 404
    assert response.json()["detail"] == "No se encontraron acudientes"


# -------------------- ADMINISTRADORES ------------------------

@pytest.mark.asyncio
@respx.mock
async def test_obtener_administradores_exitoso():
    url = f"{AUTH_API_URL}/administradores"
    respx.get(url, params={"limit": 100}).mock(
        return_value=Response(200, json=administradores_mock)
    )

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/portal_admin/administradores", params={"limit": 100})

    assert response.status_code == 200
    assert response.json() == administradores_mock

@pytest.mark.asyncio
@respx.mock
async def test_obtener_administradores_error():
    url = f"{AUTH_API_URL}/administradores"
    respx.get(url, params={"limit": 100}).mock(
        return_value=Response(400, json={"detail": "Petición inválida"})
    )

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/portal_admin/administradores", params={"limit": 100})

    assert response.status_code == 400
    assert response.json()["detail"] == "Petición inválida"
