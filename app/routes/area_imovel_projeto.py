from fastapi import APIRouter, HTTPException, BackgroundTasks, UploadFile, File
from fastapi.responses import StreamingResponse
from schemas.area_imovel_projeto_schema import Feature, PropertyImage
from schemas.plus_code_schema import PlusCode, CreatePlusCode, UpdatePlusCode
from typing import List
from services.area_imovel_projeto_service import list_properties_service, add_properties_plus_code_service, update_property_plus_code_service, add_property_img, get_img_service
from services.pdf_services import send_pdf_service


area_imovel_router = APIRouter(prefix='/area_imovel', tags=['Area_Imovel'])


@area_imovel_router.get('/properties/{cod_cpf}', response_model=List[Feature])
async def list_properties(cod_cpf:str):
    try:
        user_properties = await list_properties_service(cod_cpf)
        return user_properties
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@area_imovel_router.post('/properties/{cod_imovel}/pluscode')
async def add_pluscode(cod_imovel: str, request: CreatePlusCode):
    try:
        property_pluscode = await add_properties_plus_code_service(cod_imovel, request)
        return {
            "message": "PlusCode adicionado com sucesso",
            "cod_imovel": cod_imovel,
            "result": property_pluscode
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
     

@area_imovel_router.put('/properties/{cod_imovel}/pluscode')
async def update_pluscode(cod_imovel: str, request:UpdatePlusCode ):
    try:
        property_pluscode = await update_property_plus_code_service(cod_imovel, request)
        return {
            "message": "PlusCode atualizado com sucesso",
            "cod_imovel": cod_imovel
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
        

@area_imovel_router.post('/properties/pluscode/pdf')
async def create_certificate(req_pluscode: PlusCode, background_tasks: BackgroundTasks):
    try:
        response = await send_pdf_service(req_pluscode, background_tasks)
        return {
            "message": "Certificado será enviado por email em breve",
            "cod_imovel": req_pluscode.cod_imovel,
            "hash": response["hash"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@area_imovel_router.post('/upload/{cod_imovel}/img', response_model=PropertyImage)
async def upload_property_img(cod_imovel:str, file: UploadFile = File(...)):
    try:
        contents = await file.read()
        response = await add_property_img(cod_imovel, contents=contents)
        return PropertyImage(**response)        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))   
    

@area_imovel_router.get('image/{cod_imovel}/property', response_model=PropertyImage)
async def get_property_img(cod_imovel:str):
    try:
        property_image = await get_img_service(cod_imovel)
        return PropertyImage(**property_image)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
