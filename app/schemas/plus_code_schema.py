from pydantic import BaseModel, Field, EmailStr
from .coordinate_schema import Coordinate
from datetime import datetime
from uuid import uuid4
from typing import Optional

class PlusCode(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4())[:8])
    owner_email: EmailStr
    pluscode_cod: str
    cod_imovel: str
    cordinates: Coordinate
    validation_date: datetime = Field(default_factory=datetime.now)

    class Config:
        arbitrary_types_allowed = True
      

class CreatePlusCode(PlusCode):
    owner_email: EmailStr
    pluscode_cod: str
    cod_imovel: str
    cordinates: Coordinate



class UpdatePlusCode(BaseModel): 
    owner_email: Optional[EmailStr] = None
    pluscode_cod: Optional[str] = None
    cordinates: Optional[Coordinate] = None


