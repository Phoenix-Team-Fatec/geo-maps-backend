from fastapi import APIRouter, HTTPException
from services.routes import get_directions
from schemas.routes import DirectionsRequest

routes_router = APIRouter(prefix='/rotas', tags=['Rotas'])


@routes_router.post('/', response_model=list)
async def trace_route(req: DirectionsRequest):
    try:
        route = await get_directions(req)
        return route
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))