from app.repositories.plus_code_repository import get_all_plus_codes

async def get_all_plus_codes_from_db():
    """
    Lista todos os plus codes do sistema.   
    
    Returns:
        list: Lista de plus codes disponiveis.
    """
    resultados = await get_all_plus_codes()
    pluscodes = []
    for doc in resultados:
        if 'pluscode' in doc:
            pluscodes.append(doc['pluscode'])
    
    return pluscodes