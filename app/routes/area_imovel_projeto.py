from fastapi import APIRouter, HTTPException, BackgroundTasks
from starlette.concurrency import run_in_threadpool
from schemas.area_imovel_projeto_schema import Feature
from schemas.coordinate_schema import Coordinate
from schemas.plus_code_schema import PlusCode, CreatePlusCode, UpdatePlusCode, ResquestPlusCode
from typing import List
from services.area_imovel_projeto_service import list_properties_service, add_properties_plus_code_service, update_property_plus_code_service
from utils.pdf_utils import gerar_pdf_bytes
from utils.email_utils import send_email_with_attachment


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
async def create_certificate(req: PlusCode, email:str , background_tasks: BackgroundTasks):
    try:
        pdf_bytes, req.id = await run_in_threadpool(
            gerar_pdf_bytes, req
        )

        filename = f"certificado_{req.cod_imovel}.pdf"
        subject = "Seu Certificado de Endereço Digital"
        body = (
            f"Olá {req.owner_name},\n\nSegue em anexo o certificado do imóvel {req.cod_imovel}."
            f"\nHash de validação: {req.id}\n\nAtenciosamente."
        )

        background_tasks.add_task(send_email_with_attachment, email, subject, body, pdf_bytes, filename)

        return {"status": "ok", "hash": req.id, "filename": filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))