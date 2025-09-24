from pymongo.errors import DuplicateKeyError
from core.database import users_collection
from schemas.user import UserCreate, UserRead

#Cria o usuário no banco de dados
async def create_user(user_data: UserCreate) -> UserRead:
    try:
        result = await users_collection.insert_one(user_data)
        return UserRead(id=str(result.inserted_id), **{k: v for k, v in user_data.items() if k != "hashed_password"})
    except DuplicateKeyError:
        raise

#Busca o usuário com base no email
async def find_user_by_email(email: str) -> dict | None:
    return await users_collection.find_one({"email": email})
