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
    result = await ocorrencias_collection.insert_one(ocorrencia_data)
    return result



