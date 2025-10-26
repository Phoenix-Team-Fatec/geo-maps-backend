from pydantic import BaseModel, Field
from typing import Literal, List, Optional
from datetime import datetime

class DirectionsRequest(BaseModel):
    origin: str
    destination: str
    mode: Literal["driving", "walking", "bicycling", "transit"] = Field(
        "driving",
        description="Modo de viagem: driving, walking, bicycling ou transit"
    )
    departure_time: Optional[datetime] = None
    arrival_time:   Optional[datetime] = None
    avoid:           Optional[List[str]]   = None
    waypoints:       Optional[List[str]]   = None
    alternatives:    bool                  = False
    units:           Literal["metric","imperial"] = "metric"
    region:          Optional[str]         = None
    language:        Optional[str]         = None
    traffic_model:   Optional[str]         = None