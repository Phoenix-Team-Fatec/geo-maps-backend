import os
from dotenv import load_dotenv
import googlemaps
from datetime import datetime
from fastapi import HTTPException
from fastapi.concurrency import run_in_threadpool
from shapely.geometry import Point

from app.schemas.routes import DirectionsRequest
from app.services.ocorrencia_service import listar_ocorrencias_ativas_service  

# Carrega a chave do Google Maps
load_dotenv()
API_KEY = os.getenv("EXPO_PUBLIC_GOOGLE_MAPS_API_KEY")
if not API_KEY:
    raise RuntimeError("Defina EXPO_PUBLIC_GOOGLE_MAPS_API_KEY no seu .env")

gmaps = googlemaps.Client(key=API_KEY)


# Monta parâmetros para a API do Google Maps
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


# Função auxiliar para ver se algum passo da rota passa por um bloqueio
def verifica_bloqueios_na_rota(steps, bloqueios):
    for step in steps:
        lat = step["start_location"]["lat"]
        lng = step["start_location"]["lng"]
        ponto_rota = Point(lng, lat)

        for bloqueio in bloqueios:
            lat_b = bloqueio["coordinate"]["latitude"]
            lng_b = bloqueio["coordinate"]["longitude"]
            ponto_alerta = Point(lng_b, lat_b)

            # Distância aproximada de ~15 metros
            if ponto_rota.distance(ponto_alerta) < 0.00015:
                return bloqueio
    return None


# Função principal que obtém direções e verifica bloqueios
async def get_directions(req: DirectionsRequest):
    # 1) Busca todas as ocorrências ativas
    ocorrencias = await listar_ocorrencias_ativas_service()

    # 2) Filtra somente as intensas + intransitáveis
    bloqueios = [
        oc for oc in ocorrencias
        if oc.get("intransitavel") is True and oc.get("gravidade", "").lower() == "intensa"
    ]

    # 3) Solicita rotas ao Google Maps
    params = _build_params(req)
    result = await run_in_threadpool(gmaps.directions, **params)

    if not result:
        raise HTTPException(status_code=404, detail="Nenhuma rota encontrada.")

    # 4) Verifica TODAS as rotas alternativas
    rota_segura = None
    primeiro_bloqueio = None

    for rota in result:
        steps = rota["legs"][0]["steps"]
        bloqueio = verifica_bloqueios_na_rota(steps, bloqueios)

        if not bloqueio:
            rota_segura = rota
            break
        else:
            if primeiro_bloqueio is None:
                primeiro_bloqueio = bloqueio

    # 5) Se encontrou rota segura → retorna
    if rota_segura:
        return {
            "rota_disponivel": True,
            "mensagem": "Rota alternativa encontrada e está acessível.",
            "rota": rota_segura,
        }

    # 6) Caso contrário, alerta obrigatório
    return {
        "rota_disponivel": False,
        "mensagem": "Todas as rotas disponíveis possuem bloqueio grave.",
        "alerta": {
            "tipo": primeiro_bloqueio["tipo"],
            "gravidade": primeiro_bloqueio["gravidade"],
            "coordenadas": primeiro_bloqueio["coordinate"],
        },
    }
