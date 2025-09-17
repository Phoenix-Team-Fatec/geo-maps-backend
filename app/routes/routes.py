from fastapi import APIRouter, HTTPException
from schemas.area_imovel_projeto_schema import Properties
from typing import List
from services.area_imovel_projeto_service import list_properties_service

area_imovel_router = APIRouter(prefix='/area_imovel', tags=['Area_Imovel'])


@area_imovel_router.get('/properties/{cod_cpf}', response_model=List[Properties])
async def list_properties(cod_cpf:str):
    try:
        user_properties = await     list_properties_service(cod_cpf)
        return user_properties
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

