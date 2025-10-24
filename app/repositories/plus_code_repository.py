from core.database import collection

async def get_all_plus_codes(limit: int = 100):
    """
    Retorna apenas documentos que possuem o campo 'pluscode'.
    Pode ser usado para exibir propriedades ou locais georreferenciados.
    
    Args:
        limit (int): Número máximo de documentos a retornar (padrão: 100)
    
    Returns:
        list: Lista de documentos que possuem o campo 'pluscode'
    """
    resultados = await collection.find({"pluscode": {"$exists": True, "$ne": None}}).to_list(limit)

    return resultados