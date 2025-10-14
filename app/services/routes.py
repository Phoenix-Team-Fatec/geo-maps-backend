import os
from dotenv import load_dotenv
import googlemaps
from datetime import datetime
from fastapi import HTTPException
from fastapi.concurrency import run_in_threadpool
from schemas.routes import DirectionsRequest

load_dotenv()
API_KEY = os.getenv("EXPO_PUBLIC_GOOGLE_MAPS_API_KEY")
if not API_KEY:
    raise RuntimeError("Defina GOOGLE_MAPS_API_KEY no seu .env")

gmaps = googlemaps.Client(key=API_KEY)

def _build_params(req: DirectionsRequest) -> dict:
    params = {
        "origin": req.origin,
        "destination": req.destination,
        "mode": req.mode,
        "units": req.units,
        "alternatives": req.alternatives,
    }
    if req.language:
        params["language"] = req.language
    if req.region:
        params["region"] = req.region
    if req.avoid:
        params["avoid"] = req.avoid
    if req.waypoints:
        params["waypoints"] = req.waypoints
    if req.mode in ("driving", "transit"):
        if req.departure_time:
            params["departure_time"] = req.departure_time
        elif req.mode == "driving":
            params["departure_time"] = datetime.now()
    if req.mode == "transit" and req.arrival_time:
        params["arrival_time"] = req.arrival_time
    if req.mode == "driving" and req.traffic_model:
        params["traffic_model"] = req.traffic_model
    return params

async def get_directions(req: DirectionsRequest):
    params = _build_params(req)
    print(params)
    try:
        result = await run_in_threadpool(gmaps.directions, **params)
        if not result:
            raise HTTPException(status_code=404, detail="Nenhuma rota encontrada")
        return result
    except googlemaps.exceptions.ApiError as e:
        raise HTTPException(status_code=400, detail=f"Google Maps API error: {e}")
