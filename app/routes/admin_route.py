from fastapi import APIRouter, Response, status
from services.admin_service import block_user_service,authenticate_admin
from core.security import create_access_token, create_refresh_token

admin_route = APIRouter(prefix="/admin", tags=["Admin"])

@admin_route.post("/block_user", status_code=status.HTTP_201_CREATED)
async def block_user_endpoint(user_cpf: str, response: Response, is_blocked: bool = False):
    """Bloqueia um usuário pelo CPF"""
    result = await block_user_service(user_cpf, is_blocked)
    if "Usuário não encontrado" in result["message"]:
        response.status_code = status.HTTP_404_NOT_FOUND
    return result


@admin_route.post('/login', status_code=status.HTTP_200_OK)
async def admin_login(username: str, password: str, response: Response):
    """Rota para login do admin"""

    is_authenticated = await authenticate_admin(username, password)
    if not is_authenticated:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"message": "Credenciais inválidas"}
    
    
    access_token = create_access_token(subject='admin')
    refresh_token = create_refresh_token(subject='admin')
    
    return {
        "message": "Login bem-sucedido",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
    
    