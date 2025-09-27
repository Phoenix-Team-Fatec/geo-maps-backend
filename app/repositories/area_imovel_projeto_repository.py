from core.database import collection
from schemas.area_imovel_projeto_schema import Feature
from schemas.plus_code_schema import CreatePlusCode, UpdatePlusCode
from typing import List


async def list_properties(cod_cpf: str) -> Feature:    

    # Properties to find
    query = {"properties.cod_cpf": cod_cpf}

    # Query for find the document
    cursor = collection.find(query)

    # Convert the documents into a Properties list
    results = [Feature(**doc) async for doc in cursor]

    if not results:
        return []
    else: 
        return results
    

async def add_properties_plus_code(cod_imovel: str, pluscode: CreatePlusCode) -> None:

        # Find the property by cod_imovel, that will be add a pluscode
        query_filter = {'properties.cod_imovel': cod_imovel}

        # Pluscode for the property
        user_pluscode = pluscode.model_dump()

        # CRUD operation to add a pluscode
        update_operation = {'$set':
                            {'pluscode': user_pluscode},
                            }
        
        print(update_operation)

        # Add the pluscode into the document
        result = await collection.update_one(query_filter, update_operation)
        
        if result.modified_count > 0:
            return pluscode
        else:
            raise Exception("Não foi possível adicionar o PlusCode")
        


async def update_properties_plus_code(cod_imovel: str, pluscode: UpdatePlusCode) -> None:

        # Find the property by cod_imovel, that will be add a pluscode
        query_filter = {'properties.cod_imovel': cod_imovel}

        # Checking null values
        user_pluscode = {key: value for key, value in pluscode.model_dump().items() if value is not None}

        # Mounting the query
        update_operation = {'$set': {f'pluscode.{key}': value for key, value in user_pluscode.items()}}

        # Making the update 
        result = await collection.update_one(query_filter, update_operation)
        
        return result


    

async def get_property_polygon(cod_imovel:str) -> List:

    # Finding the property     
    query_filter = {'properties.cod_imovel': cod_imovel}

    # Filtering the fields 
    projection = {'geometry.coordinates': 1, '_id': 0}

    # CRUD operation for the property polygon
    result = await collection.find_one(query_filter, projection)

    # Trasnforming the data 
    list_coordinates = result.get('geometry', {}).get('coordinates',[]) 

    result_list = []

    for coordenadas in list_coordinates:
         for coordenada in coordenadas:
              result_list.append(tuple(coordenada))

    if not result:
          raise Exception(f'Imóvel com código {cod_imovel} não encontrado')
     
    return result_list


