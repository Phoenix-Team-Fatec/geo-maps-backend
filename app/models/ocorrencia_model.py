from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from app.schemas.coordinate_schema import Coordinate
from typing import Optional, List

# Definição dos tipos de ocorrência e gravidade 
# Isso garante que apenas valores válidos sejam aceitos pelo backend,
# mesmo que o frontend envie algo diferente.
class TipoOcorrencia(str, Enum):
    transito = "trânsito"
    acidente = "acidente"
    veiculo_acostamento = "veículo no acostamento"
    policia_rodoviaria = "polícia rodoviária"

class GravidadeOcorrencia(str, Enum):
    leve = "leve"
    moderada = "moderada"
    intensa = "intensa"

class Ocorrencia(BaseModel):
    tipo: TipoOcorrencia
    gravidade: GravidadeOcorrencia
    coordinate: Coordinate
    area: Optional[List] = None
    intransitavel: bool = False
    data_registro: datetime = Field(default_factory=datetime.utcnow)
