from datetime import datetime, timedelta
from models.ocorrencia_model import Ocorrencia
from repositories.ocorrencia_repository import salvar_ocorrencia
from core.database import db
from schemas.coordinate_schema import Coordinate
from utils.ocorrencia_utils import make_area_from_coordinate


def calcular_expira_em(gravidade: str) -> datetime:
    """
    Define por quanto tempo uma ocorrência deve permanecer ativa
    dependendo do nível de gravidade informado pelo usuário.
    Isso ajuda o sistema a "limpar" automaticamente ocorrências antigas.        
    
    Args:
        gravidade (str): Nível de gravidade da ocorrência ('leve', 'moderada' ou 'intensa')
    
    Returns:
        datetime: Data e hora de expiração da ocorrência
    """
    agora = datetime.now()
    if gravidade == "leve":
        return agora + timedelta(minutes=30)
    elif gravidade == "moderada":
        return agora + timedelta(hours=1)
    elif gravidade == "intensa":
        return agora + timedelta(hours=3)
    else:
        return agora + timedelta(hours=1)


async def registrar_ocorrencia(ocorrencia: Ocorrencia, user_coordinate: Coordinate):
    """
    Registra uma nova ocorrência no sistema.
    Realiza:
    - Validações de dados (latitude/longitude)
    - Prevenção de duplicatas ainda ativas
    - Cálculo do tempo de expiração
    - Persistência no banco via repository
    
    Args:
        ocorrencia (Ocorrencia): Objeto com os dados da ocorrência a ser registrada
    
    Returns:
        Resultado da inserção no banco de dados
    
    Raises:
        ValueError: Se latitude/longitude forem inválidas ou se houver duplicata ativa
    """
    
    if ocorrencia.coordinate != user_coordinate:
        raise ValueError("As coordenadas fornecidas não correspondem à localização do usuário")

    ocorrencias_collection = db["ocorrencias"]

    agora = datetime.now()
    duplicata = await ocorrencias_collection.find_one({
        "tipo": ocorrencia.tipo,
        "gravidade": ocorrencia.gravidade,
        "latitude": ocorrencia.coordinate.latitude,
        "longitude": ocorrencia.coordinate.longitude,
        "expira_em": {"$gt": agora}
    })
    if duplicata:
        raise ValueError("Ocorrência duplicada ainda ativa")
    

    ocorrencia_dict = ocorrencia.model_dump()
    ocorrencia_dict["data_registro"] = agora
    ocorrencia_dict["expira_em"] = calcular_expira_em(ocorrencia.gravidade)
    ocorrencia_dict['area'] = make_area_from_coordinate(ocorrencia.coordinate)

    result = await salvar_ocorrencia(ocorrencia_dict)
    return result


async def listar_ocorrencias_ativas(limit: int = 100):
    """
    Lista apenas ocorrências ativas.
    
    Busca no banco todas as ocorrências cuja data de expiração
    ainda não foi atingida. Útil para exibir apenas eventos recentes
    no mapa ou painel do frontend.
    
    Args:
        limit (int): Número máximo de ocorrências a retornar (padrão: 100)
    
    Returns:
        list: Lista de ocorrências ativas com dados formatados
    """
    ocorrencias_collection = db["ocorrencias"]
    agora = datetime.now()
    resultados = await ocorrencias_collection.find({"expira_em": {"$gt": agora}}).to_list(limit)

    for ocorrencia in resultados:
        ocorrencia["_id"] = str(ocorrencia["_id"])
        ocorrencia["data_registro"] = ocorrencia["data_registro"].strftime("%d/%m/%Y %H:%M")
        ocorrencia["expira_em"] = ocorrencia["expira_em"].strftime("%d/%m/%Y %H:%M")

    return resultados
