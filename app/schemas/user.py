from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional

#Schema base do usuário
class UserBase(BaseModel):
    cpf: Optional[str] = None
    nome: Optional[str] = None
    sobrenome: Optional[str] = None
    email: Optional[EmailStr] = None
    image: Optional[HttpUrl] = None

#Schmea de criação do usuário
class UserCreate(UserBase):
    cpf: str
    nome: str
    sobrenome: str
    email: EmailStr
    password: str
    image: Optional[HttpUrl] = None

#Schema de leitura do usuário
class UserRead(BaseModel):
    id: str
    cpf: str
    nome: str
    sobrenome: str
    email: EmailStr
    image: Optional[HttpUrl] = None

#Schema do token JWT
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int

#Schema das credenciais de login
class Credentials(BaseModel):
    email: EmailStr
    password: str