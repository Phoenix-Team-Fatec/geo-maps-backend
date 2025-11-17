from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()


MONGO_URL = os.environ.get('MONGO_URL')
DB_NAME = os.environ.get('DB_NAME')


client = AsyncIOMotorClient(MONGO_URL)

db = client[DB_NAME]

collection = db['area_imovel_projeto']
users_collection = db["users"]

async def ensure_indexes():
    await users_collection.create_index(
        "email",
        name="uniq_email",
        unique=True,
        partialFilterExpression={"email": {"$exists": True, "$type": "string"}}
    )
    await users_collection.create_index(
        "cpf",
        name="uniq_cpf",
        unique=True,
        partialFilterExpression={"cpf": {"$exists": True, "$type": "string"}}
    )

if __name__ == "__main__":
    print("Conexão com o Mongo feita com sucesso")


