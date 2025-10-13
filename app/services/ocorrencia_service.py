from datetime import datetime, timedelta
from app.models.ocorrencia_model import Ocorrencia
from app.repositories.ocorrencia_repository import salvar_ocorrencia
from app.core.database import db
from fastapi import HTTPException

# Função para definir expiração com base na gravidade
# Define por quanto tempo uma ocorrência deve permanecer ativa
# dependendo do nível de gravidade informado pelo usuário.
# Isso ajuda o sistema a "limpar" automaticamente ocorrências antigas.
def calcular_expira_em(gravidade: str) -> datetime:

    agora = datetime.utcnow() # Usa UTC para consistência entre servidores

    if gravidade == "leve":
        return agora + timedelta(minutes=30)
    elif gravidade == "moderada":
        return agora + timedelta(hours=1)
    elif gravidade == "intensa":
        return agora + timedelta(hours=3)
    else:
        # fallback de segurança caso algo inesperado ocorra
        return agora + timedelta(hours=1)  


# Função principal: registrar nova ocorrência
# Realiza:
# - validações de dados (latitude/longitude)
# - prevenção de duplicatas ainda ativas
# - cálculo do tempo de expiração
# - persistência no banco via repository
async def registrar_ocorrencia(ocorrencia: Ocorrencia):

    # Validação de coordenadas geográficas
    if not (-90 <= ocorrencia.latitude <= 90):
        raise ValueError("Latitude inválida")
    if not (-180 <= ocorrencia.longitude <= 180):
        raise ValueError("Longitude inválida")

    # Acesso à coleção de ocorrências
    ocorrencias_collection = db["ocorrencias"]

    # Verificação de duplicatas
    # Impede registrar uma nova ocorrência se já existir uma
    # do mesmo tipo, gravidade e coordenadas que ainda esteja ativa.
    agora = datetime.utcnow()
    duplicata = await ocorrencias_collection.find_one({
        "tipo": ocorrencia.tipo,
        "gravidade": ocorrencia.gravidade,
        "latitude": ocorrencia.latitude,
        "longitude": ocorrencia.longitude,
        "expira_em": {"$gt": agora} # só considera ocorrências ainda válidas
    })
    if duplicata:
        raise ValueError("Ocorrência duplicada ainda ativa")

    # Converte o objeto Pydantic para dict e adiciona campos calculados.
    ocorrencia_dict = ocorrencia.dict()
    ocorrencia_dict["data_registro"] = agora
    ocorrencia_dict["expira_em"] = calcular_expira_em(ocorrencia.gravidade)

    # Inserção no banco
    result = await salvar_ocorrencia(ocorrencia_dict)
    return result


# Função para listar apenas ocorrências ativas
# Busca no banco todas as ocorrências cuja data de expiração
# ainda não foi atingida. Útil para exibir apenas eventos recentes
# no mapa ou painel do frontend.
async def listar_ocorrencias_ativas(limit: int = 100):
    ocorrencias_collection = db["ocorrencias"]
    agora = datetime.utcnow()

    # Busca as ocorrências não expiradas (expira_em > agora)
    resultados = await ocorrencias_collection.find({"expira_em": {"$gt": agora}}).to_list(limit)

    # Formatação dos dados de saída
    # - Converte o _id (ObjectId) para string
    # - Formata datas para padrão legível "dd/mm/yyyy hh:mm"
    for ocorrencia in resultados:
        ocorrencia["_id"] = str(ocorrencia["_id"])
        ocorrencia["data_registro"] = ocorrencia["data_registro"].strftime("%d/%m/%Y %H:%M")
        ocorrencia["expira_em"] = ocorrencia["expira_em"].strftime("%d/%m/%Y %H:%M")

    return resultados
