from fastapi import APIRouter, HTTPException
from models.ocorrencia_model import Ocorrencia
from services.ocorrencia_service import registrar_ocorrencia, listar_ocorrencias_ativas_service, listar_todas_ocorrencias_service
from schemas.coordinate_schema import Coordinate

ocorrencia_router = APIRouter(prefix='/ocorrencia',tags=['Ocorrencias'])

# POST - REGISTRAR OCORRÊNCIAS
# Rota responsável por receber uma nova ocorrência via requisição POST.
# O corpo da requisição (JSON) é validado automaticamente pelo modelo Pydantic (Ocorrencia).
# Caso a validação falhe, o FastAPI retorna automaticamente um erro 422 (Unprocessable Entity).
@ocorrencia_router.post('/adicionar')
async def criar_ocorrencia(ocorrencia: Ocorrencia, user_coordinate: Coordinate):
    try:
        # Chama a função de serviço que faz as validações e salva no banco.
        result = await registrar_ocorrencia(ocorrencia, user_coordinate)

        # Retorna uma resposta simples com status e o ID gerado pelo banco.
        return {"status": "registrado", "id": str(result.inserted_id)}
    
    # Captura erros de validação de negócio definidos no service.
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    # Captura erros inesperados (ex: conexão com banco, falhas internas).
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao registrar ocorrência: {e}")

# GET - LISTAR OCORRÊNCIAS ATIVAS
# Rota para buscar e retornar todas as ocorrências ainda válidas/ativas.
# Essa função chama o service que filtra as ocorrências com base na expiração.
@ocorrencia_router.get("/listar")
async def listar_ocorrencias():
    try:
        # Chama o service que busca no banco apenas as ocorrências válidas.
        resultados = await listar_ocorrencias_ativas_service()
        return resultados
    
        # Captura qualquer erro inesperado e retorna código 500 (erro interno do servidor).
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar ocorrências: {e}")


# GET - LISTAR TODAS AS OCORRÊNCIAS
# Rota para buscar e retornar todas as ocorrências, independentemente do status de expiração
@ocorrencia_router.get("/listar_todas")
async def listar_todas_ocorrencias():
    try:
        # Chama o service que busca no banco todas as ocorrências.
        resultados = await listar_todas_ocorrencias_service()
        return resultados
    
        # Captura qualquer erro inesperado e retorna código 500 (erro interno do servidor).
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar todas as ocorrências: {e}")