from repositories.area_imovel_projeto_repository import list_properties, add_properties_plus_code, get_property_polygon
from schemas.plus_code_schema import CreatePlusCode
from schemas.coordinate_schema import Coordinate
from utils.pluscode_utils import generate_plus_code, validate_coordinate

async def list_properties_service(cod_cpf: str):
    return await list_properties(cod_cpf)

async def add_properties_plus_code_service(cod_imovel:str, coordinates: Coordinate, owner_name: str):
    
    propertie_polygon = await get_property_polygon(cod_imovel)

    is_coordinate_available = validate_coordinate(point_coordinate=coordinates, propertie_coordinates=propertie_polygon)

    if is_coordinate_available:

        lat = coordinates.latitude
        long = coordinates.longitude
        
        user_pluscode = generate_plus_code(lat=lat, long=long)

        pluscode = CreatePlusCode(
            owner_name=owner_name,
            pluscode_cod=user_pluscode,
            cordinates=coordinates
        )
        
        return await add_properties_plus_code(cod_imovel, pluscode)
    
  
    


