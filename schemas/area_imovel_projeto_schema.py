from pydantic import BaseModel
from typing import List, Optional,Tuple
from bson import ObjectId

# Modelo para as coordenadas (lista de [longitude, latitude])
class Coordinate(BaseModel):
    # Cada coordenada é uma tupla de dois floats (longitude, latitude)
    longitude: float
    latitude: float

    # Configuração para permitir a conversão de listas em tuplas
    class Config:
        arbitrary_types_allowed = True

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

# Modelo principal que representa a estrutura completa do GeoJSON
class Feature(BaseModel):
    id: str  # ID do recurso (não o ObjectId, mas o campo 'id' do JSON)
    type: str  # Tipo do recurso, ex: "Feature"
    geometry: Geometry  # Geometria do imóvel
    properties: Properties  # Propriedades do imóvel
    _id: ObjectId  # ObjectId do MongoDB

    # Configuração para suportar ObjectId e validação
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str  # Converte ObjectId para string no JSON
        }