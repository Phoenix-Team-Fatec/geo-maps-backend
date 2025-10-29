from pydantic import BaseModel, Field, EmailStr
from .coordinate_schema import Coordinate
from datetime import datetime
from uuid import uuid4
from typing import Optional, List

class PlusCode(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4())[:8])
    surname: str
    owner_email: EmailStr
    pluscode_cod: str
    cod_imovel: str
    cordinates: Coordinate
    validation_date: datetime = Field(default_factory=datetime.now)
    updates_logs: Optional[list] = []

    class Config:
        arbitrary_types_allowed = True
      

class CreatePlusCode(PlusCode):
    surname: str
    owner_email: EmailStr
    pluscode_cod: str
    cod_imovel: str
    cordinates: Coordinate



class UpdatePlusCode(BaseModel): 
    surname: Optional[str] = None
    owner_email: Optional[EmailStr] = None
    pluscode_cod: Optional[str] = None
    cordinates: Optional[Coordinate] = None


