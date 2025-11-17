import pluscodes
from shapely import Point, Polygon 
from typing import List, Tuple
from app.schemas.coordinate_schema import Coordinate
from pprint import pprint

class PointOutsideThePolygon(Exception):
    """Excessão para quando uma coordenada não estiver no Polígono"""
    pass


def validate_coordinate(point_coordinate: Coordinate ,propertie_coordinates: List) -> bool:
    poly = Polygon(propertie_coordinates)
    point = Point(point_coordinate.longitude, point_coordinate.latitude)
    if poly.covers(point):
        return True
    else:
        raise PointOutsideThePolygon(f'O ponto passado, não está presente na área do imóvel: {point_coordinate}')



def generate_plus_code(lat: float, long: float) -> str:
    try:
        propertie_pluscode = pluscodes.encode(lat, long)
        return propertie_pluscode
    except Exception as e:
        raise Exception(f"Erro ao gerar o pluscode: {e}")



def best_point(coordinates: Polygon) -> Tuple:
    try:
        centroid = coordinates.centroid
        lat  = centroid.y
        lon = centroid.x
        best_coordinate = (lon, lat)
        return best_coordinate        
    except TypeError as e:
        raise TypeError(f'Objeto {coordinates} não é do tipo Polygon')
    except Exception as e:
        raise Exception(f'Erro ao retornar a melhor coordenada: {e}')
    


