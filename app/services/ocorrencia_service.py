from datetime import datetime, timedelta
from app.models.ocorrencia_model import Ocorrencia
from app.repositories.ocorrencia_repository import salvar_ocorrencia
from app.schemas.coordinate_schema import Coordinate
from app.utils.ocorrencia_utils import make_area_from_coordinate
from app.repositories.ocorrencia_repository import listar_ocorrencias_ativas

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

    agora = datetime.now()
    
    ocorrencia_dict = ocorrencia.model_dump()
    ocorrencia_dict["data_registro"] = agora
    ocorrencia_dict["expira_em"] = calcular_expira_em(ocorrencia.gravidade)
    ocorrencia_dict['area'] = make_area_from_coordinate(ocorrencia.coordinate)

    result = await salvar_ocorrencia(ocorrencia_dict)
    return result



async def listar_ocorrencias_ativas_service():
    """
    Lista todas as ocorrências ativas no sistema.
    
    Retorna apenas ocorrências cuja data de expiração ainda não foi atingida.
    Útil para exibir eventos recentes no mapa ou painel do frontend.
    
    Returns:
        list: Lista de ocorrências ativas com dados formatados
    """
    resultados = await listar_ocorrencias_ativas()

    return resultados