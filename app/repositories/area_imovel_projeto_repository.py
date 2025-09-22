from app.core.database import collection
from app.schemas.area_imovel_projeto_schema import Properties
from typing import List

async def list_properties(cod_cpf: str) -> List[Properties]:    

    # Properties to find
    document_to_find = {"properties.cod_cpf": cod_cpf}

    # Query for find the document
    cursor = collection.find(document_to_find)

    # Convert the documents into a Properties list
    results = [Properties(**doc['properties']) async for doc in cursor]

    if not results:
        return []
    else: 
        return results
