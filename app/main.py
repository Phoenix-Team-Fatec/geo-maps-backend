from fastapi import FastAPI
from routes.routes import area_imovel_router

app = FastAPI()

app.include_router(area_imovel_router)





