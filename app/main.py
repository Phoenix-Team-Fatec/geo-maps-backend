from fastapi import FastAPI
from routes.area_imovel_projeto import area_imovel_router
from routes.plus_code import plus_code
from routes.auth import auth
from routes.auth_password_reset import auth as auth_password_reset
from core.database import ensure_indexes
from fastapi.middleware.cors import CORSMiddleware
from routes.ocorrencia import ocorrencia_router


# Função para criar índices no banco ao iniciar a aplicação
async def lifespan(app: FastAPI):
    await ensure_indexes()
    yield

# Cria a instância do FastAPI com lifespan
app = FastAPI(lifespan=lifespan)

# Configura o CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui as rotas no backend
app.include_router(area_imovel_router)
app.include_router(auth)
app.include_router(ocorrencia_router) 
app.include_router(auth_password_reset)
app.include_router(plus_code)
