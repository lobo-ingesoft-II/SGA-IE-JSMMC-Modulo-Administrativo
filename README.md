# API - Modulo Administrativo

Esta es una API para el **Modulo Administrativo** que interactúa con una API de autenticación para manejar usuarios. Permite la creación, actualización, eliminación y gestión del estado de los usuarios.

## Requisitos

### Dependencias

Esta API está construida con **FastAPI** y se conecta con una API de autenticación. Asegúrate de tener las siguientes dependencias instaladas:

- **fastapi**: Framework para construir APIs rápidas y eficientes.
- **httpx**: Cliente HTTP asíncrono para hacer solicitudes HTTP a la API de autenticación.
- **pydantic**: Librería para la validación de datos basada en Python.
- **uvicorn**: Servidor ASGI para correr la API.
- **email-validator**: Para validación de correos electrónicos en Pydantic.
- **python-dotenv**: Para gestionar variables de entorno.

### Dependencias adicionales para entorno de desarrollo

```bash
pip install -r requirements.txt
```
# Endpoints de la API - Módulo Administrativo

## Crear un nuevo usuario

- **Método**: `POST`
- **Ruta**: `/portal_admin/usuarios`
- **Descripción**: Crea un nuevo usuario en la API de autenticación.
- **Entrada**: 
  - `nombres` (str): Nombre del usuario.
  - `apellidos` (str): Apellidos del usuario.
  - `tipo_documento` (str): Tipo de documento de identificación.
  - `documento_identidad` (str): Número de documento de identidad.
  - `telefono` (str): Número de teléfono.
  - `email` (str): Correo electrónico.
  - `contrasena` (str): Contraseña del usuario.
  - `rol` (str): Rol del usuario (`administrador`, `profesor`, `acudiente`).
  - `datos_adicionales` (dict, opcional): Datos adicionales específicos del rol (por ejemplo, especialidad para profesores, parentesco para acudientes).
- **Respuesta**: 
  - `{ "mensaje": "Usuario creado correctamente", "id_usuario": int }`
- **Error**: 
  - Si ya existe un usuario con el mismo documento o correo, se devuelve un error con el detalle: `"Documento de identidad o email ya existen."`.

## Editar un usuario

- **Método**: `PATCH`
- **Ruta**: `/portal_admin/usuarios/{id_usuario}`
- **Descripción**: Actualiza parcialmente un usuario en la API de autenticación.
- **Entrada**: 
  - `nombres` (str, opcional): Nombre del usuario.
  - `apellidos` (str, opcional): Apellidos del usuario.
  - `tipo_documento` (str, opcional): Tipo de documento de identificación.
  - `documento_identidad` (str, opcional): Número de documento de identidad.
  - `telefono` (str, opcional): Número de teléfono.
  - `email` (str, opcional): Correo electrónico.
  - `rol` (str, opcional): Rol del usuario (`administrador`, `profesor`, `acudiente`).
  - `datos_adicionales` (dict, opcional): Datos adicionales del usuario.
- **Respuesta**: 
  - `{ "mensaje": "Usuario actualizado correctamente" }`
- **Error**: 
  - Si el usuario no se encuentra, se devuelve un error con el detalle: `"Usuario no encontrado."`.

## Cambiar estado de un usuario

- **Método**: `PATCH`
- **Ruta**: `/portal_admin/usuarios/{id_usuario}/estado`
- **Descripción**: Cambia el estado de un usuario (activo/inactivo).
- **Entrada**: 
  - `estado` (str): El estado del usuario, debe ser `"activo"` o `"inactivo"`.
- **Respuesta**: 
  - `{ "mensaje": "Estado de usuario actualizado correctamente" }`
- **Error**: 
  - Si el estado es inválido (no `"activo"` o `"inactivo"`), se devuelve un error con el detalle: `"Estado inválido. Debe ser 'activo' o 'inactivo'."`.
  - Si el usuario no se encuentra, se devuelve un error con el detalle: `"Usuario no encontrado."`.

## Eliminar un usuario

- **Método**: `DELETE`
- **Ruta**: `/portal_admin/usuarios/{id_usuario}`
- **Descripción**: Elimina un usuario de la base de datos.
- **Entrada**: 
  - `id_usuario` (int): El ID del usuario a eliminar.
- **Respuesta**: 
  - `{ "mensaje": "Usuario eliminado correctamente" }`
- **Error**: 
  - Si el usuario no se encuentra, se devuelve un error con el detalle: `"Usuario no encontrado."`.

## Listar profesores
- **Método**: `GET`
- **Ruta**: `/portal_admin/profesores?limit=100`
- **Parámetros**:
  - `limit` (opcional): Número máximo de resultados a devolver (valor por defecto: 100)
- **Respuesta exitosa**:
 ```json
  [
    {
      "id_usuario": 0,
      "id_profesor": 0,
      "nombres": "string",
      "apellidos": "string",
      "email": "string"
    }
  ]

```
## Listar acudientes
- **Método**: `GET`
- **Ruta**: `/portal_admin/acudientes?limit=100`
- **Parámetros**:
  - `limit` (opcional): Número máximo de resultados a devolver (valor por defecto: 100)
- **Respuesta exitosa**:
 ```json
  [
    {
      "id_usuario": 0,
      "id_acudiente": 0,
      "nombres": "string",
      "apellidos": "string",
      "email": "string"
    }
  ]

```
## Listar administradores
- **Método**: `GET`
- **Ruta**: `/portal_admin/administradores?limit=100`
- **Parámetros**:
  - `limit` (opcional): Número máximo de resultados a devolver (valor por defecto: 100)
- **Respuesta exitosa**:
 ```json
 [
  {
    "id_usuario": 0,
    "id_administrador": 0,
    "nombres": "string",
    "apellidos": "string",
    "email": "string"
  }
]

```
## Ejecutar la API:

```bash
uvicorn app.main:app --reload --port 8012
```
