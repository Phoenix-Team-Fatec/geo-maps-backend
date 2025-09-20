from pydantic import BaseModel, Field
from .coordinate_schema import Coordinate
from datetime import datetime
from uuid import uuid4

class PlusCode(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4())[:8])
    owner_name: str
    pluscode_cod: str
    cordinates: Coordinate
    validation_date: datetime = Field(default_factory=datetime.now)

    class Config:
        arbitrary_types_allowed = True
      

class CreatePlusCode(PlusCode):
    owner_name: str
    pluscode_cod: str
    cordinates: Coordinate


class ResquestPlusCode(BaseModel):
    coordinates: Coordinate
    owner_name: str






