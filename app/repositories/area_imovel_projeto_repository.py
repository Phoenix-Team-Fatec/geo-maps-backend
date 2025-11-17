from app.core.database import collection
from app.schemas.area_imovel_projeto_schema import Feature, PropertyImage
from app.schemas.plus_code_schema import CreatePlusCode, UpdatePlusCode, PlusCode
from typing import List
from datetime import datetime
from app.utils.image_utils import process_property_photo


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
            update_property = await collection.find_one(query_filter) 
            await save_update_log(cod_imovel, update_property['pluscode'])
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
        
        if result:      
            update_property = await collection.find_one(query_filter) 
            await save_update_log(cod_imovel, update_property['pluscode'])
        
        return result


async def save_update_log(cod_imovel: str, info_pluscode: PlusCode) -> None:
    # Finding the property
    query_filter = {'properties.cod_imovel': cod_imovel}
    
    
    update_obj = {
        "surname": info_pluscode.get('surname'),
        "pluscode_cod": info_pluscode.get('pluscode_cod'),
        "coordinates": info_pluscode.get('cordinates'),
        "validation_date": info_pluscode.get('validation_date'),
        "change_date": datetime.now()
    }
    
    update_query = {"$push": {'pluscode.updates_logs': update_obj}}
    result = await collection.update_one(query_filter, update_query)
    
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



async def add_image_to_property(cod_imovel: str, info_img: dict) -> dict:
    query_filter = {'properties.cod_imovel': cod_imovel}
    
    update_operation = {'$set': {'properties.photo': info_img}}
    
    result = await collection.update_one(query_filter, update_operation)
    
    if result.modified_count > 0:
        return info_img
    else:
        raise Exception("Não possível adicionar uma imagem a propriedade")
    
    
 
async def get_property_image(cod_imovel: str) -> str:
    query_filter = {'properties.cod_imovel': cod_imovel}
    doc = await collection.find_one(query_filter)
    
    properties = process_property_photo(doc.get('properties', {}))
    photo_base64 = properties.get('photo')
    
    if not photo_base64:
        raise Exception('Propriedade sem foto')

    return {
        "content_type": "WEBP",
        "image_data": photo_base64
    }
    