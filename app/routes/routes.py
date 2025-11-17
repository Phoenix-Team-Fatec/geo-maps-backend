from fastapi import APIRouter, HTTPException
from app.services.routes import get_directions
from app.schemas.routes import DirectionsRequest

routes_router = APIRouter(prefix='/rotas', tags=['Rotas'])


@routes_router.post('/')
async def trace_route(req: DirectionsRequest):
    try:
        route = await get_directions(req)
        return route
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))