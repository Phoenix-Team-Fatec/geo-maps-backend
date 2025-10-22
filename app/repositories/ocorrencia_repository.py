from datetime import datetime
from core.database import db



# A variável 'db' é importada da configuração principal de conexão (app/core/database.py).
# Aqui, acessamos a coleção 'ocorrencias' dentro do banco de dados,
# que é onde todos os registros de ocorrências serão armazenados.
ocorrencias_collection = db["ocorrencias"]


# Função para salvar ocorrências
# Essa função é responsável apenas por inserir os dados no banco.
# Não realiza validações — isso é responsabilidade da camada "service".
async def salvar_ocorrencia(ocorrencia_data: dict):
    """
    Insere uma nova ocorrência no banco de dados MongoDB.
    
    Parâmetros:
        ocorrencia_data (dict): Dados já validados da ocorrência.
    
    Retorna:
        result (InsertOneResult): Resultado da operação de inserção,
        incluindo o 'inserted_id' que identifica o documento salvo.
    """
    agora = datetime.now()
    duplicata = await ocorrencias_collection.find_one({
        "tipo": ocorrencia_data['tipo'],
        "gravidade": ocorrencia_data['gravidade'],
        "latitude": ocorrencia_data['coordinate']['latitude'],
        "longitude": ocorrencia_data['coordinate']['longitude'],
        "expira_em": {"$gt": agora}
    })
    if duplicata:
        raise ValueError("Ocorrência duplicada ainda ativa")
    
    result = await ocorrencias_collection.insert_one(ocorrencia_data)
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
    agora = datetime.now()
    resultados = await ocorrencias_collection.find({"expira_em": {"$gt": agora}}).to_list(limit)

    for ocorrencia in resultados:
        ocorrencia["_id"] = str(ocorrencia["_id"])
        ocorrencia["data_registro"] = ocorrencia["data_registro"].strftime("%d/%m/%Y %H:%M")
        ocorrencia["expira_em"] = ocorrencia["expira_em"].strftime("%d/%m/%Y %H:%M")

    return resultados
