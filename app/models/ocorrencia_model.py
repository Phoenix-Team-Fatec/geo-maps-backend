from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


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
    latitude: float
    longitude: float
    data_registro: datetime = Field(default_factory=datetime.utcnow)
