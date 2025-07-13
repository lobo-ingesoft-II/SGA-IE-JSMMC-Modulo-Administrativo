from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, Any

class CrearUsuario(BaseModel):
    nombres: str
    apellidos: str
    tipoDocumento: str = Field(..., alias="tipo_documento")
    documentoIdentidad: str = Field(..., alias="documento_identidad")
    telefono: str
    email: EmailStr
    contrasena: str
    rol: str
    datos_adicionales: Optional[Dict[str, Any]]  # Este campo es para los datos específicos del rol

    class Config:
        orm_mode = True


class UsuarioUpdate(BaseModel):
    nombres: Optional[str] = None
    apellidos: Optional[str] = None
    tipoDocumento: Optional[str] = None
    documentoIdentidad: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    contrasena: Optional[str] = None
    rol: Optional[str] = None
    datos_adicionales: Optional[dict] = None