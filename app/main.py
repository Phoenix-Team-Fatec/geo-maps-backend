from fastapi import FastAPI
from app.routes.area_imovel_projeto import area_imovel_router
from app.routes.auth import auth
from app.core.database import ensure_indexes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cria índices no banco ao iniciar a aplicação
async def lifespan(app: FastAPI):
    await ensure_indexes()
    yield

# Inclui as rotas
app.include_router(area_imovel_router)
app.include_router(auth)
