from repositories.admin_repositorie import block_user



async def block_user_service(user_cpf: str):
    return await block_user(user_cpf)





