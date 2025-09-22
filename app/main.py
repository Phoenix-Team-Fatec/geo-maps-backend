from fastapi import FastAPI
from routes.area_imovel_projeto import area_imovel_router
from routes.auth import auth
from core.database import ensure_indexes

#Cria índices no banco de dados ao iniciar a aplicação (evita usuários duplicados)
async def lifespan(app: FastAPI):
    await ensure_indexes()
    yield

#Declara uma constante para o FastAPI
app = FastAPI(lifespan=lifespan)

#Inclui as rotas no backend
app.include_router(area_imovel_router)
app.include_router(auth)
