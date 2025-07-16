from fastapi import APIRouter, HTTPException
from httpx import AsyncClient  # Para realizar peticiones HTTP hacia la API de autenticación
from app.schemas.usuario_schema import CrearUsuario, UsuarioUpdate, ProfesorResponse, AcudienteResponse, AdministradorResponse
from typing import List
from fastapi import Query
# Definir la URL base para la API de autenticación
AUTH_API_URL = "http://localhost:8009/admin"

router = APIRouter(
    prefix="/portal_admin",
    tags=["portal_admin"]
)

# Crear un nuevo usuario en la API de autenticación
@router.post("/usuarios")
async def crear_usuario(usuario: CrearUsuario):
    async with AsyncClient() as client:
        response = await client.post(
            f'{AUTH_API_URL}/usuarios',  # Usar la URL base
            json=usuario.dict(by_alias=True) # Pasa el usuario como un diccionario
        )
        if response.status_code != 201:
             # Obtener el detalle del error de la respuesta
            error_detail = response.json().get('detail', 'Error desconocido')
            raise HTTPException(status_code=response.status_code, detail=error_detail)
        return response.json()

# Editar un usuario en la API de autenticación
@router.patch("/usuarios/{id_usuario}")
async def editar_usuario(id_usuario: int, usuario: UsuarioUpdate):
    async with AsyncClient() as client:
        response = await client.patch(
            f'{AUTH_API_URL}/usuarios/{id_usuario}',  # Usar la URL base
            json=usuario.dict(by_alias=True)   # Pasa los datos de usuario
        )
        if response.status_code != 200:
            # Obtener el detalle del error de la respuesta
            error_detail = response.json().get('detail', 'Error desconocido')
            raise HTTPException(status_code=response.status_code, detail=error_detail)
        return response.json()

# Cambiar estado de un usuario
@router.patch("/usuarios/{id_usuario}/estado")
async def cambiar_estado_usuario(id_usuario: int, estado: str):
    async with AsyncClient() as client:
        # Usar la query string para enviar 'estado'
        response = await client.patch(
            f'{AUTH_API_URL}/usuarios/{id_usuario}/estado?estado={estado}',  # Pasamos 'estado' como query param
        )

        if response.status_code != 200:
            # Obtener el detalle del error de la respuesta
            error_detail = response.json().get('detail', 'Error desconocido')
            raise HTTPException(status_code=response.status_code, detail=error_detail)
        return response.json()

# Eliminar un usuario
@router.delete("/usuarios/{id_usuario}")
async def eliminar_usuario(id_usuario: int):
    async with AsyncClient() as client:
        response = await client.delete(
            f'{AUTH_API_URL}/usuarios/{id_usuario}'  # Usar la URL base
        )
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error al eliminar usuario")
        return response.json()

# Obtener todos los profesores
@router.get("/profesores", response_model=List[ProfesorResponse])
async def obtener_profesores(
    #skip: int = Query(0, description="Número de registros a saltar"),
    limit: int = Query(100, description="Límite de registros por página")
):
    async with AsyncClient() as client:
        response = await client.get(
            f"{AUTH_API_URL}/profesores",
            params={"limit": limit}
        )
        if response.status_code != 200:
            error_detail = response.json().get("detail", "Error al obtener profesores")
            raise HTTPException(status_code=response.status_code, detail=error_detail)
        return response.json()

# Obtener todos los acudientes
@router.get("/acudientes", response_model=List[AcudienteResponse])
async def obtener_acudientes(
    #skip: int = Query(0, description="Número de registros a saltar"),
    limit: int = Query(100, description="Límite de registros por página")
):
    async with AsyncClient() as client:
        response = await client.get(
            f"{AUTH_API_URL}/acudientes",
            params={"limit": limit}
        )
        if response.status_code != 200:
            error_detail = response.json().get("detail", "Error al obtener acudientes")
            raise HTTPException(status_code=response.status_code, detail=error_detail)
        return response.json()

# Obtener todos los administradores
@router.get("/administradores", response_model=List[AdministradorResponse])
async def obtener_administradores(
    #skip: int = Query(0, description="Número de registros a saltar"),
    limit: int = Query(100, description="Límite de registros por página")
):
    async with AsyncClient() as client:
        response = await client.get(
            f"{AUTH_API_URL}/administradores",
            params={"limit": limit}
        )
        if response.status_code != 200:
            error_detail = response.json().get("detail", "Error al obtener administradores")
            raise HTTPException(status_code=response.status_code, detail=error_detail)
        return response.json()
