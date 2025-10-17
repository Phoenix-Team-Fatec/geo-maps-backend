from shapely import Point, Polygon
from schemas.coordinate_schema import Coordinate

def make_area_from_coordinate(coordinate:Coordinate) -> Polygon:
    ponto = Point(coordinate.longitude, coordinate.latitude)
    area = ponto.buffer(0.0002)
    return area.__geo_interface__['coordinates']