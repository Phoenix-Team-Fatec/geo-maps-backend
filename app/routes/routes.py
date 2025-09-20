from fastapi import APIRouter, HTTPException
from schemas.area_imovel_projeto_schema import Feature
from schemas.coordinate_schema import Coordinate
from schemas.plus_code_schema import PlusCode, CreatePlusCode, ResquestPlusCode
from typing import List
from services.area_imovel_projeto_service import list_properties_service, add_properties_plus_code_service

area_imovel_router = APIRouter(prefix='/area_imovel', tags=['Area_Imovel'])


@area_imovel_router.get('/properties/{cod_cpf}', response_model=List[Feature])
async def list_properties(cod_cpf:str):
    try:
        user_properties = await list_properties_service(cod_cpf)
        return user_properties
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@area_imovel_router.post('/properties/{cod_imovel}/pluscode')
async def add_pluscode(cod_imovel: str, request: ResquestPlusCode):
    try:
        propertie_pluscode = await add_properties_plus_code_service(cod_imovel, request.coordinates, request.owner_name)
        
        return {
            "message": "PlusCode adicionado com sucesso",
            "cod_imovel": cod_imovel,
            "result": propertie_pluscode
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
     
