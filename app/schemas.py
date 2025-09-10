from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List

# Auth
class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=6, max_length=64)

class UserOut(BaseModel):
    jugador_id: int
    username: str
    email: EmailStr
    class Config: from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Mazmorras / Enemigos
class EnemigoOut(BaseModel):
    enemigo_id: int
    nombre: str
    poder: Optional[int]
    class Config: from_attributes = True

class MazmorraOut(BaseModel):
    mazmorra_id: int
    nombre: str
    descripcion: Optional[str]
    tipo_medalla: Optional[int]
    dificultad: Optional[int]
    orden: int
    enemigos: List[EnemigoOut] = []
    class Config: from_attributes = True

# Progreso
class ProgresoOut(BaseModel):
    progreso_id: int
    mazmorra_id: int
    medalla_id: Optional[int]
    completada: bool
    class Config: from_attributes = True

# Inventario
class InventarioItemOut(BaseModel):
    inventario_id: int
    pocion_id: int
    cantidad: int
    class Config: from_attributes = True

class InventarioUpdate(BaseModel):
    pocion_id: int
    delta: int  # +n para agregar, -n para consumir
