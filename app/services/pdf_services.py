from utils.pdf_utils import gerar_pdf_bytes
from utils.email_utils import send_email_with_attachment
from schemas.plus_code_schema import PlusCode
from starlette.concurrency import run_in_threadpool
from fastapi import BackgroundTasks
from repositories.user import find_user_by_email

async def send_pdf_service(pluscode: PlusCode, background_tasks: BackgroundTasks):
    
    user = await find_user_by_email(pluscode.owner_email)
    
    user_info = {
                "cpf": user['cpf'],
                "nome":user['nome'],
                "sobrenome":user['sobrenome'],
                }  
    
    print(user)
      
    pdf_bytes, pluscode.id = await run_in_threadpool(
            gerar_pdf_bytes, pluscode, user_info
        )
    
    print(f"Enviado no email: {pluscode.owner_email}")

    filename = f"certificado_{pluscode.cod_imovel}.pdf"
    subject = "Seu Certificado de Endereço Digital"
    body = (
            f"Olá {pluscode.owner_email},\n\nSegue em anexo o certificado do imóvel {pluscode.cod_imovel}."
            f"\nHash de validação: {pluscode.id}\n\nAtenciosamente."
        )

    background_tasks.add_task(
                              send_email_with_attachment, 
                              pluscode.owner_email, 
                              subject, 
                              body, 
                              pdf_bytes, 
                              filename
                              )
        
    
    res_dict = {
            "status": "ok",
            "hash": pluscode.id,
            "filename": filename
        }

    return res_dict
