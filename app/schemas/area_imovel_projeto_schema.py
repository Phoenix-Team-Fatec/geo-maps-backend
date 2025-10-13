from pydantic import BaseModel
from typing import List, Optional,Union
from bson import ObjectId
from .plus_code_schema import PlusCode

# Modelo para a geometria do tipo Polygon
class Geometry(BaseModel):
    type: str  # Tipo da geometria, ex: "Polygon"
    coordinates: List[List[List[float]]]  # Lista de listas de coordenadas (formato GeoJSON para Polygon)

# Modelo para as propriedades do imóvel
class Properties(BaseModel):
    cod_cpf: Optional[str] = None
    cod_estado: Optional[str] = None
    cod_imovel: Optional[str] = None
    cod_tema: Optional[str] = None
    dat_atuali: Optional[str] = None
    dat_criaca: Optional[str] = None
    des_condic: Optional[str] = None
    ind_status: Optional[str] = None
    ind_tipo: Optional[str] = None
    mod_fiscal: Optional[float] = None
    municipio: Optional[str] = None
    nom_tema: Optional[str] = None
    num_area: Optional[float] = None
    photo: Optional[Union[str, dict]] = None

# Modelo principal que representa a estrutura completa do GeoJSON
class Feature(BaseModel):
    id: str  # ID do recurso (não o ObjectId, mas o campo 'id' do JSON)
    geometry: Geometry  # Geometria do imóvel
    properties: Properties  # Propriedades do imóvel
    _id: ObjectId  # ObjectId do MongoDB
    pluscode: Optional[PlusCode] = None

    # Configuração para suportar ObjectId e validação
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str  # Converte ObjectId para string no JSON
        }
        

class PropertyImage(BaseModel):
    content_type: Optional[str] = 'WEBP'
    image_data: str
