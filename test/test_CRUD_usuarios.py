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

# ✅ Claves corregidas usando aliases esperados por FastAPI
usuario_valido = {
    "nombres": "Juan",
    "apellidos": "Perez",
    "tipo_documento": "CC",  # <--- CORREGIDO
    "documento_identidad": "1234567890",  # <--- CORREGIDO
    "telefono": "3000000000",
    "email": "juan.perez@ejemplo.com",
    "contrasena": "clave123",
    "rol": "profesor",
    "datos_adicionales": {
        "especialidad": "Matemáticas",
        "es_director": True
    }
}

usuario_duplicado = usuario_valido.copy()

usuario_incompleto = {
    "nombres": "Laura",
    "apellidos": "Lopez",
    "tipo_documento": "CC",  # <--- CORREGIDO
    "documento_identidad": "1111111111",  # <--- CORREGIDO
    "telefono": "3001231234",
    "email": "laura.lopez@ejemplo.com",
    "contrasena": "clave123",
    "rol": "acudiente",
    "datos_adicionales": {
        "celular": "3009999999"
    }
}

@pytest.mark.asyncio
@respx.mock
async def test_crear_usuario_exitoso():
    url = f"{AUTH_API_URL}/usuarios"
    respx.post(url).mock(return_value=Response(201, json={"mensaje": "Usuario creado correctamente", "id_usuario": 10}))

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/portal_admin/usuarios", json=usuario_valido)

    assert response.status_code == 200
    assert response.json()["mensaje"] == "Usuario creado correctamente"

@pytest.mark.asyncio
@respx.mock
async def test_crear_usuario_duplicado():
    url = f"{AUTH_API_URL}/usuarios"
    respx.post(url).mock(return_value=Response(400, json={"detail": "Documento de identidad o email ya existen."}))

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/portal_admin/usuarios", json=usuario_duplicado)

    assert response.status_code == 400
    assert response.json()["detail"] == "Documento de identidad o email ya existen."

@pytest.mark.asyncio
@respx.mock
async def test_crear_usuario_incompleto():
    url = f"{AUTH_API_URL}/usuarios"
    respx.post(url).mock(return_value=Response(400, json={"detail": "Datos adicionales del acudiente incompletos."}))

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/portal_admin/usuarios", json=usuario_incompleto)

    assert response.status_code == 400
    assert response.json()["detail"] == "Datos adicionales del acudiente incompletos."

@pytest.mark.asyncio
@respx.mock
async def test_editar_usuario_exitoso():
    url = f"{AUTH_API_URL}/usuarios/10"
    update_data = {"telefono": "3112223344"}
    respx.patch(url).mock(return_value=Response(200, json={"mensaje": "Usuario actualizado correctamente"}))

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.patch("/portal_admin/usuarios/10", json=update_data)

    assert response.status_code == 200
    assert response.json()["mensaje"] == "Usuario actualizado correctamente"

@pytest.mark.asyncio
@respx.mock
async def test_cambiar_estado_usuario_exitoso():
    url = f"{AUTH_API_URL}/usuarios/10/estado?estado=activo"
    respx.patch(url).mock(return_value=Response(200, json={"mensaje": "Estado de usuario actualizado correctamente"}))

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.patch("/portal_admin/usuarios/10/estado?estado=activo")

    assert response.status_code == 200
    assert response.json()["mensaje"] == "Estado de usuario actualizado correctamente"

@pytest.mark.asyncio
@respx.mock
async def test_cambiar_estado_usuario_invalido():
    url = f"{AUTH_API_URL}/usuarios/10/estado?estado=no_valido"
    respx.patch(url).mock(return_value=Response(400, json={"detail": "Estado inválido. Debe ser 'activo' o 'inactivo'."}))

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.patch("/portal_admin/usuarios/10/estado?estado=no_valido")

    assert response.status_code == 400
    assert "Estado inválido" in response.json()["detail"]

@pytest.mark.asyncio
@respx.mock
async def test_eliminar_usuario_exitoso():
    url = f"{AUTH_API_URL}/usuarios/10"
    respx.delete(url).mock(return_value=Response(200, json={"mensaje": "Usuario eliminado correctamente"}))

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.delete("/portal_admin/usuarios/10")

    assert response.status_code == 200
    assert response.json()["mensaje"] == "Usuario eliminado correctamente"

@pytest.mark.asyncio
@respx.mock
async def test_eliminar_usuario_no_encontrado():
    url = f"{AUTH_API_URL}/usuarios/999"
    respx.delete(url).mock(return_value=Response(404, json={"detail": "Error al eliminar usuario"}))  # Ajusta si es "Usuario no encontrado"

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.delete("/portal_admin/usuarios/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Error al eliminar usuario"
