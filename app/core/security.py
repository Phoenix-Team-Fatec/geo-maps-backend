from datetime import datetime, timedelta, timezone
from typing import Optional, Any, Dict, Tuple
from passlib.context import CryptContext
from jose import jwt, JWTError
from uuid import uuid4
import os
from dotenv import load_dotenv

#Carrega as variáveis de ambiente do .env
load_dotenv()

#Declara as constantes de segurança
SECRET_KEY = os.environ.get('SECRET_KEY',)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 365

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#Funções para hash e verificação de senhas
def get_password_hash(password:str) -> str:
    return pwd_context.hash(password)

#Verifica se a senha em texto puro bate com o hash
def verify_password(plain_password:str, hashed_password:str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

#Função interna para criar tokens
def _create_token(
    subject: str | int,
    expires_delta: timedelta,
    token_type: str,
    extra: Optional[Dict[str, Any]] = None
) -> str:
    now = datetime.now(timezone.utc)
    to_encode: Dict[str, Any] = {
        "sub": str(subject),
        "type": token_type,      
        "iat": int(now.timestamp()),
        "nbf": int(now.timestamp()),
        "jti": str(uuid4()),      
        "exp": int((now + expires_delta).timestamp())
    }
    if extra:
        to_encode.update(extra)
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

#Cria o access token
def create_access_token(subject: str | int, extra: Optional[Dict[str, Any]] = None) -> str:
    return _create_token(subject, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES), "access", extra)

#Cria o refresh token
def create_refresh_token(subject: str | int, extra: Optional[Dict[str, Any]] = None) -> str:
    return _create_token(subject, timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS), "refresh", extra)

REVOKED_JTIS: set[str] = set()

#Revoga o jti, adicionando na lista de revogados
def revoke_jti(jti: str) -> None:
    REVOKED_JTIS.add(jti)

#Revoga o jti, adicionando na lista de revogados
def is_revoked(jti: str) -> bool:
    return jti in REVOKED_JTIS

#Decodifica o token JWT
def decode_token(token: str) -> Dict[str, Any]:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

#Função para refresh do access token usando o refresh token
def refresh_session(refresh_token: str) -> Tuple[str, str]:
    try:
        payload = decode_token(refresh_token)
    except JWTError:
        raise ValueError("Refresh token inválido")

    if payload.get("type") != "refresh":
        raise ValueError("Token não é refresh")

    jti = payload.get("jti")
    sub = payload.get("sub")
    if not jti or not sub:
        raise ValueError("Refresh token malformado")

    if is_revoked(jti):
        raise ValueError("Refresh token revogado")

    revoke_jti(jti)

    #Cria novo acess e refresh token
    new_access = create_access_token(sub)
    new_refresh = create_refresh_token(sub)

    return new_access, new_refresh
    