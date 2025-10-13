from repositories.area_imovel_projeto_repository import list_properties
from repositories.area_imovel_projeto_repository import list_properties, add_properties_plus_code, get_property_polygon, update_properties_plus_code, add_image_to_property, get_property_image
from schemas.plus_code_schema import CreatePlusCode, UpdatePlusCode
from utils.pluscode_utils import generate_plus_code, validate_coordinate
from utils.image_utils import compress_image
from bson import Binary
import base64

async def list_properties_service(cod_cpf: str):
    return await list_properties(cod_cpf)

async def add_properties_plus_code_service(cod_imovel:str, create_data: CreatePlusCode):
    
    propertie_polygon = await get_property_polygon(cod_imovel)

    is_coordinate_available = validate_coordinate(point_coordinate=create_data.cordinates, propertie_coordinates=propertie_polygon)

    if is_coordinate_available:

        lat = create_data.cordinates.latitude
        long = create_data.cordinates.longitude
        
        user_pluscode = generate_plus_code(lat=lat, long=long)

        create_data.pluscode_cod = user_pluscode
        create_data.cod_imovel = cod_imovel
        
        return await add_properties_plus_code(cod_imovel, create_data)
    
  
async def update_property_plus_code_service(cod_imovel:str, update_data: UpdatePlusCode):

    if update_data.cordinates:
        
        propertie_polygon = await get_property_polygon(cod_imovel)
        
        is_coordinate_available = validate_coordinate(point_coordinate=update_data.cordinates, propertie_coordinates=propertie_polygon)
        
        if is_coordinate_available:
            lat = update_data.cordinates.latitude
            long = update_data.cordinates.longitude

            update_data.pluscode_cod = generate_plus_code(lat=lat, long=long)

    return await update_properties_plus_code(cod_imovel=cod_imovel, pluscode=update_data)



async def add_property_img(cod_imovel: str, contents):    
    bytes = compress_image(contents)
    
    data = {'image_data': Binary(bytes)}
    await add_image_to_property(cod_imovel, data)
    
    return {
        'image_data': base64.b64encode(bytes).decode('utf-8'),
        'content_type': 'WEBP'
    }
    
async def get_img_service(cod_imovel:str):
    return await get_property_image(cod_imovel)
    