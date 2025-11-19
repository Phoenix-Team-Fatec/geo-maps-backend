from pydantic import BaseModel, EmailStr, AnyUrl, constr
from datetime import date
from typing import Optional

#Schema base do usuário
class UserBase(BaseModel):
    cpf: Optional[str] = None
    nome: Optional[str] = None
    sobrenome: Optional[str] = None
    email: Optional[EmailStr] = None
    data_nascimento: Optional[date] = None
    image: Optional[AnyUrl] = None
    is_blocked: Optional[bool] = None

#Schmea de criação do usuário
class UserCreate(UserBase):
    cpf: str
    nome: str
    sobrenome: str
    email: EmailStr
    password: str
    data_nascimento: date
    image: Optional[AnyUrl] = None

#Schema de leitura do usuário
class UserRead(BaseModel):
    id: str
    cpf: str
    nome: str
    sobrenome: str
    email: EmailStr
    data_nascimento: date
    image: Optional[AnyUrl] = None

#Schema do token JWT
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    refresh_token: Optional[str] = None

#Schema das credenciais de login
class Credentials(BaseModel):
    email: EmailStr
    password: str

class ForgotPasswordIn(BaseModel):
    email: EmailStr

class VerifyResetCodeIn(BaseModel):
    email: EmailStr
    code: constr(min_length=6, max_length=6) 

class ResetPasswordIn(BaseModel):
    email: EmailStr
    code: constr(min_length=6, max_length=6)
    new_password: str