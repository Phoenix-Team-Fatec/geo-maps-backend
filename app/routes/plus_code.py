# routes/auth_password_reset.py (ou dentro do seu arquivo atual)
from fastapi import APIRouter, Response, status
from app.schemas.plus_code_schema import PlusCode
from app.services.plus_code_service import get_all_plus_codes_from_db

plus_code = APIRouter(prefix="/plus-code", tags=["Plus Code"])

@plus_code.get("/get", status_code=status.HTTP_200_OK, response_model=list[PlusCode])
async def get_all_plus_code():
    """Retorna todos os plus codes cadastrados"""
    pluscodes = await get_all_plus_codes_from_db()
    return pluscodes