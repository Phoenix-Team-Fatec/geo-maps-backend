from fastapi import APIRouter, Response, status

admin_route = APIRouter(prefix="/admin", tags=["Admin"])

@admin_route.post("/block_user", status_code=status.HTTP_201_CREATED)
async def block_user_endpoint(user_cpf: str, response: Response):
    """Bloqueia um usuário pelo CPF"""
    from services.admin_service import block_user_service

    result = await block_user_service(user_cpf)
    if "Usuário não encontrado" in result["message"]:
        response.status_code = status.HTTP_404_NOT_FOUND
    return result