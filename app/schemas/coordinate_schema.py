from pydantic import BaseModel

# Modelo para as coordenadas (lista de [longitude, latitude])
class Coordinate(BaseModel):
    # Cada coordenada é uma tupla de dois floats (longitude, latitude)
    longitude: float
    latitude: float

    # Configuração para permitir a conversão de listas em tuplas
    class Config:
        arbitrary_types_allowed = True