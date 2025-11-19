from core.database import db
from core.database import users_collection

admin_collection = db["admins"]

async def create_admin() -> dict:
    
    admin_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    if await admin_collection.find_one({"username": admin_data["username"]}):
        return {"message": "Admin já criado"}
    
    result = await admin_collection.insert_one(admin_data)
    return {"id": str(result.inserted_id), **admin_data}



async def block_user(user_cpf: str):
    user = await users_collection.find_one({"cpf": user_cpf})
    if not user:
        return {"message": "Usuário não encontrado"}
    await users_collection.update_one(
        {"cpf": user_cpf},
        {"$set": {"is_blocked": True}}
    )
    return {"message": f"Usuário com CPF {user_cpf} foi bloqueado"}